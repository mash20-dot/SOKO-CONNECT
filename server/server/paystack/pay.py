from flask import Flask, Blueprint, redirect, jsonify, request
import requests
import os
from flask_jwt_extended import jwt_required
from major.decorator import role_required
from dotenv import load_dotenv
from main.models import db, Orders, Payment
from datetime import datetime
import hashlib, hmac


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
    


#VERIFYING PAYMENTS
@paystack.route('/verify_payment/<reference>', methods=['GET'])
@jwt_required(locations=['headers'])
@role_required("user")
def verify_payment(reference):

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers ={
    "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        verification_data = response.json()
    except requests.exceptions.RequestException:
        return jsonify({"message": "Error verifying transaction"}), 500
    except ValueError:
        return jsonify({"message": "Invalid response from paystack"}), 500
    
    payment = Payment.query.filter_by(reference=reference).first()
    if not payment:
        return jsonify({"message": "payment not found"}), 404
    
    if verification_data["data"]["status"] == "success":
        payment.status = "success"
    
    else:
        payment.status = "failed"
    
    db.session.commit()
    return jsonify(verification_data)


#paystack webhook
@paystack.route("/paystack/webhook", methods=["POST"])
def paystack_webhook():
    # Verify signature
    paystack_signature = request.headers.get("x-paystack-signature")
    body = request.get_data()

    secret = os.getenv("PAYSTACK_SECRET_KEY").encode()
    computer_signature = hmac.new(secret, body, hashlib.sha512).hexdigest()

    if computer_signature != paystack_signature:
        return jsonify({"status": "error", "message": "Invalid signature"}), 400

    event = request.get_json()

    if event["event"] == "charge.success":
        reference = event["data"]["reference"]
        # update your Payment record
        payment = Payment.query.filter_by(reference=reference).first()
        if payment:
            payment.status = "success"
            db.session.commit()

    return jsonify({"status": "success"}), 200




