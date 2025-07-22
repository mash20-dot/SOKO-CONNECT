from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended  import get_jwt_identity
from main.models import db, History

buyerhistory = Blueprint('buyerhistory', __name__)

@buyerhistory.route('/history', methods=['POST'])
@jwt_required()
def history():
        data = request.get_json()
        buyer_name = data.get('buyer_name')
        buyer_product = data.get('buyer_product')
        date = data.get('date')

        #stores a blank field and if not field throws an error
        Missing_fields = []
        if not buyer_name:
             Missing_fields.append('buyer_name')
        if not buyer_product:
             Missing_fields.append('buyer_product')
        if not date:
             Missing_fields.append('data')

        if Missing_fields:
            return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400
        
         #saves user info in the database
        new_user = History(buyer_name=buyer_name, buyer_product=buyer_product, date=date)
        db.session.add(new_user)
        db.session.commit()
        
        #getting user info for accessing this protected route using get_jwt_identity
        current_email = get_jwt_identity()
        history = History.query.filter_by(email=current_email).first()

        
        if not history:
             return jsonify({'message': 'information could not be saved'}), 403
        
        return jsonify(logged_in_as=current_email), 200

       


@buyerhistory.route('/gethistory', methods=['GET'])
@jwt_required()
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
     
         

     current_email = get_jwt_identity()
     business_his = History.query.filter_by(email=current_email).first()

     if not business_his:
          return jsonify({'message': 'Access denied'}), 403
     
     return jsonify({  'message': 'Data retrieved',
                            'buyer_name': buyer_name,
                            'buyer_product': buyer_product,
                            'date': data
                                 
     }), 200

