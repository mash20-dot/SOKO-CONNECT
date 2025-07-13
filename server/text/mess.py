from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Message

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
          return jsonify({Missing_fields, 'Missing_fields'})                            
                                                  
     current_email = get_jwt_identity()
     mess_age = Message.query.filter_by(email=current_email).first()

     if not mess_age:
          return jsonify({'message': 'unable to send message'}), 403
     return jsonify(logged_in_as=current_email), 200




