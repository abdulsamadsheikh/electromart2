from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_session import Session
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure server-side session storage
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')
    app.config['SESSION_PERMANENT'] = False
    Session(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models and routes
    from app.models import AppUser
    
    @login_manager.user_loader
    def load_user(user_id):
        return AppUser.query.get(int(user_id))

    from app.routes import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Roll back the session in case of database errors
        return render_template('errors/500.html'), 500

    return app