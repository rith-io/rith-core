"""Arithmetic User Data Model required for User Accounts.

Created by Joshua Powell on 02/02/2019.

Copyright (c) 2019 Joshua Powell, L.L.C. All rights reserved.

For license and copyright information please see the LICENSE.md (the "License")
document packaged with this software. This file and all other files included in
this packaged software may not be used in any manner except in compliance with
the License. Software distributed under this License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTY, OR CONDITIONS OF ANY KIND, either express or
implied.

See the License for the specific language governing permission and limitations
under the License.
"""


import hashlib


from flask_security import current_user
from flask_security import UserMixin
from flask_security import SQLAlchemyUserDatastore


from werkzeug import generate_password_hash
from werkzeug import check_password_hash


from rith import db
from rith import logger


from rith.schema.role import Role


"""User Roles schema definition.

These tables are necessary to perform our many to many relationships

@see https://pythonhosted.org/Flask-SQLAlchemy/models.html\
      #many-to-many-relationships
   This documentation is specific to Flask using sqlalchemy

@see http://docs.sqlalchemy.org/en/rel_0_9/orm/relationships.html\
      #relationships-many-to-many
   This documentation covers SQLAlchemy
"""
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    extend_existing=True
)


class User(db.Model, UserMixin):
    """User schema definition.

    The `User` database table definition used throughout the system to
    identify, authenticate, and manage system users

    @param (object) db.Model
    @param (object) UserMixin
    """

    """Database table details.

    See the official SQLAlchemy documetation for more information
    http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html\
        #table-configuration
    """
    __tablename__ = 'user'
    __table_args__ = {
        'extend_existing': True
    }

    __def__ = {
        "access": "private",
        "fields": {
            "email": {
                "field_label": "Email Address",
                "field_help": "A valid email address (not public)",
                "field_order": 1,
                "component": {
                    "name": "textfield",
                    "options": {
                        "max-length": 0,
                        "allowed_characters": "ascii"
                    },
                    "group": "User Information"
                },
                "is_editable": True,
                "is_required": True,
            },
            "password": {
                "field_label": "Password",
                "field_help": "",
                "field_order": 2,
                "component": {
                    "name": "password",
                    "options": {},
                    "group": "User Information"
                },
                "is_editable": True,
                "is_required": True,
            },
            "active": {
                "field_label": "Active",
                "field_help": "",
                "field_order": 3,
                "component": {
                    "name": "boolean",
                    "options": {},
                    "group": "User Information"
                },
                "is_editable": True,
                "is_required": True,
            },
            "first_name": {
                "field_label": "First Name",
                "field_help": "",
                "field_order": 1,
                "component": {
                    "name": "textfield",
                    "options": {},
                    "group": "User Profile"
                },
                "is_editable": True,
                "is_required": False,
            },
            "last_name": {
                "field_label": "Last Name",
                "field_help": "",
                "field_order": 2,
                "component": {
                    "name": "textfield",
                    "options": {},
                    "group": "User Profile"
                },
                "is_editable": True,
                "is_required": False,
            },
            "background": {
                "field_label": "Background",
                "field_help": "",
                "field_order": 3,
                "component": {
                    "name": "textarea",
                    "options": {},
                    "group": "User Profile"
                },
                "is_editable": True,
                "is_required": False,
            },
            "picture": {
                "field_label": "Profile Picture",
                "field_help": "",
                "field_order": 4,
                "component": {
                    "name": "image",
                    "options": {
                        "allowed_extensions": [
                            "JPG",
                            "jpg",
                            "JPEG",
                            "jpeg",
                            "GIF",
                            "gif",
                            "PNG",
                            "png"
                        ],
                        "multiple": False
                    },
                    "group": "User Profile"
                },
                "is_editable": True,
                "is_required": False,
            },
            "title": {
                "field_label": "Title",
                "field_help": "",
                "field_order": 1,
                "component": {
                    "name": "textfield",
                    "options": {},
                    "group": "Job Information"
                },
                "is_editable": True,
                "is_required": False,
            },
            "organization_name": {
                "field_label": "Organization Name",
                "field_help": "",
                "field_order": 2,
                "component": {
                    "name": "textfield",
                    "options": {},
                    "group": "Job Information"
                },
                "is_editable": True,
                "is_required": False,
            },
            "roles": {
                "field_label": "Roles",
                "field_help": "",
                "field_order": 1,
                "component": {
                    "name": "relationship",
                    "options": {},
                    "group": "Roles"
                },
                "is_editable": True,
                "is_required": True,
            },
            "confirmed_at": {
                "field_label": "Confirmed At",
                "field_help": "",
                "field_order": 1,
                "component": {
                    "name": "datetime",
                    "options": {},
                    "group": "Account History"
                },
                "is_editable": False,
                "is_required": True,
            },
            "last_login_at": {
                "field_label": "Last Login At",
                "field_help": "",
                "field_order": 2,
                "component": {
                    "name": "datetime",
                    "options": {},
                    "group": "Account History"
                },
                "is_editable": False,
                "is_required": True,
            },
            "current_login_at": {
                "field_label": "Current Login At",
                "field_help": "",
                "field_order": 4,
                "component": {
                    "name": "datetime",
                    "options": {},
                    "group": "Account History"
                },
                "is_editable": False,
                "is_required": True,
            },
            "last_login_ip": {
                "field_label": "Last Login IP",
                "field_help": "",
                "field_order": 3,
                "component": {
                    "name": "textfield",
                    "options": {},
                    "group": "Account History"
                },
                "is_editable": False,
                "is_required": True,
            },
            "current_login_ip": {
                "field_label": "Current Login IP",
                "field_help": "",
                "field_order": 5,
                "component": {
                    "name": "textfield",
                    "options": {},
                    "group": "Account History"
                },
                "is_editable": False,
                "is_required": True,
            },
            "login_count": {
                "field_label": "Login Count",
                "field_help": "",
                "field_order": 6,
                "component": {
                    "name": "number",
                    "options": {},
                    "group": "Account History"
                },
                "is_editable": False,
                "is_required": True,
            }
        }
    }

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    active = db.Column(db.Boolean)

    confirmed_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.Text)
    current_login_ip = db.Column(db.Text)
    login_count = db.Column(db.Integer)

    roles = db.relationship('Role', **{
        'secondary': user_roles,
        'backref': db.backref('users')
    })

    def __init__(self, email, password=None, active=False, background=None,
                 picture=None, title=None, organization_name=None,
                 confirmed_at=None, last_login_at=None,
                 current_login_at=None, last_login_ip=None,
                 current_login_ip=None, login_count=0, roles=None,
                 organizations=None):
        """Role schema definition constructor.

        @param (object) self
        @param (string) email
        @param (string) password
        @param (boolean) active
        @param (string) first_name
        @param (string) last_name
        @param (string) bio
        @param (string) picture
        @param (string) title
        @param (string) organization_name
        @param (datetime) confirmed_at
        @param (datetime) last_login_at
        @param (datetime) current_login_at
        @param (string) last_login_ip
        @param (string) current_login_ip
        @param (integer) login_count
        @param (array) roles
        """
        self.email = email
        self.password = password
        self.active = active
        self.background = background
        self.picture = picture
        self.title = title
        self.organization_name = organization_name
        self.confirmed_at = confirmed_at
        self.last_login_at = last_login_at
        self.current_login_at = current_login_at
        self.last_login_ip = last_login_ip
        self.current_login_ip = current_login_ip
        self.login_count = login_count
        self.roles = roles if roles else []
        self.organizations = organizations if organizations else []

    def set_password(self, password):
        """Generate a password hash based on user input.

        Set the user password using the pbkdf2:sha1 method and a
        salt_length of 128

        @param (object) self
        @param (string) password
            The password to set in the database
        """
        self.password = generate_password_hash(password, method='pbkdf2:sha1',
                                               salt_length=128)

    def check_password(self, password):
        """Verify password is correct by hashing and comparing hashes.

        Check to see if the password entered by the user matches the password
        saved in the database associated with the acting user

        @param (object) self
        @param (string) password
        The password to check against the database
        @return (bool)
            The boolean of whether or not the passwords match
        """
        return check_password_hash(self.password, password)

    def user_get(self):
        """Get the SQLAlchemy User object for the current_user.

        @param (object) self
        @return (object) user_
            The object of the current user, not to be confused with
            current_user
        """
        return {
            'id': self.id,
            # 'first_name': self.first_name,
            # 'last_name': self.last_name,
            # 'picture': self.picture,
        }


"""Setup User/Role Datastore for Flask Security.

The last thing we need to do is actually hook these things up to the
User Datastore provided by SQLAlchemy's Engine's datastore that provides
Flask-Security with User/Role information so we can lock down access
to the system and it's resources.

See the official Flask Security documentation for more information
https://pythonhosted.org/Flask-Security/api.html#flask_security.datastore.SQLAlchemyUserDatastore
"""
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
