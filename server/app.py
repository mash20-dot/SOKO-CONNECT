from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os



app = Flask(__name__)


#database structure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sokoconnect.db'
db = SQLAlchemy(app)

class Buyer_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True,)
    password = db.Column(db.String(150),)






#signup route for buyers
@app.route('/register', methods=['POST'])
def register():
        data = request.get_json()
        firstname = data.get('fname')
        lastname = data.get('lname')
        email = data.get('email') 
        password = data.get('password')


        #checks for every empty space and save it if none of that empty space is not provided it throws that error
        Missing_fields= []

        if not firstname:
            Missing_fields.append(firstname)
        if not lastname:
            Missing_fields.append(lastname)
        if not email:
            Missing_fields.append(email)
        if not password:
            Missing_fields.append(password)
            return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400

        if (firstname and lastname and email and password):
            return jsonify({'message': 'successfully signed up'}), 201

        #Check if email already exists
        existing_user = Buyer_info.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 409
    
    

        #hash the password, making it invisible
        hashed_password = generate_password_hash(password)


        #saves user info in the database
        new_user = Buyer_info(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
   
    
        
    


#login route for buyers
@app.route('/login', methods=['POST'])
def login():

        data = ({"user":
           "firstname"
           "lastname"
           "email"
           "password"
        })

        data = request.get_json()
        firstname = data.get('fname')
        lastname = data.get('lname')
        email = data.get('email')
        password = data.get('password')


        #find a user by email 
        user = Buyer_info.query.filter_by(email=email).first()

        #If user exists and password matches
        if user and check_password_hash(user.password, password):
            return jsonify({"message": "Successfully logged in"}), 201

        if not (firstname and lastname and email and password):
            return jsonify({"message": "Invalid credentials"}), 401
    

        Missing_fields = []
        if not firstname:
            Missing_fields.append('fname')
        if not lastname:
            Missing_fields.append('lname')
        if not email:
            Missing_fields.append('email')
        if not password:
            Missing_fields.append('password')
            return jsonify({f"Missing_fields": {Missing_fields}},"fill in all blank spaces"), 400
    

    



#DATABASE FOR BUSINESS PROFILE 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///business.db'

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    business_name = db.Column(db.String(50))
    business_email = db.Column(db.String(150), unique=True,)
    phone = db.Column(db.String(150),)


#Signup form for businesses
@app.route('/business', methods=['POST'])
def business_user():
    data = request.get_json()
    business_name = data.get('business_name')
    business_email = data.get('business_email')
    phone = data.get('phone')



    Missing_fields= []

    if not business_name:
        Missing_fields.append('business_name')
    if not business_email:
        Missing_fields.append('business_email')
    if not phone:
        Missing_fields.append('phone')
        
        
    
    if Missing_fields:
        return jsonify({"Error": f"Missing_fields: {Missing_fields}"}), 400
     


     
    #saves products/items into the database
    new_business = Business(business_name=business_name, business_email=business_email, phone=phone,)
    db.session.add(new_business)
    db.session.commit()



    if (business_name and business_email and phone):
        return jsonify({'message': 'Information uploaded successfully'})
    else:
        return jsonify({'message': "Error, can't upload information"})
    
#LOGIN form for business
@app.route('/getbusiness', methods=['POST'])

def getbusiness():
     #get data from the database
     data = request.get_json()
     business_name = data.get('business_name')
     business_email = data.get('business_email')
     phone = data.get('phone')
     password = data.get('password')


     Missing_fields = []
     if not business_name:
            Missing_fields.append('business_name')
     if not business_email:
            Missing_fields.append('business_email')
     if not phone:
            Missing_fields.append('phone')
     if not password:
            Missing_fields.append('password')


     if Missing_fields:
          return jsonify({f"Missing_fields", Missing_fields,"'message': fill in all blank spaces"}), 400
    
            




    #Helps to find user by email or phone
     business_user = Business.query.filter_by(
          business_email=business_email, phone=phone).first()
     
     
     #conditional statements
     if   business_user:
          return jsonify({'message': 'Information retrieved successfully'}), 201
     else:
          return jsonify({'message': 'Error, information could not be retrieved'}), 404
     
     
     
    
#PRODUCT CODE BASE
#product database structure
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///product.db'                                           

class products(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        product_name = db.Column(db.String(50))
        product_price = db.Column(db.String(50))
        product_uses = db.Column(db.String(1000))
        product_images = db.Column(db.String)

@app.route('/product', methods=['POST'])
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

        
             
       
        if product:
             return jsonify({'message': 'Item updated successfully '}), 201
        
        
        if not product:
             return jsonify({'message': 'Error item not updated'}), 400

        
        
        
#ROUTE FOR GETTING ITEMS FROM THE DATABASE
@app.route('/getproduct', methods=['GET'])
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
    product = products.query.filter_by(product_name=product_name).first()

    if product:
         return jsonify({'message': 'items retrieved successfully',
                         'product_name':product_name,
                         'product_price':product_price,
                         'product_uses':product_uses
                         
    }), 200
    if not product:
         return jsonify({'message': 'could not retrieve item'}), 400
    
    
    



#A form a buyer will fill whiles contacting or buying a product, this will go into the business owner histoy

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///contact.db'                                           
class History(db.Model):
        id = db.Column(db.Integer, primary_key=True)    
        buyer_name = db.Column(db.String(50))
        buyer_product = db.Column(db.String(50))
        date = db.Column(db.String(30))


@app.route('/history', methods=['POST'])
def history():
        data = request.get_json()
        buyer_name = data.get('buyer_name')
        buyer_product = data.get('buyer_product')
        date = data.get('date')

        #stores a blank field and if not field throws an error
        Missing_fields = []
        if not buyer_name:
             Missing_fields('buyer_name')
        if not buyer_product:
             Missing_fields('buyer_product')
        if not date:
             Missing_fields('data')

        if Missing_fields:
            return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400
        
        if History:
             return jsonify({'message': 'history stored successfuly'}), 201
        else:
             return jsonify({'message': 'Error, could not update history'}), 400



@app.route('/gethistory', methods=['GET'])
def gethistory():
     
     data = request.args
     buyer_name = request.args.get('buyer_name')
     buyer_product = request.args.get('buyer_product')
     date = request.args.get('date')
     

     #stores a blank field and if not field throws an error
     Missing_fields = []
     if not buyer_name:
          Missing_fields('buyer_name')
     if not buyer_product:
          Missing_fields('buyer_product')
     if not date:
          Missing_fields('date')

     if Missing_fields:
          return jsonify({"Error": f"missing_fields: {Missing_fields}"}), 400
     
    
    
     #Filters the history with buyer_name
     history = History.query.filter_by(buyer_name=buyer_name).first()
     if History:
          return jsonify({  'message': 'Data retrieved',
                            'buyer_name': buyer_name,
                            'buyer_product': buyer_product,
                            'date': data
                                 
     }), 200
     else:
          return jsonify({'message': 'Error, could not retrieve history'}), 400
     


@app.route('/logout', methods=['DELETE'])
def logout():
     data = request.args.delete
     firstname = request.args.delete('fname')
     lastname = request.args.delete('lname')
     email = request.args.delete('email')
     password = request.args.delete('password')

     Missing_fields = []
     if not firstname:
          Missing_fields('firstname')
     if not lastname:
          Missing_fields('lastname')
     if not email:
          Missing_fields('email')
     if not password:
          Missing_fields('password')

     if Missing_fields:
          return ((Missing_fields, ['Missing_fields']))
     
     if (firstname and lastname and email and password):
          return jsonify({'Message': 'Credentials deleted successfuly'})
     else:
          return jsonify({'Message': 'Credentials can not be deleted'})


@app.route('/logdel', methods=['DELETE'])
def logdel():
     data = request.data.delete
     firstname = data.delete('fname')
     lastname = data.delete('lname')
     email = data.delete('email')
     password = data.delete('password')

     Missing_fields = []

     if not firstname:
          Missing_fields('firstname')
     if not lastname:
          Missing_fields('lastname')
     if not email:
          Missing_fields('email')
     if not password:
          Missing_fields('password')

     if Missing_fields:
          return jsonify({Missing_fields: 'missing_fields'})



     if  (firstname and lastname and email and password):
          return ('message': 'information deleted successfuly')
     else:
          return ('message': 'information could not be delete')




          
     
             
    

    
#this allows sqlalchemy to find data and create data according to your db.Model
with app.app_context():
    db.create_all()

(__name__) == ('__main__')
app.run(debug=True)
