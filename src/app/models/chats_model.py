from . import db

class ChatLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    message = db.Column(db.String(200))
    response = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    # Other fields as necessary
