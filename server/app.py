from flask import Flask
from flask_jwt_extended import JWTManager
from models import db

#from auth.route import auth as auth_blueprint
from logout.log import logout as logout_blueprint
from buyerhistory.history import buyerhistory
from item.items import item
from add.min import add

from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

# JWT Secret Key
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-default-secret')

# Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sokoconnect.db'

# Initializing extensions
db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
#app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(logout_blueprint, url_prefix='/logout')
app.register_blueprint(buyerhistory, url_prefix='/buyerhistory')
app.register_blueprint(item, url_prefix='/item')
app.register_blueprint(add, url_prefix='/add')

# Create all tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
