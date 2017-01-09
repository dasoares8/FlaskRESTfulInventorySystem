from models.user import UserModel
# safe_str_cmp allows for the same syntax to be used whether in Py2 or Py3
from werkzeug.security import safe_str_cmp


# Function to authenticate a user
def authenticate(username, password):
    user = UserModel.find_user_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


# identity() function is unique to Flask JWT
# payload is the contents of the JWT token
# extract the user_id from that payload, then do the lookup
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_user_by_id(user_id)
