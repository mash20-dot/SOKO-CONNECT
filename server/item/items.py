from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.models import db, products

item = Blueprint('item', __name__)

@item.route('/product', methods=['POST'])
@jwt_required()
def product():
        data = request.get_json()
        product_name = data.get('product_name')
        product_price = data.get('product_price')
        product_uses = data.get('product_uses')

        Missing_fields= []

        if not product_name:
            Missing_fields.append('product_name')
        if not product_price:
            Missing_fields.append('product_price')
        if not product_uses:
            Missing_fields.append('product_uses')
    
            

        if Missing_fields:
             return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400

        # Accessing the identity of the current user with get_jwt_identity
        current_email = get_jwt_identity()
       #saves products/items into the database
        new_product = products(
            product_name=product_name, product_price=product_price, product_uses=product_uses, email=current_email)
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({"message":"product saved successfully", "logged_in_as": current_email}), 200


        
        
        
#ROUTE FOR GETTING ITEMS FROM THE DATABASE
@item.route('/getproduct', methods=['GET'])
@jwt_required()
def getproduct():
     
    data = request.args
    product_name = request.args.get('product_name')
    product_price = request.args.get('product_price')
    product_uses = request.args.get('product_uses')

    
    Missing_fields= []
    if not product_name:
            Missing_fields.append('product_name')
    if not product_price:
            Missing_fields.append('product_price')
    if not product_uses:
            Missing_fields.append('product_uses')


    if Missing_fields:
        return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400

    
     #Access the identity of the logged in useer with get_jwt_identity
    current_email = get_jwt_identity()

    if not current_email:
          return jsonify({"message": "Access denied"}), 403                 
    
    return jsonify({  'message': 'Data retrieved',
                            'product_name': product_name,
                            'product_price': product_price,
                            'product_uses': product_uses
                                 
     }), 200


