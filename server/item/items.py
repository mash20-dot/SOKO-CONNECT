from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.models import db, products, Business_user
from major.decorate import role_required

item = Blueprint('item', __name__)
#FOR BUSINESSES TO POST THEIR PRODUCT
@item.route('/product', methods=['POST'])
@jwt_required()
@role_required("business_owner")
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
        business = Business_user.query.filter_by(email=current_email).first()

      
       #saves products/items into the database
        new_product = products(
            product_name=product_name, product_price=product_price, product_uses=product_uses,
              business_user_id=business.id)
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({"message":"product saved successfully", "logged_in_as": current_email}), 200

        
        
        
#ROUTE FOR GETTING ITEMS FROM THE DATABASE
@item.route('/getproduct', methods=['GET'])
@jwt_required()
def getproduct():
     
    data = request.get_json()
    product_name = data.get('product_name')

    
    Missing_fields= []
    if not product_name:
            Missing_fields.append('product_name')

    if Missing_fields:
        return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400

    
     #Access the identity of the logged in useer with get_jwt_identity
    current_email = get_jwt_identity()

    product_get = products.query.filter_by(product_name=product_name).all()

    if not product_get:
          return jsonify({"message": "Product could not be found"}), 403                 


 # Convert data to JSON-serializable format
    result = []
    for record in product_get:
        result.append({
            "product_name": record.product_name,
            "product_price": record.product_price,
            "product_uses": record.product_uses,
        })

    return jsonify(result), 200

#TRY TO FIX THIS USER NOT FOUND

     
     



