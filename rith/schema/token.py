"""Arithmetic Token Data Model required for OAuth.

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


from rith import db


from rith.schema.user import User


class Token(db.Model):
    """Token database definition.

    :param object db.Model: SQLAlchemy declarative base

    See the official Flask SQLAlchemy documentation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    __tablename__ = 'token'
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.String, db.ForeignKey('client.client_id'),
                          nullable=False)
    client = db.relationship('Client')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

    token_type = db.Column(db.String)

    access_token = db.Column(db.String, unique=True)
    refresh_token = db.Column(db.String, unique=True)

    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.String)

    @property
    def scopes(self):
        """Define how scopes should be displayed."""
        if self._scopes:
            return self._scopes.split()
        return []
