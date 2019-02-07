"""Arithmetic Grant Data Model required for OAuth.

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


class Grant(db.Model):
    """Grant model definition.

    The Grant databse table definition for handling OAuth authentication

    :param object db.Model: SQLAlchemy declarative base

    See the official Flask SQLAlchemy documentation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id',
                        ondelete='CASCADE'))
    user = db.relationship('User')

    client_id = db.Column(db.String, db.ForeignKey('client.client_id'),
                          nullable=False)
    client = db.relationship('Client')

    code = db.Column(db.String, index=True, nullable=False)

    redirect_uri = db.Column(db.String)
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.String)

    def delete(self):
        """Remove the Grant from the database table.

        :param object self: Grant class
        """
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        """Define how scopes are displayed."""
        if self._scopes:
            return self._scopes.split()
        return []
