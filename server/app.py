from datetime import datetime
from datetime import timedelta
from datetime import timezone


from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt

#importing key from dotenv
from dotenv import load_dotenv
import os
load_dotenv()



app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-default-secret')

# Seting up the Flask-JWT-Extended extension
app.config
jwt = JWTManager(app)

# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=60))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
      #return response if jwt is invalid
        return response




#database structure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sokoconnect.db'
db = SQLAlchemy(app)

class Buyer_user(db.Model):
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
#THE PROBLEM IS WITH THE MISSING FIELDS
          Missing_fields = []
          #if not firstname:
               #Missing_fields.append('firstname')
          #if not lastname:
               #Missing_fields.append('lastname')
          if not email:
               Missing_fields.append('email')
          if not password:
               Missing_fields.append('password')
            
          if Missing_fields:   
           return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
        
        
          #Check if email already exists
          existing_user = Buyer_user.query.filter_by(email=email).first()
          if existing_user:
               return jsonify({"message": "Email already exists"}), 400
        
          #hash the password, making it invisible
          hashed_password = generate_password_hash(password)

          #saves user info in the database
          new_user = Buyer_user(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
          db.session.add(new_user)
          db.session.commit()
          return jsonify({'message': 'Account created successfuly'}), 201


#THIS LOGIN ROUTE IS WORKING PERFECTLY DONT TOUCH IT
#login route for buyers
@app.route('/login', methods=['POST'])
def login():
       
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        #find a user by email 
        user = Buyer_user.query.filter_by(email=email).first()

        if not user:
             return jsonify({'message': 'User not found'}), 400
        
        
        response = jsonify({'msg': 'logged in successful'})
        #create an access token for the user to verify their identity when visiting a protected route
        access_token = create_access_token(identity="email and password")
        set_access_cookies(response, access_token)
        return response
     


        #Route for logout
@app.route('/logout', methods=['POST'])
def logout():
     response = jsonify({"msg": "logout successful"})
     #this removes the jwt cookies from the user's browser, enbling them to log out
     unset_jwt_cookies(response)
     return response



#DATABASE FOR BUSINESS PROFILE 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///business.db'

class Business_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    business_name = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True,)
    phone = db.Column(db.String(150),)
    password = db.Column(db.String(150),)


#Signup form for businesses
@app.route('/business', methods=['POST'])
def business_user():
    data = request.get_json()
    business_name = data.get('business_name')
    email = data.get('business_email')
    phone = data.get('phone')
    password = data.get('password')

    #PROBLEM IN THIS ROUTE IS EVEN IF ITS TRUE THE SUCCESSFUL MESSAGE DOES NOT RUN 
    Missing_fields= []

    if not business_name:
        Missing_fields.append('business_name')
    if not email:
        Missing_fields.append('email')
    if not phone:
        Missing_fields.append('phone')
    if not password:
        Missing_fields.append('password')
        #if all fields are provided, it creates an access token
        return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
    
    #Check if email already exists
    existing_user = Business_user.query.filter_by(email=email).first()
    if existing_user:
          return jsonify({"message": "Email already exists"}), 400
    
    #hash the password, making it invisible
    hashed_password = generate_password_hash(password)


    #saves products/items into the database
    new_business = Business_user(business_name=business_name, email=email, phone=phone, password=password)
    db.session.add(new_business)
    db.session.commit()
    return jsonify({'message': 'Account created successfuly'}),201

    
    if Business_user:
            return jsonify({"message": "Account created successfuly"}), 201
    else:
            return jsonify({"message": "Account could not be created"}), 400

            
            
     
