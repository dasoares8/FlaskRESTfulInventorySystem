from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.brand import BrandModel

class Brand(Resource):
    @jwt_required()
    def get(self, name):
        brand = BrandModel.find_brand_by_name(name)
        if(brand):
            return brand.json()
        return {'message': "A brand with the name '{}' does not exist".format(name)}, 404

    @staticmethod
    def parse_brand_data():
        parser = reqparse.RequestParser()
        parser.add_argument('manufacturer',
                            type=str,
                            required=False,
                            help="Optional"
                            )
        request_data = parser.parse_args()
        print(request_data)
        return request_data

    @jwt_required()
    def post(self, name):
        if BrandModel.find_brand_by_name(name):
            return {'message': "A brand with the name '{}' already exists".format(name)}, 400

        request_data = Brand.parse_brand_data()
        brand = BrandModel(None, name, **request_data)

        try:
            brand.add_or_update_brand()
        except:
            return {'message': "Add brand failed for '{}'".format(name)}, 500

        return brand.json(), 201

    @jwt_required()
    def put(self, name):
        request_data = Brand.parse_brand_data()
        brand = BrandModel.find_brand_by_name(name)

        if brand:
            brand.manufacturer = request_data['manufacturer']
        else:
            brand = BrandModel(None, name, **request_data)

        try:
            brand.add_or_update_brand()
        except:
            return {'message': "Add or update brand failed for '{}'".format(name)}, 500  # Internal Server Error

        return brand.json()

    @jwt_required()
    def delete(self, name):
        brand = BrandModel.find_brand_by_name(name)
        if not brand:
            return {'message': "A brand with the name '{}' does not exist".format(name)}, 400

        try:
            brand.delete_brand()
        except:
            return {'message': "Delete brand failed for '{}'".format(name)}

        return {'message': "Brand '{}' deleted".format(name)}


class Brands(Resource):
    @jwt_required()
    def get(self):
        return[brand.json() for brand in BrandModel.find_all_brands()]
