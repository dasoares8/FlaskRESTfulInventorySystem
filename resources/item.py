from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel
from models.brand import BrandModel


# Api works with resources, which are classes that inherits from Resource
# In this case Item is the resource.
class Item(Resource):
    # decorator, means we have to authenticate before calling the get method
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        # If the item doesn't exist, we need to return a response that is a dictionary for JSON
        # Also make sure we send a 404; a 200 is not accurate even though we are handling the failure case
        if(item):
            return item.json()
        return {'message': "An item with the name '{}' does not exist".format(name)}, 404

    @staticmethod
    def parse_item_data():
        # Initialize a new parser object to parse the request
        parser = reqparse.RequestParser()
        # This can look not only into JSON payloads but also into form payloads
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This field cannot be left blank"
                            )
        parser.add_argument('color',
                            type=str,
                            required=False,
                            help="Optional description field"
                            )
        parser.add_argument('brand',
                            type=str,
                            required=True,
                            help="Required field"
                            )
        # Now, go through the JSON payload, and only put the valid ones in request_data
        request_data = parser.parse_args()
        print(request_data)
        return request_data

    @jwt_required()
    def post(self, name):
        # This is a bad request, return a 400 with a message
        if(ItemModel.find_item_by_name(name)):
            return {'message': "An item with the name '{}' already exists".format(name)}, 400

        request_data = Item.parse_item_data()

        brand = BrandModel.find_brand_by_name(request_data['brand'])
        if not brand:
            return {'message': "Brand '{}' does not exist; post failed".format(request_data['brand'])}, 400

        item = ItemModel(None, name, request_data['price'], request_data['color'], brand.id)

        try:
            item.add_or_update_item()
        except:
            return {'message': "Add item failed for '{}'".format(name)}, 500 #Internal Server Error

        return item.json(), 201

    @jwt_required()
    def put(self, name):
        request_data = Item.parse_item_data()

        # Verify the brand is an already registered one.
        brand = BrandModel.find_brand_by_name(request_data['brand'])
        if not brand:
            return {'message': "Brand '{}' does not exist; put failed".format(request_data['brand'])}, 400

        item = ItemModel.find_item_by_name(name)
        # If item already exists, we need to change its values. If not, we need to send in everything to
        # create a new one.
        if item:
            item.price = request_data['price']
            item.color = request_data['color']
            item.brand_id = brand.id
        else:
            item = ItemModel(None, name, request_data['price'], request_data['color'], brand.id)

        try:
            item.add_or_update_item()
        except:
            return {'message': "Add or update item failed for '{}'".format(name)}, 500 #Internal Server Error

        return item.json()

    @jwt_required()
    def delete(self, name):
        # Need to clearly state that items is global, not a variable in the local context
        item = ItemModel.find_item_by_name(name)
        if not item: return {'message': "An item with the name '{}' does not exist".format(name)}, 400

        try:
            item.delete_item()
        except:
            return {'message': "Delete item failed for '{}'".format(name)}

        return {'message': "Item '{}' deleted".format(name)}


class Items(Resource):
    @jwt_required()
    def get(self):
        #Python List comprehension
        return[item.json() for item in ItemModel.find_all_items()]
            # A possible more generic solution, using lambda/map
            # return {'items': list(map(lambda x: x.json(), ItemModel.find_all_items()))}