#LOGIN form for business
@app.route('/getbusiness', methods=['POST'])
def getbusiness():
     #get data from the database
     data = request.get_json()
     business_name = data.get('business_name')
     email = data.get('email')
     phone = data.get('phone')
     password = data.get('password')


     #Helps to find user by email or phone
     business_user = Business_user.query.filter_by(email=email, phone=phone).first()
     
     response = jsonify({"msg": "login successful"})
     #create an access token for the user
     #this access token is used to authenticate the user in subsequent requests
     if not business_user:
          return jsonify({"message": "Business not found"}), 404
     access_token = create_access_token(identity=email and business_name and phone and password)
     set_access_cookies(response, access_token)
     return response
     

     




    
     
   
     
     
    
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


        Missing_fields= []

        if not product_name:
            Missing_fields.append('product_name')
        if not product_price:
            Missing_fields.append('product_price')
        if not product_uses:
            Missing_fields.append('product_uses')
    
            

        if Missing_fields:
             return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400

        
       #saves products/items into the database
        new_product = products(product_name=product_name, product_price=product_price, product_uses=product_uses)
        db.session.add(new_product)
        db.session.commit()

        
             
       
        if product:
             return jsonify({'message': 'Item updated successfully '}), 201
        
        
        if not product:
             return jsonify({'message': 'Error item not updated'}), 400

        
        
        
#ROUTE FOR GETTING ITEMS FROM THE DATABASE
@app.route('/getproduct', methods=['GET'])
def getproduct():
     
    data = request.args
    product_name = request.args.get('product_name')
    product_price = request.args.get('product_price')
    product_uses = request.args.get('product_uses')

    
    
    Missing_fields= []

    if not product_name:
            Missing_fields.append('product_name')
    if not product_price:
            Missing_fields.append('product_price')
    if not product_uses:
            Missing_fields.append('product_uses')



    if Missing_fields:
        return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400

    #not working yet have to fix it    
    #if product in products:
         #return jsonify({'message': 'product already uploaded'})
    #product = products.query.filter_by(product_name=product_name).first()

    if product:
         return jsonify({'message': 'items retrieved successfully',
                         'product_name':product_name,
                         'product_price':product_price,
                         'product_uses':product_uses
                         
    }), 200
    if not product:
         return jsonify({'message': 'could not retrieve item'}), 400
    
    
    



