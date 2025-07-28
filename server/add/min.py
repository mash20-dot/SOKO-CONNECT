from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from main.models import db, Admin
#from flask_rbac import RBAC

add = Blueprint('/add', __name__)

#Route for admins to create account
@add.route('/Admin_Route', methods=['POST'])
def admin():
     data = request.get_json()
     Full_name = data.get('Full_name')
     email = data.get('email')
     password = data.get('password')

     Missing_fields = []
     if not Full_name:
          Missing_fields.append('Full_name')
     if not email:
          Missing_fields.append('email')
     if not password:
          Missing_fields.append('Password')
     if Missing_fields:     
          return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
     
      #Check if email already exists
     existing_user = Admin.query.filter_by(email=email).first()
     if existing_user:
            return jsonify({"message": "Email already exists"}), 400
        
     
      #hash the password, making it invisible
     hashed_password = generate_password_hash(password)

     #saves user info in the database
     new_user = Admin(Full_name=Full_name, email=email, password=hashed_password)
     db.session.add(new_user)
     db.session.commit()
     return jsonify({'message': 'Account created successfully'}), 201
     

@add.route('/Adminlogin', methods=['POST'])
def login():
     data = request.get_json()
     email = data.get('email')
     password = data.get('password')


     Missing_fields = []
     if not email:   
          Missing_fields.append('email')
     if not password:
          Missing_fields.append('Password')
     if Missing_fields:     
          return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
     
     
     # Query the admin user from database, to see if the credentials matches
     admin = Admin.query.filter_by(email=email).first()

     if not admin:
        return jsonify({'message': 'Invalid email'}), 400
     
     if check_password_hash(admin.password, password):
          pass
     else:
          return ({'message': 'Invalid password'}), 400

     
     
     #create an access token for the admin 
     access_token = create_access_token(identity=admin.email)
     
     response = jsonify({
          'msg': 'logged in successful',
            'access_token':access_token})
     #this token is stored in a cookie with this to verify their identity when visiting a protected route
     set_access_cookies(response, access_token)
     return response
     
     
#Route protecting users from accessing the admin dashboard
@add.route('/admindash', methods=['GET'])
@jwt_required()
def dashboard():
    
     current_email = get_jwt_identity()
     admin = Admin.query.filter_by(email=current_email).first()

     if not admin:
          return jsonify({'message': 'Access denied'}), 403
     return jsonify(logged_in_as=current_email), 200

@add.route('/upgrade', methods=['PUT'])
@jwt_required()
def upgrade():

     current_email = get_jwt_identity()
     get_email = Admin.query.filter_by(email=current_email).first()

     if not get_email:
          return jsonify({"message": "user could not be found"}), 404
     
     data = request.get_json()
     new_email = data.get('new_email')

     if not new_email:
          return jsonify({'message': "New email required"}), 400

     get_email.email = new_email
     db.session.commit()
     return jsonify({'message': 'Email has been updated successfully'}), 200


@add.route('/up_password', methods=['PUT'])
@jwt_required()
def up_password():

     current_email = get_jwt_identity()
     update_password = Admin.query.filter_by(email=current_email).first()

     if not update_password:
          return jsonify({'message': 'password could not be found'}), 400

     data = request.get_json()
     old_password = data.get('old_password')
     new_password = data.get('new_password')

     if not old_password or not new_password:
          return jsonify({'message': 'Both old_password and new_password must be provided'}), 400
     
     if not check_password_hash(update_password.password, old_password):
          return jsonify({'message': 'old_password is incorrect'}), 400
     
     update_password.password = generate_password_hash(new_password)
     db.session.commit()
     return jsonify({'message': 'password updated successfully'}), 200

     
