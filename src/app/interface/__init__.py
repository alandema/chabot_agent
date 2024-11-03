from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# from app.models import User
# from app import routes  # noqa

file_path = os.path.abspath(os.getcwd())+"\\src\\app\\users.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


