from flask import Flask, Blueprint, redirect, jsonify
import requests
import os
from flask_jwt_extended import jwt_required
from major.decorator import role_required
from dotenv import load_dotenv
from main.models import db, Orders, Payment
from datetime import datetime


load_dotenv()

paystack = Blueprint('paystack', __name__)

@paystack.route('/payment', methods=['GET'])
@jwt_required()
@role_required("user")
def initialize_paystack_transaction(tracking_code):
    
    order = Orders.query.filter_by(tracking_code=tracking_code).first()

    # Creating Payment record (pending)
    payment = Payment(
        reference=f"PAY-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{order.id}",
        status="pending",
        created_at=datetime.utcnow()
    )

    db.session.add(payment)
    order.payment = payment
    db.session.commit()
    
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": order.buyer_user.email,
        "amount": order.amount * 100,
        "reference": payment.reference
    }
    try:
        #making the API request with the ini url header and sending the payload in a json format
        response = requests.post(url, headers=headers, json=payload)
    except requests.exceptions.RequestException:
            return jsonify({"Error": "error initializing transaction"}), 500
    
    try:   
        #converts paystack json response into python script
        paystack_response = response.json()
    except ValueError:
        return jsonify({"Error": "Invalid json response from paystack"})

    # Save Paystack gateway response
    payment.gateway_response = paystack_response.get("message", "")
    db.session.commit()

    return paystack_response
    

#VERIFY THE BUYERS PAYMENT AND SET UP WEBHOOKS


