from app import create_app, db
from app.models import Category, Brand, AppUser, Product, CustomerOrder, OrderItem, Payment

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)