from app import create_app, db
from app.models import User, Product, Category, Brand, Order, OrderItem
from werkzeug.security import generate_password_hash
import datetime

def seed_data():
    """Populate database with sample data."""
    app = create_app()
    with app.app_context():
        # Create categories
        categories = [
            Category(name='Laptops', description='Portable computers for work and play'),
            Category(name='Smartphones', description='Latest mobile devices'),
            Category(name='Accessories', description='Essential gadget accessories'),
            Category(name='Audio', description='Headphones and speakers')
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Create brands
        brands = [
            Brand(name='TechPro', description='Premium technology products'),
            Brand(name='SmartGear', description='Innovative smart devices'),
            Brand(name='AudioMax', description='High-quality audio equipment'),
            Brand(name='PowerTech', description='Reliable power accessories')
        ]
        db.session.add_all(brands)
        db.session.commit()

        # Create admin user
        admin = User(
            email='admin@electromart.com',
            password_hash=generate_password_hash('admin123'),
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

        # Create sample products
        products = [
            Product(
                name='TechPro Laptop Pro',
                description='15-inch professional laptop with latest processor',
                price=1299.99,
                stock=50,
                category_id=1,
                brand_id=1,
                image_url='laptop_pro.jpg'
            ),
            Product(
                name='SmartGear Phone X',
                description='Latest smartphone with 5G capability',
                price=899.99,
                stock=100,
                category_id=2,
                brand_id=2,
                image_url='phone_x.jpg'
            ),
            Product(
                name='AudioMax Wireless Headphones',
                description='Premium noise-canceling headphones',
                price=249.99,
                stock=75,
                category_id=4,
                brand_id=3,
                image_url='headphones.jpg'
            ),
            Product(
                name='PowerTech Fast Charger',
                description='65W USB-C fast charger',
                price=49.99,
                stock=200,
                category_id=3,
                brand_id=4,
                image_url='charger.jpg'
            )
        ]
        db.session.add_all(products)
        db.session.commit()

        print("Sample data has been successfully added to the database!")

if __name__ == '__main__':
    seed_data() 