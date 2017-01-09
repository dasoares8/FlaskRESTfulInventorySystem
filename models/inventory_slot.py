from db import db
from models.item import ItemModel


# Inventory slot is a superclass for a container of inventory for a particular item. It can be anywhere (warehouse,
# vending machine, store, etc.). It is expected to be abstract (i.e., no one should use it directly).
# Subclasses hold specific information to the type of slot location (its locators should be required fields).
class InventorySlotModel(db.Model):
    __tablename__ = 'inv_slot'

    # Tell SQLAlchemy what the columns are to be stored in the DB
    id = db.Column(db.Integer, primary_key=True)
    # SQLAlchemy join
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship('ItemModel')
    # impose 80 char max limit on name and color
    description = db.Column(db.String(80))
    item_count = db.Column(db.Integer)
    max_items = db.Column(db.Integer)
    # Discriminator for ORM to determine object type stored in the row
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'inv_slot',
        'polymorphic_on': type
    }

    def __init__(self, _id, description, item_id, item_count=0, max_items=0):
        self.id = _id
        self.description = description
        self.item_count = item_count
        self.max_items = max_items
        self.item_id = item_id

    def json(self):
        item = ItemModel.find_item_by_id(self.item_id)
        return {'id': self.id, 'description': self.description, 'item_id': item.id,
                'item_count': self.item_count, 'max_items': self.max_items}

    @classmethod
    def find_inv_slot_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all_inv_slots(cls):
        return cls.query.all()

    # Not a class method as it is inserting itself, which should be an object
    def add_or_update_inv_slot(self):
        db.session.add(self)
        db.session.commit()

    def remove_x_items_from_inv_slot(self, x):
        if self.item_count < x:
            return None
        self.item_count -= x
        db.session.add(self)
        db.session.commit()
        return self.item_count

    def add_x_items_to_inv_slot(self, x):
        if self.max_items:
            if self.item_count + x > self.max_items:
                return None
        self.item_count += x
        db.session.add(self)
        db.session.commit()
        return self.item_count

    def change_items_in_inv_slot(self, item_id, item_count):
        # User should update max_items (if necessary) first if adding a new item
        if item_count > self.max_items:
            return None
        self.item_id = item_id
        self.item_count = item_count
        db.session.add(self)
        db.session.commit()
        return item_id

    def change_max_items_in_inv_slot(self, max_items):
        self.max_items = max_items
        db.session.add(self)
        db.session.commit()
        return max_items

    def delete_inv_slot(self):
        db.session.delete(self)
        db.session.commit()
        return self.id