#A form a buyer will fill whiles contacting or buying a product, this will go into the business owner histoy

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///contact.db'                                           
class History(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        buyer_name = db.Column(db.String(50))
        buyer_product = db.Column(db.String(50))
        date = db.Column(db.String(30))


@app.route('/history', methods=['POST'])
def history():
        data = request.get_json()
        buyer_name = data.get('buyer_name')
        buyer_product = data.get('buyer_product')
        date = data.get('date')

        #stores a blank field and if not field throws an error
        Missing_fields = []
        if not buyer_name:
             Missing_fields('buyer_name')
        if not buyer_product:
             Missing_fields('buyer_product')
        if not date:
             Missing_fields('data')

        if Missing_fields:
            return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400
        
        if History:
             return jsonify({'message': 'history stored successfuly'}), 201
        else:
             return jsonify({'message': 'Error, could not update history'}), 400



@app.route('/gethistory', methods=['GET'])
def gethistory():
     
     data = request.args
     buyer_name = request.args.get('buyer_name')
     buyer_product = request.args.get('buyer_product')
     date = request.args.get('date')
     

     #stores a blank field and if not field throws an error
     Missing_fields = []
     if not buyer_name:
          Missing_fields('buyer_name')
     if not buyer_product:
          Missing_fields('buyer_product')
     if not date:
          Missing_fields('date')

     if Missing_fields:
          return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400
     
    
    
     #Filters the history with buyer_name
     history = History.query.filter_by(buyer_name=buyer_name).first()
     if History:
          return jsonify({  'message': 'Data retrieved',
                            'buyer_name': buyer_name,
                            'buyer_product': buyer_product,
                            'date': data
                                 
     }), 200
     else:
          return jsonify({'message': 'Error, could not retrieve history'}), 400
     




#Route for buyer logout
@app.route('/logdel', methods=['DELETE'])
def logdel():
     data = request.data.delete
     Buyer_info = data.delete('fname')

     Missing_fields = []

     if not Buyer_info:
          Missing_fields.append('Buyer_info')
          return jsonify({Missing_fields, 'missing_fields'})
          

     if Missing_fields:
          return jsonify({Missing_fields: 'missing_fields'})



     #if Buyer_info:
          #return ('message': 'Account deleted successfuly'), 201
     #else:
          #return ('message': ' Account could not delete'), 400




#Database for messages
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///Messages.db'                                           
class Message(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        text = db.Column(db.String)

#Route for messages
@app.route('/message', methods=['POST'])
def message():
     data = request.post_json()
     text = data.post('text')

     Missing_fields = []
     if not text:
          Missing_fields.append('text')

     if Missing_fields:
          return jsonify({Missing_fields, 'Missing_fields'})                            
                                                           
     if text:
          return jsonify({'message': 'message sent'})
     if not text:
          return jsonify({'message': 'Enter a text'})




#route for updating buyer credentials                      
@app.route('/update', methods=['UPDATE'])
def update():                          
     data = request.update_json()
     Buyer_info = data.update('Buyer_info')

     Missing_fields= []

     if not Buyer_info:
          Missing_fields.append('Buyer_info')
          return jsonify({"Error": f"Missing_fields: {Missing_fields}"})
     
     if Buyer_info:
          return jsonify({'message': 'credentials updated successfully'})
     
     if not Buyer_info:
          return jsonify({'message': 'credentials not found'})
     



#Route for businesses to update their credentials
@app.route('/business_updates', methods=['POST'])
def business_updates():
     data = request.post_json()
     Business = data.post('Business')

     Missing_fields = []
     if not Business:
          return Missing_fields.append('Business')
     
     if Missing_fields:
          return jsonify({Missing_fields, 'missing_fields'})
     
     if Business:
          return jsonify({'message': 'credentials updated successfuly'}), 201
     if not Business:
          return jsonify({'message': 'credentials can not be updated'})
     



#Route for business owner to logout
@app.route('/business_logout', methods=['DELETE'])
def business_logout():
     data = request.delete_json()
     Business = data.delete('Business')

     Missing_fields = []
     if not Business:
          Missing_fields.append('Business')

     if Missing_fields:
          return ({Missing_fields, 'missing_fields'})
     

     if Business:
          return  jsonify({'message': 'logged out successfuly'}), 201
     else:
          return jsonify({'message': 'could not log out try again'}), 400
     


#Route for business owners to delete their account
@app.route('/business_delete', methods=['POST'])
def business_delete():
     data = request.delete_json()
     Business = data.delete('Business')

     Missing_fields = []
     if not Business:
          Missing_fields.append('Business')

     if Missing_fields:
          return jsonify({Missing_fields, 'missing_fields'})
     
     if Business:
          return jsonify({'message': 'Account deleted successfuly'}), 201
     else:
          return jsonify({'message': 'Account could not be deleted'}), 400
     



#Admin data structure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sokoconnect.db'
#db = SQLAlchemy(app)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    Full_name = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True,)
    password = db.Column(db.String(150),)



#Route for admins to create account
@app.route('/Admin_Route', methods=['POST'])
def admin():
     data = request.get_json()
     Full_name = data.get('Full_name')
     email = data.get('email')
     password = data.get('password')

     Missing_fields = []
     if not Full_name:
          Missing_fields('Full_name')
     if not email:
          Missing_fields('email')
     if not password:
          Missing_fields('Password')
          return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
     

     if (Full_name and email and password):
          return jsonify({'message': 'Account created successfuly'}), 201
     if (Full_name and email and password):
          return jsonify({'message': 'Account could not be created'}),400
     

@app.route('/adminlogin', methods=['POST'])
def adminlogin():
     data = request.get_json()
     Full_name = data.get('Full_name')
     email = data.get('email')
     password = data.get('password')


     Missing_fields = []
     if not Full_name:
          Missing_fields('Full_name')
     if not email:   
          Missing_fields('email')
     if not password:
          Missing_fields('Password')
          return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
     
     if Admin:
          return jsonify({'message': 'logged in sucessfuly'}), 201
     if not Admin:
          return jsonify({'message': 'could not login'}), 400
     




     



#this allows sqlalchemy to find data and create data according to your db.Model
with app.app_context():
    db.create_all()

(__name__) == ('__main__')
app.run(debug=True)
