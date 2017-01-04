import sqlite3
from db import db

class BrandModel(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    manufacturer = db.Column(db.String(80))

    def __init__(self, _id, name, manufacturer):
        self.id = _id
        self.name = name
        self.manufacturer = manufacturer

    def json(self):
        return {'name': self.name, "manufacturer": self.manufacturer}

    @classmethod
    def find_all_brands(cls):
        return cls.query.all()

    @classmethod
    def find_brand_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_brand_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def add_or_update_brand(self):
        db.session.add(self)
        db.session.commit()

    def delete_brand(self):
        db.session.delete(self)
        db.session.commit()
