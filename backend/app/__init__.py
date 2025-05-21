from flask import Flask, render_template
from config import Config
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

    from app.routes import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)

    from app.auth import bp as auth_routes_bp
    app.register_blueprint(auth_routes_bp, url_prefix='/auth')

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Roll back the session in case of database errors
        return render_template('errors/500.html'), 500

    # Ensure models are known to the app
    with app.app_context():
        from . import models # This line imports your models.py

    return app