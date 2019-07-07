from flask import Flask,render_template,request,url_for,redirect,session,jsonify
from models.model import create_user, existing_user,check_user,get_type,create_product,get_products,remove_products,update_cart,get_cart,get_product_info,remove_from_cart


app = Flask(__name__)#
app.secret_key = 'hello'

# Geneal Web Displaying Page
@app.route('/')
def home():
	print("Welcome to My Amazon")
	return render_template("home.html")

@app.route('/about')
def about():
	print("MyAmazon was created for e-commerce shopping")
	return render_template("about.html")

@app.route('/contact')
def contact():
	print("/n Contact Number: 99090 09099")
	print("/n Address : 120 Ambit IT Park")
	return render_template("contact.html")

#General Web Displaying Page

#User Creating Account
@app.route('/signup',methods = ['POST'])
def signup():
	
	if request.method == 'POST': #req.method -
		username = request.form["username"] # request.form - is a dictionary for storing the information from POST 
		password1 = request.form["password1"]
		password2 = request.form["password2"]
		typev = request.form["type"]
		print(username,password1,typev)
		if(existing_user(username)):
			return "User already exists"	
		create_user(username, password1, typev)
		session["username"] = username
		session["type"] = typev
		return redirect(url_for('home'))


#Loging in 
@app.route('/login',methods = ['POST'])
def login():

	if request.method == 'POST':
		print(request.form["username"],request.form["password"])
		if check_user(request.form["username"],request.form["password"]) == True:
			username = request.form["username"]
			#c = get_type(username)
			session["username"] = username #Session - Cookie for storing the information b/w requests from a single user
			session["type"]= get_type(username)
			return redirect(url_for('home'))

		else:
			return "Invalid Credentials"

#Adding Products as Seller

@app.route('/products',methods = ['POST','GET'])
def products():

	if request.method == 'POST':
		product_name = request.form["product_name"]
		price = request.form["price"]
		description = request.form["description"]
		seller = session["username"]
		print(product_name,price,description,seller)
		create_product(product_name,price,description,seller)
		return redirect(url_for('home'))
	else:
		return render_template("products.html",products = get_products())

#Removing Products as Seller
@app.route('/remove_product' , methods = ['POST'])
def rmv_products():
	if request.method == 'POST':
		product_name = request.form["name"]
		b = remove_products(product_name)
		return redirect(url_for('products'))

#Adding products to cart as Buyer
@app.route('/cart' , methods = ['POST' , 'GET'])
def add_to_cart():
	if request.method == 'POST':
		id = request.form["id"]
		username = session["username"]
		c = update_cart(id,username)
		return render_template("products.html",products = get_products())
	else:
		cart_list = []
		username = session["username"]
		cart = get_cart(username) 
		if cart != None:
			for idv in cart:
				print(idv)
				a = get_product_info(idv)
				if idv in cart:
					a["count"] = cart[idv]
				else:
					a["count"] = 0	
				cart_list.append(a)
				print(a)
			return render_template("cart.html" , cart = cart_list)

#Buyer removing products from cart
@app.route('/remove_cart' , methods = ['POST'])
def rmv_from_cart():
	if request.method == 'POST':
		print(request.form)
		product_id = request.form["product_id"]
		c = remove_from_cart(product_id , session["username"])
		return redirect(url_for('add_to_cart'))

#Logout for Buyer and seller
@app.route('/logout',methods = ['GET'])
def logout():		
	session.clear()
	return redirect(url_for('home'))

app.run(debug=True)#Start running this file as server