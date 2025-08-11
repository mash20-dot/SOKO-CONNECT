from flask import Flask, request, jsonify, Response, Blueprint, redirect
import requests
import os
from flask_jwt_extended import jwt_required
from major.decorator import role_required


paystack = Blueprint('paystack', __name__)

@paystack.route('/payment', methods=['GET'])
@jwt_required()
@role_required("user")
def payment():

    data = request.get_json()
    email = data.get("email")
    money = data.get("money")
    
