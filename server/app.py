from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os



app = Flask(__name__)


#database structure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sokoconnect.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    firstname = db.Column(db.String(50),)
    lastname = db.Column(db.String(50),)
    email = db.Column(db.String(150), unique=True,)
    password = db.Column(db.String(150),)


#signup route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstname = data.get('fname')
    lastname = data.get('lname')
    email = data.get('email')
    password = data.get('password')


     #checks for every empty space and save it if none of that empty space is not provided it throws that error
    missing_fields= []

    if not firstname:
        missing_fields.append(firstname)
    if not lastname:
        missing_fields.append(lastname)
    if not email:
        missing_fields.append(email)
    if not password:
        missing_fields.append(password)
        return jsonify({'Error': f'missing_fields: "join"{(missing_fields)}'}), 400
    

    #Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409
    


     #hash the password, making it invisible
    hashed_password = generate_password_hash(password)


      #saves user info in the database
    new_user = User(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
   
    
    if (firstname and lastname and email and password):
        return jsonify({'message': 'successfully signed up'}), 201


    if not (firstname and lastname and email and password):
        return jsonify({'message': 'Invalid credentials, fill all blank spaces'}), 400
    
   

     
   


#this allows sqlalchemy to find data and create data according to your db.Model
with app.app_context():
    db.create_all()

(__name__) == ('__main__')
app.run(debug=True)
