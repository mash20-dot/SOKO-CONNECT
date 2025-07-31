import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_jwt_extended import JWTManager
from main.models import db
from flask_sqlalchemy import SQLAlchemy
import pymysql

#Importing blueprints
from major.route import major
from logout.log import logout as logout_blueprint
from buyerhistory.history import buyerhistory
from item.items import item
from add.min import add

#Telling python to use pymysql as a replacement for MySQLdb
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# JWT Secret Key
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-default-secret')

#setting up MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# This disables SQLAlchemy's event system for tracking object modifications (saves memory and avoids warnings)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Initializing extensions
db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(major, url_prefix='/major')
app.register_blueprint(logout_blueprint, url_prefix='/logout')
app.register_blueprint(buyerhistory, url_prefix='/buyerhistory')
app.register_blueprint(item, url_prefix='/item')
app.register_blueprint(add, url_prefix='/add')

# Create all tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)


