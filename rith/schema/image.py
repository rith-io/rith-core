"""Arithmetic Image Data Model Class.

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


from rith.schema.base import BaseMixin


class Image(BaseMixin):
    """Image schema definition.

    The `Image` database table definition

    :param object db.Model: SQLAlchemy declarative base

    See the official Flask SQLAlchemy documentation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    __tablename__ = 'image'
    __table_args__ = {
        'extend_existing': True
    }

    original = db.Column(db.String)

    square_retina = db.Column(db.String)
    square = db.Column(db.String)

    thumbnail_retina = db.Column(db.String)
    thumbnail = db.Column(db.String)

    icon_retina = db.Column(db.String)
    icon = db.Column(db.String)

    filename = db.Column(db.String)
    filetype = db.Column(db.String)
    filesize = db.Column(db.String)

    caption = db.Column(db.String)
    caption_link = db.Column(db.String)
