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
             Missing_fields.append('date')

        if Missing_fields:
            return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400
         
         
         #getting user info for accessing this protected route using get_jwt_identity
        current_email = get_jwt_identity()

         #saves user info in the database
        new_user = History(buyer_name=buyer_name, buyer_product=buyer_product, date=date)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "purchase information successfully", "logged_in_as":current_email}), 200

       


@buyerhistory.route('/gethistory', methods=['GET'])
@jwt_required()
def gethistory():
     
     data = request.args
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
          Missing_fields.append('date')

     if Missing_fields:
          return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400
     
         

     current_email = get_jwt_identity()

     history_data = History.query.filter_by(email=current_email).all()


     if not current_email:
          return jsonify({'message': 'History not found'}), 403
     
      # Convert data to JSON-serializable format
     result = []
     for record in history_data:
        result.append({
            "buyer_name": record.buyer_name,
            "buyer_product": record.buyer_product,
            "date": record.date.strftime("%Y-%m-%d"),#convert date to string if it's a date object
        })

     return jsonify(result), 200

#TEST THIS