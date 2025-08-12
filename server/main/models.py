from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#db model for buyer authentication
class Buyer_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    Orders = db.relationship('Orders', backref='user', lazy=True)


    
class Orders(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(150), nullable=False)
    tracking_code = db.Column(db.String(50), unique=True, nullable=False)
    ordered_at = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), default="pending", nullable=False)
    shipping_date = db.Column(db.DateTime)
    delivery_date = db.Column(db.DateTime)
    buyer_user_id = db.Column(db.Integer, db.ForeignKey('buyer_user.id'), nullable=False)
    product_s_id = db.Column(db.Integer, db.ForeignKey("product_s.id"), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"), nullable=False)



#db model for business authentication
class Business_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    business_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(20), default="business_owner", nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    Product_s = db.relationship('Product_s', backref='owner', lazy=True)


class Product_s(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        product_name = db.Column(db.String(50))
        product_price = db.Column(db.String(50))
        product_uses = db.Column(db.String(1000))
        create_at = db.Column(db.DateTime, default=datetime.utcnow)
        business_user_id = db.Column(db.Integer, db.ForeignKey('business_user.id'), nullable=False)
        Orders = db.relationship("Orders", backref="order", lazy=True)

class Payment(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     reference = db.Column(db.String(100), unique=True, nullable=False)
     status = db.Column(db.String(100), default="pending")
     gateway_response = db.Column(db.String(100))
     paid_at = db.Column(db.DateTime)
     created_at = db.Column(db.DateTime, default=datetime.utcnow)
     Orders = db.relationship("Orders", backref="order", lazy=True)





#ADD A PAYMENT ROW WITH DEFAULT="Pending" AND AMOUNT COLUMN TO ORDERS TABLE AND A PAYSTACK DB MODEL AND CONNECT BOTH