from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import User, Users
from resources.item import Item, Items
from resources.brand import Brand, Brands
from resources.threeD_inventory_slots import ThreeDInventorySlot, ThreeDInventorySlots

application = Flask(__name__)

# Determine whether running in development (SQLite) or AWS Elastic Beanstalk (MySQL) env
if __name__ == '__main__':
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
else:
    application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://soada01:acloudguru@aake81314qtwxl.cbdmvzrbabca.us-east-1.rds.amazonaws.com:3306/ebdb'

# Shuts off the Flask SQL Alchemy modification tracker, not the SQLAlchemy specific one, Flask one not needed
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# key is simple for test purposes, but if used for product, should be secret and secure (long and complicated)
application.secret_key = 'david'
api = Api(application)

@application.before_first_request
def create_tables():
    if __name__ == '__main__':
        db.create_all()

# use app, and our authenticate and identity functions
# JWT extension creates a new endpoint, /auth. When we call /auth, we send it the username and password
# JWT sends these over to the authenticate function
# once that returns, the /auth endpoint sends a jwt token. That token is sent with a payload to identity()
# To test this out, in postman, run a POST to /auth, copy the token (only)
jwt = JWT(application, authenticate, identity)


# Resource declarations
api.add_resource(Item, '/item/<int:_id>')
api.add_resource(Items, '/items')
api.add_resource(Brand, '/brand/<string:name>')
api.add_resource(Brands, '/brands')
api.add_resource(User, '/user/<string:username>')
api.add_resource(Users, '/users')
api.add_resource(ThreeDInventorySlot, '/three_dinvslot/<int:_id>')
api.add_resource(ThreeDInventorySlots, '/three_dinvslots')

# Ensure that if app is imported from elsewhere, it is not run more than once
# __main__ is the name Python assigns to the file you run
# add 'host=0.0.0.0' to app.run() for running this on remote server
if __name__ == '__main__':
    from db import db
    db.init_app(application)
    application.debug = True
    application.run()
