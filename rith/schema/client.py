"""Arithmetic Client Data Model required for OAuth.

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


class Client(db.Model):
    """Client model definition.

    Setup the client database table definition for handling OAuth
    authentication

    :param object db.Model: SQLAlchemy base declarative

    See the official Flask SQLAlchemy documetation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    application_name = db.Column(db.Text)

    client_id = db.Column(db.String, primary_key=True)
    client_secret = db.Column(db.String, nullable=False)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')

    _redirect_uris = db.Column(db.String)
    _default_scopes = db.Column(db.String)

    @property
    def client_type(self):
        """Define the default client type."""
        return 'public'

    @property
    def redirect_uris(self):
        """Define how redirect_uris are displayed."""
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        """Select default redirect_uri."""
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        """Define how scopes are displayed."""
        if self._default_scopes:
            return self._default_scopes.split()
        return []
