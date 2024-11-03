from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# from .models import User
# from .routes import *

file_path = os.path.abspath(os.getcwd())+"\\src\\app\\users.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()