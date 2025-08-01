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
    History = db.relationship('History', backref='user', lazy=True)

    

#db model for business authentication
class Business_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    business_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(20), default="business_owner", nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('products', backref='owner', lazy=True)



#db model for buyer purchase history
class History(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        buyer_name = db.Column(db.String(50))
        buyer_product = db.Column(db.String(50))
        date = db.Column(db.String(30))
        buyer_user_id = db.Column(db.Integer, db.ForeignKey('buyer_user.id'), nullable=False)

class products(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        product_name = db.Column(db.String(50))
        product_price = db.Column(db.String(50))
        product_uses = db.Column(db.String(1000))
        create_at = db.Column(db.DateTime, default=datetime.utcnow)
        business_user_id = db.Column(db.Integer, db.ForeignKey('business_user.id'), nullable=False)

class Message(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        text = db.Column(db.String(1000))


#DEVELOP AN ORDER TABLE
