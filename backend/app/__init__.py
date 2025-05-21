from flask import Flask
from backend.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

db = SQLAlchemy()
migrate = Migrate() # Define once
login_manager = LoginManager()
login_manager.login_view = 'auth_routes.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db) # Initialize once with the app instance
    login_manager.init_app(app)

    from backend.app.routes import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)

    from backend.app.auth import bp as auth_routes_bp
    app.register_blueprint(auth_routes_bp, url_prefix='/auth')

    # Ensure models are known to the app
    with app.app_context():
        from . import models # This line imports your models.py

    return app