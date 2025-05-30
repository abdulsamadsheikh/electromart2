from app import create_app, db
from app.models import Category, Brand, AppUser, Product, CustomerOrder, OrderItem, Payment
from config import config
import os

# Use production config if FLASK_ENV is set to production
app = create_app(config['production'] if os.environ.get('FLASK_ENV') == 'production' else config['development'])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)