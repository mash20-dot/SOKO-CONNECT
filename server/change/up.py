from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Buyer_user, Business_user


change = Blueprint('/change', __name__)
#route for updating buyer credentials                      


@change.route('/update', methods=['UPDATE'])
@jwt_required()
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
     current_email = get_jwt_identity()
     up_date = Buyer_user.query.filter_by(email=current_email).first()
     
     if not up_date:
          return jsonify({'Error': 'information can not be updated'}), 403
     return jsonify(logged_in_as=current_email), 200
     



#Route for businesses to update their credentials
@change.route('/business_updates', methods=['POST'])
@jwt_required()
def business_updates():
     data = request.get_json()
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
     
     current_email = get_jwt_identity()
     bus_up = Business_user.query.filter_by(email=current_email)

     if not bus_up:
          return jsonify({'Error':'information can not be updated'}), 403
     return jsonify(logged_in_as=current_email), 200

     


#Route for business owners to delete their account
@change.route('/business_delete', methods=['DELETE'])
@jwt_required()
def business_delete():
     
     current_email = get_jwt_identity()
     dele_te = Business_user.query.filter_by(email=current_email)
     if not dele_te:
          return jsonify({'Error': 'Account could not be deleted'}), 403
     return jsonify(logged_in_as=current_email), 200
     

