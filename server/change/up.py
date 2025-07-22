from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.models import db, Buyer_user, Business_user


change = Blueprint('/change', __name__)
#route for updating buyer credentials                      


@change.route('/update', methods=['PUT'])
@jwt_required()
def update():                          
     data = request.get_json()
     business_name = data.get('business_name')
     email = data.get('email')
     password = data.get('password')
     phone = data.get('phone')

     Missing_fields= []

     if not business_name:
          Missing_fields.append('business_name')
     if not email:
          Missing_fields.append('email')
     if not password:
          Missing_fields.append('password')
     if not phone:
          Missing_fields.append('phone')
          return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
     
     current_email = get_jwt_identity()
     up_date = Business_user.query.filter_by(email=current_email).first()
     
     if not up_date:
          return jsonify({'Error': 'information can not be updated'}), 403
     

     #saves user info in the database
     new_user = Buyer_user(business_name=business_name, phone=phone, email=email, password=password)
     db.session.add(new_user)
     db.session.commit()
     return jsonify({'message': 'Information updated successfully'}), 200


     



#Route for buyers to update their credentials
@change.route('/business_updates', methods=['PUT'])
@jwt_required()
def business_updates():
     data = request.get_json()
     firstname = data.get('firstname')
     lastname = data.get('lastname')
     email = data.get('email')
     password = data.get('password')

     Missing_fields = []
     if not firstname:
          return Missing_fields.append('firstname')
     if not lastname:
          return Missing_fields.append('lastname')
     if not email:
          return Missing_fields.append('email')
     if not password:
          return Missing_fields.append('password')
     
     if Missing_fields:
          return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400

     
     current_email = get_jwt_identity()
     bus_up = Buyer_user.query.filter_by(email=current_email).first()

     if not bus_up:
          return jsonify({'Error':'information can not be updated'}), 403

     #saves user info in the database
     new_user = Buyer_user(firstname=firstname, lastname=lastname, email=email, password=password)
     db.session.add(new_user)
     db.session.commit()
     return jsonify({'message': 'Information updated successfully'}), 200




#Route for business owners to delete their account
@change.route('/business_delete', methods=['DELETE'])
@jwt_required()
def business_delete():
     
     current_email = get_jwt_identity()
     dele_te = Business_user.query.filter_by(email=current_email)
     if not dele_te:
          return jsonify({'Error': 'Account could not be deleted'}), 403
     return jsonify(logged_in_as=current_email), 200
     

