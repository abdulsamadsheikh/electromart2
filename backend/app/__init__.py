from flask import Flask
from backend.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager() # Initialize LoginManager
login_manager.login_view = 'auth_routes.login' # Tell Flask-Login where the login page is
login_manager.login_message_category = 'info' # Optional: for styling flashed messages

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app) # Configure LoginManager for the app

    from backend.app.routes import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)

    from backend.app.auth import bp as auth_routes_bp
    app.register_blueprint(auth_routes_bp, url_prefix='/auth')


    return app