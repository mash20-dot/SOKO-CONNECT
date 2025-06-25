from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os



app = Flask(__name__)


#database structure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sokoconnect.db'
db = SQLAlchemy(app)

class Buyer_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True,)
    password = db.Column(db.String(150),)






#signup route for buyers
@app.route('/register', methods=['POST'])
def register():
        data = request.get_json()
        firstname = data.get('fname')
        lastname = data.get('lname')
        email = data.get('email') 
        password = data.get('password')


        #checks for every empty space and save it if none of that empty space is not provided it throws that error
        Missing_fields= []

        if not firstname:
            Missing_fields.append(firstname)
        if not lastname:
            Missing_fields.append(lastname)
        if not email:
            Missing_fields.append(email)
        if not password:
            Missing_fields.append(password)
            return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400

        if (firstname and lastname and email and password):
            return jsonify({'message': 'successfully signed up'}), 201

        #Check if email already exists
        existing_user = Buyer_info.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 409
    
    

        #hash the password, making it invisible
        hashed_password = generate_password_hash(password)


        #saves user info in the database
        new_user = Buyer_info(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
   
    
        
    


#login route for buyers
@app.route('/login', methods=['POST'])
def login():

        data = ({"user":
           "firstname"
           "lastname"
           "email"
           "password"
        })

        data = request.get_json()
        firstname = data.get('fname')
        lastname = data.get('lname')
        email = data.get('email')
        password = data.get('password')


        #find a user by email 
        user = Buyer_info.query.filter_by(email=email).first()

        #If user exists and password matches
        if user and check_password_hash(user.password, password):
            return jsonify({"message": "Successfully logged in"}), 201

        if not (firstname and lastname and email and password):
            return jsonify({"message": "Invalid credentials"}), 401
    

        Missing_fields = []
        if not firstname:
            Missing_fields.append('fname')
        if not lastname:
            Missing_fields.append('lname')
        if not email:
            Missing_fields.append('email')
        if not password:
            Missing_fields.append('password')
            return jsonify({f"Missing_fields": {Missing_fields}},"fill in all blank spaces"), 400
    

    



#DATABASE FOR BUSINESS PROFILE 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///business.db'

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    business_name = db.Column(db.String(50))
    business_email = db.Column(db.String(150), unique=True,)
    phone = db.Column(db.String(150),)


#Signup form for businesses
@app.route('/business', methods=['POST'])
def business_user():
    data = request.get_json()
    business_name = data.get('business_name')
    business_email = data.get('business_email')
    phone = data.get('phone')



    Missing_fields= []

    if not business_name:
        Missing_fields.append('business_name')
    if not business_email:
        Missing_fields.append('business_email')
    if not phone:
        Missing_fields.append('phone')
        
        
    
    if Missing_fields:
        return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
     


    #saves products/items into the database
    new_business = Business(business_name=business_name, business_email=business_email, phone=phone,)
    db.session.add(new_business)
    db.session.commit()



    if (business_name and business_email and phone):
        return jsonify({'message': 'Information uploaded successfully'})
    else:
        return jsonify({'message': "Error, can't upload information"})
    
#LOGIN form for business
@app.route('/getbusiness', methods=['POST'])

def getbusiness():
     #get data from the database
     data = request.get_json()
     business_name = data.get('business_name')
     business_email = data.get('business_email')
     phone = data.get('phone')


     Missing_fields = []
     if not business_name:
            Missing_fields.append('business_name')
     if not business_email:
            Missing_fields.append('business_email')
     if not phone:
            Missing_fields.append('phone')


     if Missing_fields:
          return jsonify({f"Missing_fields", Missing_fields,"'message': fill in all blank spaces"}), 400
    
            




    #Helps to find user by email or phone
     business_user = Business.query.filter_by(
          business_email=business_email, phone=phone).first()
     
     
     #conditional statements
     if   business_user:
          return jsonify({'message': 'Information retrieved successfully'}), 201
     else:
          return jsonify({'message': 'Error, information could not be retrieved'}), 404
     
     
     
    
#PRODUCT CODE BASE
#product database structure
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///product.db'                                           

class products(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        product_name = db.Column(db.String(50))
        product_price = db.Column(db.String(50))
        product_uses = db.Column(db.String(1000))
        product_images = db.Column(db.String)

@app.route('/product', methods=['POST'])
def product():
        data = request.get_json()
        product_name = data.get('product_name')
        product_price = data.get('product_price')
        product_uses = data.get('product_uses')
        product_images = data.get('product_images')

        Missing_fields= []

        if not product_name:
            Missing_fields.append('product_name')
        if not product_price:
            Missing_fields.append('product_price')
        if not product_uses:
            Missing_fields.append('product_uses')
        if not product_images:
            Missing_fields.append('product_images')
            

        if Missing_fields:
             return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400

        
       #saves products/items into the database
        new_product = products(product_name=product_name, product_price=product_price, product_uses=product_uses, product_images=product_images)
        db.session.add(new_product)
        db.session.commit()

        
             
       
        if product:
             return jsonify({'message': 'Item updated successfully '}), 201
        
        
        if not product:
             return jsonify({'message': 'Error item not updated'}), 400

        
        
        
#ROUTE FOR GETTING ITEMS FROM THE DATABASE
@app.route('/getproduct', methods=['GET'])
def getproduct():
     
    data = request.get_json()
    product_name = data.get('product_name')
    product_price = data.get('product_price')
    product_uses = data.get('product_uses')
    product_images = data.get('product_images')

    
    
    Missing_fields= []

    if not product_name:
            Missing_fields.append('product_name')
    if not product_price:
            Missing_fields.append('product_price')
    if not product_uses:
            Missing_fields.append('product_uses')
    if not product_images:
            Missing_fields.append('product_images')



    if Missing_fields:
        return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400

        
   

    if product:
         return jsonify({'message': 'items retrieved successfully'}), 201
    if not product:
         return jsonify({'message': 'could not retrieve item'}), 400

    

    
#this allows sqlalchemy to find data and create data according to your db.Model
with app.app_context():
    db.create_all()

(__name__) == ('__main__')
app.run(debug=True)
