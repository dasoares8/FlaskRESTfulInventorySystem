from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel
from models.brand import BrandModel


# Api works with resources, which are classes that inherits from Resource
# In this case Item is the resource.
class Item(Resource):
    # decorator, means we have to authenticate before calling the get method
    @jwt_required()
    def get(self, _id):
        item = ItemModel.find_item_by_id(_id)
        # If the item doesn't exist, we need to return a response that is a dictionary for JSON
        # Also make sure we send a 404; a 200 is not accurate even though we are handling the failure case
        if item:
            return item.json()
        return {'message': "An item with the id '{}' does not exist".format(_id)}, 404

    @staticmethod
    def parse_item_data():
        # Initialize a new parser object to parse the request
        parser = reqparse.RequestParser()
        # This can look not only into JSON payloads but also into form payloads
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help="Required field"
                            )
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
        parser.add_argument('brand_id',
                            type=int,
                            required=True,
                            help="Required field"
                            )
        # Now, go through the JSON payload, and only put the valid ones in request_data
        request_data = parser.parse_args()
        print(request_data)
        return request_data

    @jwt_required()
    def post(self, _id):
        request_data = Item.parse_item_data()

        brand = BrandModel.find_brand_by_id(request_data['brand_id'])
        if not brand:
            return {'message': "Brand id '{}' does not exist; post failed".format(request_data['brand_id'])}, 400

        item = ItemModel.find_item_by_name(brand.id, request_data['name'])
        if item:
            return {'message': "Item '{}' of Brand id '{}'  already exists; post failed".format(item.name,
                                                                                                item.brand_id)}, 400

        item = ItemModel(None, request_data['name'], request_data['price'], request_data['color'], brand.id)

        try:
            item.add_or_update_item()
        except:
            return {'message': "Add item failed for brand '{}' item '{}'".format(brand.name, item.name)}, 500
        return item.json(), 201

    @jwt_required()
    def put(self, _id):
        request_data = Item.parse_item_data()

        # Verify the brand is an already registered one.
        brand = BrandModel.find_brand_by_id(request_data['brand_id'])
        if not brand:
            return {'message': "Brand id '{}' does not exist; put failed".format(request_data['brand_id'])}, 400

        item = ItemModel.find_item_by_id(_id)
        # If item already exists, we need to change its values. If not, we need to send in everything to
        # create a new one.
        if item:
            item.name = request_data['name']
            item.price = request_data['price']
            item.color = request_data['color']
            item.brand_id = brand.id
        else:
            item = ItemModel(None, request_data['name'], request_data['price'], request_data['color'], brand.id)

        try:
            item.add_or_update_item()
        except:
            return {'message': "Add or update item failed for brand '{}' item '{}'".
                format(brand.name, item.name)}, 500

        return item.json()

    @jwt_required()
    def delete(self, _id):
        # Need to clearly state that items is global, not a variable in the local context
        item = ItemModel.find_item_by_id(_id)
        if not item: return {'message': "An item with the id '{}' does not exist".format(_id)}, 400

        try:
            item.delete_item()
        except:
            return {'message': "Delete item failed for '{}'".format(_id)}

        return {'message': "Item '{}' deleted".format(_id)}


class Items(Resource):
    @jwt_required()
    def get(self):
        #Python List comprehension
        return[item.json() for item in ItemModel.find_all_items()]
            # A possible more generic solution, using lambda/map
            # return {'items': list(map(lambda x: x.json(), ItemModel.find_all_items()))}

