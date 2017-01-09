from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel
from models.threeD_inventory_slots import three_dInventorySlotModel


# Api works with resources, which are classes that inherits from Resource
# In this case Item is the resource.
class ThreeDInventorySlot(Resource):
    @jwt_required()
    def get(self, _id):
        three_d_inv_slot = three_dInventorySlotModel.find_inv_slot_by_id(_id)
        if three_d_inv_slot:
            return three_d_inv_slot.json()
        return {'message': "This three_d inventory slot id '{}' does not exist".format(_id)}, 404

    @staticmethod
    def parse_item_data():
        # Initialize a new parser object to parse the request
        parser = reqparse.RequestParser()
        # This can look not only into JSON payloads but also into form payloads
        parser.add_argument('description',
                            type=str,
                            required=False,
                            help="Optional description field"
                            )
        parser.add_argument('item_id',
                            type=str,
                            required=False,
                            help="Required if there are items in the slot"
                            )
        parser.add_argument('x_loc_descr',
                            type=str,
                            required=True,
                            help="Required field"
                            )
        parser.add_argument('y_loc_descr',
                            type=str,
                            required=True,
                            help="Required field"
                            )
        parser.add_argument('z_loc_descr',
                            type=str,
                            required=True,
                            help="Required field"
                            )
        parser.add_argument('item_count',
                            type=int,
                            required=False,
                            help="Required if there are items in the slot"
                            )
        parser.add_argument('max_items',
                            type=int,
                            required=False,
                            help="Optional field to provide a slot limit"
                            )

        request_data = parser.parse_args()
        print(request_data)
        return request_data

    @jwt_required()
    def post(self, _id):
        if three_dInventorySlotModel.find_inv_slot_by_id(_id):
            return {'message': "This slot id '{}' already exists".format(_id)}, 400

        request_data = ThreeDInventorySlot.parse_item_data()
        # Check the referential integrity of the item_id if passed
        if request_data['item_id']:
            item = ItemModel.find_item_by_id(request_data['item_id'])
        else:
            return {'message': "No item_id was provided; post failed"}, 400

        if not item:
                return {'message': "Item id '{}' does not exist; post failed".format(request_data['item_id'])}, 400

        three_dInvSlot = three_dInventorySlotModel(None, request_data['description'],
                                                   item.id, request_data['x_loc_descr'],
                                                   request_data['y_loc_descr'], request_data['z_loc_descr'],
                                                   request_data['item_count'], request_data['max_items'])

        try:
            three_dInvSlot.add_or_update_three_d_inv_slot()
        except:
            return {'message': "Add three_d_inv_slot failed for id '{}'".format(_id)}, 500

        return three_dInvSlot.json(), 201

    @jwt_required()
    def put(self, _id):
        request_data = ThreeDInventorySlot.parse_item_data()
        if request_data['item_id']:
            item = ItemModel.find_item_by_id(request_data['item_id'])
        else:
            return {'message': "No item_id was provided; put failed"}, 400

        if not item:
            return {'message': "Item id '{}' does not exist; put failed".format(request_data['item_id'])}, 400

        three_dInvSlot = three_dInventorySlotModel.find_inv_slot_by_id(_id)
        if three_dInvSlot:
            three_dInvSlot.description = request_data['description']
            three_dInvSlot.item_id = item.id
            three_dInvSlot.x_loc_descr = request_data['x_loc_descr']
            three_dInvSlot.y_loc_descr = request_data['y_loc_descr']
            three_dInvSlot.z_loc_descr = request_data['z_loc_descr']
            three_dInvSlot.item_count = request_data['item_count']
            three_dInvSlot.max_items = request_data['max_items']
        else:
            three_dInvSlot = three_dInventorySlotModel(None, request_data['description'], item.id,
                                                       request_data['x_loc_descr'], request_data['y_loc_descr'],
                                                       request_data['z_loc_descr'], request_data['item_count'],
                                                       request_data['max_items'])

        try:
            three_dInvSlot.add_or_update_inv_slot()
        except:
            return {'message': "PUT three_d_inv_slot failed for '{}'".format(_id)}, 500  # Internal Server Error

        return three_dInvSlot.json()

    @jwt_required()
    def delete(self, _id):
        three_dInvSlot = three_dInventorySlotModel.find_inv_slot_by_id(_id)
        if not three_dInvSlot:
            return {'message': "A three_d_inv_slot with the id '{}' does not exist".format(_id)}, 400

        try:
            three_dInvSlot.delete_inv_slot()
        except:
            return {'message': "Delete three_d_inv_slot failed for id '{}'".format(_id)}

        return {'message': "three_d_inv_slot id '{}' deleted".format(_id)}


class ThreeDInventorySlots(Resource):
    @jwt_required()
    def get(self):
        return[three_dInvSlot.json() for three_dInvSlot in three_dInventorySlotModel.find_all_inv_slots()]
