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

     #generates a unique code for buyers to retrieve order information
     def generate_tracking_code():
        while True:
               random_part = (''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
               tracking_code = f"{random_part}"
               existing_user = Orders.query.filter_by(tracking_code=tracking_code).first()
               if not existing_user:
                return tracking_code
     
     new_order = Orders(
          product=product,buyer_user_id=Order_id.id, tracking_code=generate_tracking_code())
     db.session.add(new_order)
     db.session.commit()
     return jsonify({"message": f"order made successfully, tracking code is {generate_tracking_code()}"}), 201




#FOR BUYERS TO GET THEIR ORDER DETAILS
@order_pro.route('/getorder', methods=['GET'])
@jwt_required()
@role_required("user") 
def get_order():
          data = request.get_json()
          tracking_code = data.get('tracking_code')

        #stores a blank field and if not field throws an error
          Missing_fields = []
          if not tracking_code:
             Missing_fields.append('tracking_code')

          if Missing_fields:
            return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400
         
         
         #getting user info for accessing this protected route using get_jwt_identity
          current_email = get_jwt_identity()
          if current_email:
               pass
          else:
               return jsonify({"messagge": "user not found"}), 400
          
          buyer = Orders.query.filter_by(tracking_code=tracking_code).all()

          if not buyer:
               return jsonify({"message": "no order found"}), 400
          
          #purchase = Orders.query.filter_by(current_email=buyer_user_id).all()
          #if not purchase:
               #return jsonify({"message": "You did not make any purchase"})

           # Convert data to JSON-serializable format
          result = []
          for record in buyer:
               result.append({
            "product": record.product,
            "ordered_at": record.ordered_at,
            "tracking_code": record.tracking_code,
            "shipping_date": record.shipping_date,
            "delivery_date": record.delivery_date
          })

          return jsonify(result), 200

#returns a real time update on a customer order
@order_pro.route('/orders/stream')
def stream_orders():
    return Response(stream_order_updates(), mimetype='text/event-stream')


@order_pro.route('/update_order', methods=['PUT'])
@jwt_required()
@role_required("user")
def update_order():

     current_email = get_jwt_identity()
     change_order = Orders.query.filter_by(tracking_code=tracking_code).first()

     if not current_email:
          return jsonify({"message": "user not found"}), 400
     
     data = request.get_json()
     new_product = data.get("product")
     tracking_code = data.get("old_tracking")
     
     if not new_product or not tracking_code:
          return jsonify({"message": "old_tracking and product required"}), 401
     
     if not (change_order.tracking_code,  tracking_code):
          return jsonify({"message": "tracking code is invalid"}), 400
     
     change_order.product = new_product
     db.session.commit()
     return jsonify({"message": "update made successfullt"}), 201
     
     #TEST THIS ROUTE AND ADD A ROUTE TO DELETE AN ORDER

@order_pro.route('/delete_order', methods=['DELETE'])
@jwt_required()
@role_required("user")
def delete_order():

     current_email = get_jwt_identity()
     user =    Buyer_user.query.filter_by(email=current_email).first()
     
     if not user:
          return jsonify({"message": "no order was found"}), 400
     
     
     data= request.get_json()
     your_tracking_code = data.get("your_tracking_code")
     del_pro = data.get("del_pro")

     

     if not your_tracking_code or not del_pro:
          return jsonify({"message": "del_pro and tracking code required"}), 401
     
     track = Orders.query.filter_by(tracking_code=your_tracking_code).first()

     if not (track.tracking_code, your_tracking_code):
          return jsonify({"message": "Invalid tracking code"}), 400

     
     track.product = del_pro
     db.session.delete(track)
     db.session.commit()
     return jsonify({"message": f"Order {track} deleted successfully"}), 201
