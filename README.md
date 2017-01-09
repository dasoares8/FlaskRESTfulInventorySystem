# FlaskRESTfulInventorySystem
Inventory System in Python using Flask RESTful

## Description
This is an inventory system. Its components include:
  - Users: simple users system, uses JWT for identity/authorization
  - Items: inventory items, includes a brand for id. For example Lay's Potato Chips, or Utz Pretzels.
  - Brands: Brands that help identify items
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
  
I have used Postman for REST API testing (will post the code for that soon). 
This has been developed using JetBrains PyCharm Community Edition. 
