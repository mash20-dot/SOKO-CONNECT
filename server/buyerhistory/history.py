from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended  import get_jwt_identity
from main.models import db, Orders
from major.decorator import role_required

buyerhistory = Blueprint('buyerhistory', __name__)

#FOR BUYER TO FILL WHEN CONTACTING OR PURCHASING SOMETHING ON THE PLATFORM
@buyerhistory.route('/history', methods=['POST'])
@jwt_required()
@role_required("user") 
def history():
          data = request.get_json()
          product = data.get('product')

        #stores a blank field and if not field throws an error
          Missing_fields = []
          if not product:
             Missing_fields.append('my_orders')

          if Missing_fields:
            return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400
         
         
         #getting user info for accessing this protected route using get_jwt_identity
          current_email = get_jwt_identity()
          if current_email:
               pass
          else:
               return jsonify({"messagge": "user not found"}), 400
          
          buyer = Orders.query.filter_by(product=product).first()

          if not buyer:
               return jsonify({"message": "no order found"}), 400

           # Convert data to JSON-serializable format
          result = []
          for record in buyer:
               result.append({
            "product": record.buyer_name,
            "order_status": record.buyer_product,
            "status": record.date,
          })

          return jsonify(result), 200
