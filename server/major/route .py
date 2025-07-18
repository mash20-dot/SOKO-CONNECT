from flask import  Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended  import get_jwt_identity
from flask_jwt_extended  import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended  import set_access_cookies
from flask_jwt_extended  import unset_jwt_cookies
from flask_jwt_extended  import get_jwt
from werkzeug.security  import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from main.models import db, Buyer_user, Business_user

major = Blueprint('major', __name__)


# Define how early before expiration you want to refresh the token
REFRESH_WINDOW_MINUTES = 60
#Refreshing token  
@major.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=REFRESH_WINDOW_MINUTES))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
      #return response if jwt is invalid
        return response





#signup route for buyers
@major.route('/register', methods=['POST'])
def register():
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
          
        Missing_fields = []
        if not firstname:
            Missing_fields.append('firstname')
        if not lastname:
            Missing_fields.append('lastname')
        if not email:
            Missing_fields.append('email')
        if not password:
            Missing_fields.append('password')
            
        if Missing_fields:   
           return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
        
        
        #find's email from db and compare if email already exist
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
@major.route('/login', methods=['POST'])
def login():
       
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        #find user by email
        user = Buyer_user.query.filter_by(email=email).first()

        if not user:
             return jsonify({'message': 'User not found'}), 400

        #hashes the entered password and comapare it to the hash password in the db
        if check_password_hash(user.password, password):
            pass
        else:
            return jsonify({'message': 'Invalid password'}), 401

        
        
        #create an access token for the user to verify their identity when visiting a protected route
        access_token = create_access_token(identity=email)
        
        response = jsonify({
             'msg': 'logged in successfully',
               'access_token':access_token})
        set_access_cookies(response, access_token)
        return response
     


#This route is working perfectly do not touch it
#Signup form for businesses
@major.route('/business', methods=['POST'])
def business_user():
    data = request.get_json()
    business_name = data.get('business_name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    
    Missing_fields= []

    if not business_name:
        Missing_fields.append('business_name')
    if not email:
        Missing_fields.append('email')
    if not phone:
        Missing_fields.append('phone')
    if not password:
        Missing_fields.append('password')
    
    if Missing_fields:  
        #if all fields are provided, it creates an access token
        return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
    
    #Check if email already exists by getting it from the db
    existing_user = Business_user.query.filter_by(email=email).first()
    if existing_user:
          return jsonify({"message": "Email already exists"}), 400
    
    #hash the password, making it invisible
    hashed_password = generate_password_hash(password)
    
    #saves products/items into the database
    new_business = Business_user(business_name=business_name, email=email, phone=phone, password=hashed_password)
    db.session.add(new_business)
    db.session.commit()
    return jsonify({'message': 'Account created successfully'}),201


            
            
 #THIS ROUTE IS WORKING PERFECTLY DO NOT TOUCH IT    
#LOGIN form for business
@major.route('/getbusiness', methods=['POST'])
def getbusiness():
     #get data from the database
     data = request.get_json()
     email = data.get('email')
     password = data.get('password')


     #find user by email
     business_user = Business_user.query.filter_by(email=email).first()
     
     
     
     if not business_user:
          return jsonify({"message": "Invalid email"}), 404
     
     #hashes the entered password and comapare it to the hash password in the db
     if check_password_hash(business_user.password, password):
        pass
     else:
        return jsonify({'message': 'Invalid password'}), 401

     #create an access token for the user
     #this access token is used to authenticate the user in subsequent requests
     access_token = create_access_token(identity=email)
     
     response = jsonify({
        "msg": "logged in successful",
          "access_token":access_token})
     
     set_access_cookies(response, access_token)
     return response
     