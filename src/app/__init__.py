from flask import Flask
from config import Config
from .models import db
from flask_login import LoginManager
from .models.user_model import Users

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
    
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app