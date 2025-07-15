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

        
       #saves products/items into the database
        new_product = products(product_name=product_name, product_price=product_price, product_uses=product_uses)
        db.session.add(new_product)
        db.session.commit()
        
        # Accessing the identity of the current user with get_jwt_identity
        current_email = get_jwt_identity()
        pro_duct = products.query.filter_by(email=current_email)
        if not pro_duct:
             return jsonify({'message': 'product could not be uploaded'}), 403
        return jsonify(logged_in_as=current_email), 200


        
        
        
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

    #not working yet have to fix it    
    #if product in products:
         #return jsonify({'message': 'product already uploaded'})
    #product = products.query.filter_by(product_name=product_name).first()

    if product:
         return jsonify({'message': 'items retrieved successfully',
                         'product_name':product_name,
                         'product_price':product_price,
                         'product_uses':product_uses
                         
    }), 200
    
    if not products:
         return jsonify({'message': 'could not retrieve item'}), 400
     #Access the identity of thr logged in useer with get_jwt_identity
    current_email = get_jwt_identity()
    get_product = products.query.filter_by(email=current_email)
    if not get_product:
         return jsonify({'message': 'can not retrieve product'}), 403
    return jsonify(looged_in_as=current_email), 200                                  



