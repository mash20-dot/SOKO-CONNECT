from flask import  Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended  import set_access_cookies, jwt_required
from flask_jwt_extended  import get_jwt, get_jwt_identity, verify_jwt_in_request
from werkzeug.security  import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from main.models import db, Buyer_user, Business_user
from major.decorator import role_required

major = Blueprint('major', __name__)


# Define how early before expiration you want to refresh the token
REFRESH_WINDOW_MINUTES = 60
#Refreshing token  
@major.after_request
def refresh_expiring_jwts(response):
    try:
        #verify if jwt is valid
        verify_jwt_in_request(optional=True) 

        #asking when the token is going to expire
        exp_timestamp = get_jwt()["exp"]
        
        #asking what time is it
        now = datetime.now(timezone.utc)
        
        #looking ahead 60 minutes from now
        target_timestamp = datetime.timestamp(now + timedelta(minutes=REFRESH_WINDOW_MINUTES))
        
        #asking if the key will espire in that 60 minutes
        if target_timestamp > exp_timestamp:
            
            #then set a new key and save in cookies
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

        Missing_fields = []
        if not email:
            Missing_fields.append('email')
        if not password:
            Missing_fields.append('password')
        if Missing_fields:
            return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400

        #find user by email
        user = Buyer_user.query.filter_by(email=email).first()

        if not user:
             return jsonify({'message': 'Invalid email'}), 400

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

    Missing_fields = []
    if not email:
        Missing_fields.append('email')
    if not password:
        Missing_fields.append('password')
    if Missing_fields:
        return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400


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


#UPDATING BUYERS EMAIL
@major.route('/difference', methods=['PUT'])
@jwt_required()
def difference():

    current_email = get_jwt_identity()
    new_info = Buyer_user.query.filter_by(email=current_email).first()

    if not new_info:
        return jsonify({"message": "user not found"}), 404
    
    data = request.get_json()
    new_email = data.get("new_email")

    if not new_email:
        return jsonify({"message": "New email required"})
    
    new_info.email = new_email
    db.session.commit()
    return jsonify({"message": "Email updated successfully"}), 200


#UPDATING BUYERS PASSWORD
@major.route('/password_update', methods=['PUT'])
@jwt_required()
def up_date():

    current_email = get_jwt_identity()
    change_password = Buyer_user.query.filter_by(email=current_email).first()

    if not change_password:
        return jsonify({"message": "user not found"}), 404
    

    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')


    if not old_password or not new_password:
        return jsonify({"message": "Both old and new password are required"}), 400

    if not check_password_hash(change_password.password, old_password):
        return jsonify({"message": "Old password is incorrect"}), 401
    
    change_password.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "password updated successfully"}), 200



#UPDATING BUSINESS OWNERS EMAIL
@major.route('/business_update', methods=['PUT'])
@jwt_required()
def business_update():

    current_email = get_jwt_identity()
    new_info = Business_user.query.filter_by(email=current_email).first()

    if not new_info:
        return jsonify({"message": "user not found"}), 404
    
    data = request.get_json()
    new_email = data.get("new_email")

    if not new_email:
        return jsonify({"message": "New email required"})
    
    new_info.email = new_email
    db.session.commit()
    return jsonify({"message": "Email updated successfully"}), 200


#UPDATING BUSINESS OWNERS PASSWORD
@major.route('/business_password', methods=['PUT'])
@jwt_required()
def bus_password():

    current_email = get_jwt_identity()
    change_password = Business_user.query.filter_by(email=current_email).first()

    if not change_password:
        return jsonify({"message": "user not found"}), 404
    

    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')


    if not old_password or not new_password:
        return jsonify({"message": "Both old and new password are required"}), 400

    if not check_password_hash(change_password.password, old_password):
        return jsonify({"message": "Old password is incorrect"}), 401
    
    change_password.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "password updated successfully"}), 200


@major.route('/delete_user', methods=['DELETE'])
@jwt_required()
def delete_user():

    current_email = get_jwt_identity()
    delete_email = Buyer_user.query.filter_by(email=current_email).first()

    if not delete_email:
        return jsonify({"message": "user not found"}), 400
    
    data = request.get_json()
    remove_email = data.get("remove_email")
    remove_password = data.get("remove_password")

    if not remove_email or not remove_password:
        return jsonify({"message": "Both email and password required to delete accound"}), 400
    
    if not check_password_hash(delete_email.password, remove_password):
        return jsonify({"message": "Invalid password"}), 400
    
    delete_email.email = remove_email
    db.session.delete(delete_email)
    db.session.commit()
    return jsonify({"message": f"user {delete_email} deleted successfully"}), 201


@major.route('/delete_business', methods=['DELETE'])
@jwt_required()
def delete_business():

    current_email = get_jwt_identity()
    delete_email = Business_user.query.filter_by(email=current_email).first()

    if not delete_email:
        return jsonify({"message": "user not found"}), 400
    
    data = request.get_json()
    remove_email = data.get("remove_email")
    remove_password = data.get("remove_password")

    #TEST FOR THIS BLOCK OF CODE
    if not remove_email:
        return jsonify({"message": "email is required"}), 400
    
    if not check_password_hash(delete_email.password, remove_password):
        return jsonify({"message": "Invalid password"})
    
    delete_email.email = remove_email
    db.session.delete(delete_email)
    db.session.commit()
    return jsonify({"message": f"user {delete_email} has been deleted successfully"}), 201


