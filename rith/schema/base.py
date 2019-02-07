"""Arithmetic Base Data Model Class.

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


from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.collections import InstrumentedList


class BaseMixin(db.Model):

    __abstract__  = True

    """Feature Identifier."""
    id = db.Column(db.Integer, primary_key=True)

    """Feature Statuses."""
    has_been_archived = db.Column(db.Boolean)
    has_been_deleted = db.Column(db.Boolean)

    """Feature Timestamps."""
    created_on = db.Column(db.DateTime)
    modified_on = db.Column(db.DateTime)

    """Define attributes that create relationships for us.

    :see: For more documentation on usage of declarative attributes see the
          official SQLAlchemy documentation at:

          http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/
            api.html#sqlalchemy.ext.declarative.declared_attr
    """

    """Feature User Association."""
    @declared_attr
    def creator_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    @declared_attr
    def created_by(cls):
        return db.relationship('User', **{
            'foreign_keys': cls.creator_id,
            'uselist': False
        })

    """Feature Modified by User Association."""
    @declared_attr
    def last_modified_by_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    @declared_attr
    def last_modified_by(cls):
        return db.relationship('User', **{
            'foreign_keys': cls.last_modified_by_id,
            'uselist': False
        })

    def get_related_data_values(self, objects_, field_):

        list_ = []

        #
        # Make sure our relationship is a list
        #
        if type(objects_) == InstrumentedList or type(objects_) == "list":
            for object_ in objects_:
                list_.append({
                    "id": object_.__dict__["id"],
                    "name": object_.__dict__[field_] if object_.__dict__[field_] else "Unnamed"
                })
        else:
            if hasattr(objects_, '__dict__'):
                list_.append({
                    "id": objects_.__dict__["id"],
                    "name": objects_.__dict__[field_] if objects_.__dict__[field_] else "Unnamed"
                })

        return list_

    def related_data(self):

        list_ = []

        for relationship_ in self.__def__["relationships"]:

            if hasattr(self, relationship_.get('name')):

                field_ = relationship_.get('label_field_name')
                values_ = self.__dict__[relationship_.get('name')]
                items_ = self.get_related_data_values(values_, field_)

                r_ = {
                    "type": relationship_.get('machine_name'),
                    "label": relationship_.get('class_name'),
                    "count": len(items_),
                    "list": items_
                }

                list_.append(r_)

        return list_
