from flask import Flask
from config import Config
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Import routes from main and chatbot logic
    with app.app_context():
        db.create_all(bind_key='userdb')
        db.create_all(bind_key='chatdb')  # This will create tables for all models in all connected databases
        from .main import routes  # Importing routes to register them

    return app