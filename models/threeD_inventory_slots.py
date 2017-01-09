from db import db
from models.inventory_slot import InventorySlotModel


# 3DInventory slot is a subclass of InventorySlot for a container of inventory within a 3D (or less) system.
# It would be anything with X/Y coordinates with also a 3rd dimension, for example:
#   A large warehouse with rows of X/Y shelving
#   A set of vending machines (which naturally have X/Y coordinates for products)
# We are using simple Single Table Inheritance for mapping the class inheritance hierarchy in SQLAlchemy,
# hence no table is specified for the subclass
class three_dInventorySlotModel(InventorySlotModel):
    __mapper_args__ = {
        'polymorphic_identity': 'three_d_inv_slot'
    }
    # Indexes are integer locations, descrs are human-readable locations. Indexes could be useful
    # for automation purposes; i.e. warehouse robots using distance algorithms
#    x_loc_index = db.Column(db.Integer)
#    y_loc_index = db.Column(db.Integer)
#    z_loc_index = db.Column(db.Integer)
    x_loc_descr = db.Column(db.String(10))
    y_loc_descr = db.Column(db.String(10))
    z_loc_descr = db.Column(db.String(10))

    def __init__(self, _id, description, item_id, x_loc_descr, y_loc_descr, z_loc_descr,
                 item_count=0, max_items=0):
        super().__init__(_id, description, item_id, item_count, max_items)
#        self.x_loc_index = x_loc_index
#        self.y_loc_index = y_loc_index
#        self.z_loc_index = z_loc_index
        self.x_loc_descr = x_loc_descr
        self.y_loc_descr = y_loc_descr
        self.z_loc_descr = z_loc_descr

    def json(self):
        three_d_fields = {'X_location': self.x_loc_descr, 'Y_location': self.y_loc_descr,
                          'Z_location': self.z_loc_descr}
        return dict(super(three_dInventorySlotModel, self).json(), **three_d_fields)

    # May use this later
    # @classmethod
    # def find_all_inv_slots(cls):
    #    return cls.query.all()

    @classmethod
    def find_three_d_inv_slot(cls, x_loc_descr, y_loc_descr, z_loc_descr):
        return cls.query.filter_by(x_loc_descr=x_loc_descr, y_loc_descr=y_loc_descr, z_loc_descr=z_loc_descr).first()

    def add_or_update_three_d_inv_slot(self):
        db.session.add(self)
        db.session.commit()

    def delete_three_d_inv_slot(self):
        db.session.delete(self)
        db.session.commit()
