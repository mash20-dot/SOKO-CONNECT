from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#db model for buyer authentication
class Buyer_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True,)
    password = db.Column(db.String(300),)

    

#db model for business authentication
class Business_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    business_name = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True,)
    phone = db.Column(db.String(150),)
    password = db.Column(db.String(300),)


#db model for buyer purchase history
class History(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        buyer_name = db.Column(db.String(50))
        buyer_product = db.Column(db.String(50))
        date = db.Column(db.String(30))
        email = db.Column(db.String(50))

class products(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        product_name = db.Column(db.String(50))
        product_price = db.Column(db.String(50))
        product_uses = db.Column(db.String(1000))


class Message(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        text = db.Column(db.String(1000))



class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    Full_name = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True,)
    password = db.Column(db.String(300),)
