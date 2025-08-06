from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended  import get_jwt_identity
from main.models import db, Orders, Buyer_user
from major.decorator import role_required

order_pro = Blueprint('order_pro', __name__)


@order_pro.route('/order', methods=['POST'])
@jwt_required()
@role_required("user")
def order(): 

     
     data = request.get_json() 
     product = data.get("product")
     payment = data.get("payment")

     Missing_fields = []
     if not product:
          Missing_fields.append("product")
     if not payment:
          Missing_fields.append("payment")

     if Missing_fields:
          return jsonify({"message": f"missing_fields, {Missing_fields}"})

     current_email = get_jwt_identity()
     Order_id = Buyer_user.query.filter_by(email=current_email).first()

     if not Order_id:
          return jsonify({"message": "user not found"}), 400
     
     new_order = Orders(
          product=product, payment=payment, buyer_user_id=Order_id.id)
     db.session.add(new_order)
     db.session.commit()
     return jsonify({"message": "order made successfully"}), 201




#FOR BUYERS TO GET THEIR ORDER DETAILS
@order_pro.route('/getorder', methods=['GET'])
@jwt_required()
@role_required("user") 
def get_order():
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
