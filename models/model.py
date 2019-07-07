from pymongo import MongoClient
from bson.objectid import ObjectId #MongoDB Specific

client = MongoClient()
db = client['amazon']

def create_user(username,password1,typev):#To create an new user
	db["users"].insert({"username" :username ,"password" : password1, "type" : typev})
	return "Created User"

def existing_user(username):# To say that already an user exists in this USERNAME
	if db.users.find_one({"username" : username})!=None:
		return True
	else:
		return False

def check_user(username,password):#Checks the user with the registered Username and Password or not
	a = db.users.find_one({"username" : username})# Used for login part
	print(a)
	if a != None:
		if a["password"]==password:
			return True
		else:
			return False
	else:
		return False

def get_type(username):#To determine the function as seller or buyer
	b = db.users.find_one({"username" : username})
	return b["type"]

def create_product(product_name,price,description,seller):#To create product from seller part
	db["products"].insert({"product_name" : product_name , "price" : price , "description" : description , "seller" : seller})
	return "Product Created"

def get_products():#Lists the Products which Seller have created
	a = db.products.find({})
	product_list = [x for x in a] 
	print(product_list)
	return product_list

def remove_products(product_name):#Removes the products which Seller wants to remove
	a = db.products.remove({"product_name" : product_name})
	print(a)
	return "Product Removed"

def update_cart(id,username):#Buyer cart gets updated for the added items to cart
	userinfo = db.users.find_one({"username" : username})
	if "cart" in userinfo:
		cart = userinfo["cart"]
	else:
		cart = {}	
	if id in cart:
		cart[id]+=1
	else:	
		cart[id] = 1
	a = db.users.update({"username" : username},{'$set' : {"cart" : cart}})
	print (a)
	return "Added to cart"

def get_cart(username):#Returns the cart of the Buyer
	b = db.users.find_one({"username" : username})
	return b["cart"]

def get_product_info(idv):#Returns the information of the product from id used by buyer
	print(idv)
	a = db.products.find_one({"_id" : ObjectId(idv)})#Query(find out) - _id = Key ; ObjectId(id) = Value
	return a

def remove_from_cart(product_id , username):#Removes the products which Buyer wants to remove
	userinfo = db.users.find_one({"username" : username})
	if "cart" in userinfo:
		cart = userinfo["cart"]
	else:
		cart = {}	
	print(cart, product_id, type(product_id))
	if product_id in cart and cart[product_id]!=0:
		cart[product_id]-=1	
	a = db.users.update({"username" : username} , {'$set' : {"cart" : cart}})
	print(a)
	return "Product removed from the cart"

