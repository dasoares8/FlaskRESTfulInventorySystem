from db import db
from models.brand import BrandModel


# extend class from db.Model for SQLAlchemy
class ItemModel(db.Model):
    __tablename__ = 'items'

    # Tell SQLAlchemy what the columns are to be stored in the DB
    id = db.Column(db.Integer, primary_key=True)
    # impose 80 char max limit on name and color
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    color = db.Column(db.String(80))

    # SQLAlchemy join
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    brand = db.relationship('BrandModel')

    # using _id instead of "id" itself as id is a Python keyword
    def __init__(self, _id, name, price, color, brand_id):
        self.id = _id
        self.name = name
        self.price = price
        self.color = color
        self.brand_id = brand_id

    def json(self):
        brand = BrandModel.find_brand_by_id(self.brand_id)
        return {'id': self.id, 'name': self.name, 'price': self.price, 'color': self.color, 'brand': brand.name}

    @classmethod
    def find_all_items(cls):
        return cls.query.all()

    # A class method as it should return an ItemModel-based object
    @classmethod
    def find_item_by_name(cls, brand_id, name):
        # Return ItemModel object (cls) by running a query through SQLAlchemy. .first() extension is just like
        # SQL's "LIMIT 1"
        return cls.query.filter_by(brand_id=brand_id, name=name).first()

    @classmethod
    def find_item_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # Not a class method as it is inserting itself, which should be an object
    def add_or_update_item(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
