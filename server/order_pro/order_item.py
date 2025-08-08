from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required
from flask_jwt_extended  import get_jwt_identity
from main.models import db, Orders, Buyer_user
from major.decorator import role_required
import time
import random
import string

order_pro = Blueprint('order_pro', __name__)


def stream_order_updates():
    """Yields real-time updates about orders when called."""
    while True:
        latest_order = Orders.query.order_by(Orders.created_at.desc()).first()
        data = f"New order from user: {latest_order.buyer_user_id} at {latest_order.created_at}"
        yield f"data: {data}\n\n"
        time.sleep(5) 



@order_pro.route('/order', methods=['POST'])
@jwt_required()
@role_required("user")
def order(): 

     
     data = request.get_json() 
     product = data.get("product")

     Missing_fields = []
     if not product:
          Missing_fields.append("product")

     if Missing_fields:
          return jsonify({"message": f"missing_fields, {Missing_fields}"})

     current_email = get_jwt_identity()
     Order_id = Buyer_user.query.filter_by(email=current_email).first()

     if not Order_id:
          return jsonify({"message": "user not found"}), 400


     def generate_tracking_number():
        while True:
               random_part = int(''.join(random.choices(string.digits, k=6)))
               tracking_number = f"{random_part}"
            # Ensure it's unique
               existing_user = Orders.query.filter_by(tracking_number=tracking_number).first()
               if not existing_user:
                return tracking_number
     
     new_order = Orders(
          product=product,buyer_user_id=Order_id.id, tracking_number=generate_tracking_number())
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
          
          buyer = Orders.query.filter_by(product=product).all()

          if not buyer:
               return jsonify({"message": "no order found"}), 400

           # Convert data to JSON-serializable format
          result = []
          for record in buyer:
               result.append({
            "product": record.product,
            "ordered_at": record.ordered_at,
            "tracking_number": record.tracking_number,
            "shipping_date": record.shipping_date,
            "delivery_date": record.delivery_date
          })

          return jsonify(result), 200

#returns a real time update on a customer order
@order_pro.route('/orders/stream')
def stream_orders():
    return Response(stream_order_updates(), mimetype='text/event-stream')


#HANDLE WHERE A USER CAN RETRIEVE ONLY WHAT HE BOUGHT NOT WHAT OTHERS BOUGHT AS WELL