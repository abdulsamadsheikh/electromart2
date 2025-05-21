import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(basedir)), '.env')

dotenv_path = os.path.join(os.path.dirname(basedir), '.env')


if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}. Attempted from basedir: {basedir}")


class Config:  
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-default-fallback-secret-key-is-not-secure'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db') # Fallback
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']