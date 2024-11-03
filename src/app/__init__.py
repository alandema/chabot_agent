from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


file_path = os.path.abspath(os.getcwd())+"\\src\\todo.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)


app.app_context().push()

db.create_all()

from app import routes  # noqa
