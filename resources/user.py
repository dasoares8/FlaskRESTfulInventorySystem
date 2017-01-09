from models.user import UserModel
from flask_restful import Resource, reqparse

class User(Resource):
    @staticmethod
    def parse_user_data():
        parser = reqparse.RequestParser()
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be left blank"
                            )

        request_data = parser.parse_args()
        return request_data

    def get(self, username):
        user = UserModel.find_user_by_username(username)
        if user:
            return user.json()
        return {'message': "A user with the username '{}' does not exist".format(username)}, 404

    def post(self, username):
        user = UserModel.find_user_by_username(username)
        if user:
            return {'message': "A user with the username '{}' already exists".format(username)}, 400
        request_data = User.parse_user_data()
        user = UserModel(None, username, request_data['password'])
        try:
            user.add_or_update_user()
        except:
            return {'message': "User '{}' failed to be added".format(username)}, 500

        return user.json(), 201

    def put(self, username):
        request_data = User.parse_user_data()
        user = UserModel.find_user_by_username(username)

        if user:
            user.password = request_data['password']
        else:
            user = UserModel(None, username, **request_data)

        try:
            user.add_or_update_user()
        except:
            return {'message': "User '{}' failed to be added".format(username)}, 500

        return {'message': "Added or updated user '{}'".format(username)}

    def delete(self, username):
        user = UserModel.find_user_by_username(username)
        if not user: return {'message': "A user with the username '{}' does not exist".format(username)}, 400

        try:
            user.delete_user()
        except:
            return {'message': "User '{}' failed to be deleted".format(username)}, 500

        return {'message': "User '{}' has been deleted".format(username)}


class Users(Resource):
    def get(self):
        return [user.json() for user in UserModel.find_all_users()]
