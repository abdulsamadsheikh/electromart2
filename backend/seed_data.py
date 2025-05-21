from app import create_app, db
from app.models import AppUser, Product, Category, Brand, CustomerOrder, OrderItem
from werkzeug.security import generate_password_hash
import datetime

def seed_data():
    """Populate database with sample data."""
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create categories
        categories = [
            Category(Name='Laptops', Description='Portable computers for work and play'),
            Category(Name='Smartphones', Description='Latest mobile devices'),
            Category(Name='Accessories', Description='Essential gadget accessories'),
            Category(Name='Audio', Description='Headphones and speakers')
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Create brands
        brands = [
            Brand(Name='TechPro', Description='Premium technology products'),
            Brand(Name='SmartGear', Description='Innovative smart devices'),
            Brand(Name='AudioMax', Description='High-quality audio equipment'),
            Brand(Name='PowerTech', Description='Reliable power accessories')
        ]
        db.session.add_all(brands)
        db.session.commit()

        # Create admin user
        admin = AppUser(
            Username='admin',
            Email='admin@electromart.com',
            PasswordHash=generate_password_hash('admin123'),
            FirstName='Admin',
            LastName='User',
            AddressLine1='123 Admin Street',
            City='Admin City',
            PostalCode='12345',
            Country='Norway'
        )
        db.session.add(admin)
        db.session.commit()

        # Create sample products
        products = [
            Product(
                Name='TechPro Laptop Pro',
                Description='15-inch professional laptop with latest processor',
                Price=1299.99,
                StockQuantity=50,
                CategoryID=1,
                BrandID=1,
                ImageURL='laptop_pro.jpg'
            ),
            Product(
                Name='SmartGear Phone X',
                Description='Latest smartphone with 5G capability',
                Price=899.99,
                StockQuantity=100,
                CategoryID=2,
                BrandID=2,
                ImageURL='phone_x.jpg'
            ),
            Product(
                Name='AudioMax Wireless Headphones',
                Description='Premium noise-canceling headphones',
                Price=249.99,
                StockQuantity=75,
                CategoryID=4,
                BrandID=3,
                ImageURL='headphones.jpg'
            ),
            Product(
                Name='PowerTech Fast Charger',
                Description='65W USB-C fast charger',
                Price=49.99,
                StockQuantity=200,
                CategoryID=3,
                BrandID=4,
                ImageURL='charger.jpg'
            )
        ]
        db.session.add_all(products)
        db.session.commit()

        print("Sample data has been successfully added to the database!")

if __name__ == '__main__':
    seed_data() 