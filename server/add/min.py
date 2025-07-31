from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required
from major.decorator import role_required


add = Blueprint('/add', __name__)

     
     
#Route protecting users from accessing the admin dashboard
@add.route('/admindash', methods=['GET'])
@jwt_required()
@role_required("admin")
def dashboard():
     return jsonify({"message": "welcome admin"}), 200

