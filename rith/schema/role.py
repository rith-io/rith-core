"""Arithmetic Role Data Model required for User Accounts.

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


from sqlalchemy import event


from flask_security import RoleMixin


from rith import db


class Role(db.Model, RoleMixin):
    """Role schema definition.

    The `Role` database table definition used throughout the system to grant
    permissions to specific users

    @param (object) db.Model
    @param (object) RoleMixin
    """

    """Name of the database table that holds `role` data.

    @see http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/
         declarative.html#table-configuration
    """
    __tablename__ = 'role'
    __table_args__ = {
      'extend_existing': True
    }

    __def__ = {
        "access": "private",
        "fields": {
            "name": {
                "field_label": "Role Name",
                "field_help": "",
                "field_order": 1,
                "component": {
                    "name": "textfield",
                    "options": {},
                    "group": "Role Information"
                },
                "is_editable": True,
                "is_required": True,
            },
            "description": {
                "field_label": "Role Description",
                "field_help": "",
                "field_order": 2,
                "component": {
                    "name": "textfield",
                    "options": {},
                    "group": "Role Information"
                },
                "is_editable": True,
                "is_required": True,
            },
        }
    }

    """Fields within the data model."""
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)

    def __init__(self, name, description=None):
        """Role schema definition.

        @param (object) self
        @param (string) name
        @param (string) description
        """
        self.name = name
        self.description = description

    def __repr__(self):
        """How the Role schema is representation when inspected."""
        return '<Role %r>' % (self.name)


def default_values(*args, **kwargs):
    """Add a default `generic` user role to the system."""
    db.session.add(Role(name="generic"))

    db.session.commit()


event.listen(Role.__table__, 'after_create', default_values)
