from application import application
from db import db

# This file is needed for running the app using WSGI (Heroku or AWS Elastic Beanstalk)

db.init_app(application)

# Use a Flask decorator, do this before anything else the app does
@application.before_first_request
def create_tables():
    db.create_all()