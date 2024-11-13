import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_BINDS = {
        'userdb': 'sqlite:///userdb.db',
        'chatdb': 'sqlite:///chatdb.db'
    }
