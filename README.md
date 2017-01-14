# FlaskRESTfulInventorySystem
Inventory System in Python using Flask RESTful

## Description
This is an inventory system. Its components include:
  - Users: simple users system, uses JWT for identity/authorization
  - Brands: Brands that help identify items
  - Items: inventory items, includes a brand for id. For example Lay's Potato Chips, or Utz Pretzels.
  - Inventory Slots: A location of inventory of a specific item.
	- 3D Inventory Slot: Subclass for slots that can be identified in an X/Y/Z location grid. Examples are:
		- Vending Machine (only 2D, other identifier can be for the vending machine itself)
		- Warehouse (similar to Amazon-type warehouse)

##Implementation
This is code that demonstrates
  - Usage of a REST API using Flask RESTful
  - Usage of SQAlchemy as an ORM (vs. using direct SQL)
  - Usage of FlaskJWT for authorization
  - General Python3 OO coding, including inheritance

## Prerequisites:
Written on Python 3.4.3. Your virtual environment will require the following :
  - FlaskRESTful
  - FlaskJWT
  - Flask-SQLAlchemy
All other necessary packages will come from those. See requirements.txt in the main directory for a comprehensive list.
  
## To run the code:
in the main directory at the prompt, type "python application.py"
To do anything other than CRUD users, you'll need to refresh the JWT token for the respective user. This is done with
a POST to /auth, with username/password in the POST body.

## Amazon AWS Elastic Beanstalk implementation
I am currently running this on AWS ELB. If it's up, you can test it there. The URL there is:
http://inv-system.n9n92pezny.us-east-1.elasticbeanstalk.com
For example, you wanted a list of all the users, you would enter:
http://inv-system.n9n92pezny.us-east-1.elasticbeanstalk.com/users (I have yet to implement an administrative user, TBD)
This implementation uses MySQL on AWS RDS rather than the development SQLite. The code automatically detects
whether it is running from application.py (development) or WSGI (ELB)

TOD0: I have yet to figure out how to allow for JWT tokens to pass through AWS. I need to alter the wsgi.conf
file manually with "WSGIPassAuthorization On" then restart the httpd service to get it to work. This will likely
need to be done with a .ebextensions command and a sed script on the server.

I have used Postman for REST API testing (will post the code for that soon).
This has been developed using JetBrains PyCharm Community Edition. 


