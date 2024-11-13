from . import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    __bind_key__ = 'userdb'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    # Other fields as necessary
    def get_id(self):
        return str(self.id)