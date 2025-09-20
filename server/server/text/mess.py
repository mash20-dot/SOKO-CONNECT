from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.models import db, Message

text = Blueprint('/text', __name__)

#Route for messages
@text.route('/message', methods=['POST'])
@jwt_required()
def message():
     data = request.get_json()
     text = data.get('text')

     Missing_fields = []
     if not text:
          Missing_fields.append('text')

     if Missing_fields:
          return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
                             
                                                  
     current_email = get_jwt_identity()
     if not current_email:
          return jsonify({"message": "Access denied"}), 403
     return jsonify({'message': 'message sent successfully'}), 201




