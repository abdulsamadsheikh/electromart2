from app import create_app, db
from app.models import Product, Category, Brand
import os
from datetime import datetime

def add_products():
    """Add more products to the database."""
    app = create_app()
    with app.app_context():
        # Create static/images directory if it doesn't exist
        static_dir = os.path.join(app.root_path, 'static')
        images_dir = os.path.join(static_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)

        # Get existing categories and brands
        categories = {cat.Name: cat.CategoryID for cat in Category.query.all()}
        brands = {brand.Name: brand.BrandID for brand in Brand.query.all()}

        # New products to add
        new_products = [
            {
                'name': 'TechPro UltraBook',
                'description': '14-inch ultrabook with 16GB RAM and 512GB SSD',
                'price': 1499.99,
                'stock': 30,
                'category': 'Laptops',
                'brand': 'TechPro',
                'image': 'ultrabook.jpg'
            },
            {
                'name': 'SmartGear Phone Pro',
                'description': 'Flagship smartphone with 256GB storage',
                'price': 1099.99,
                'stock': 50,
                'category': 'Smartphones',
                'brand': 'SmartGear',
                'image': 'phone_pro.jpg'
            },
            {
                'name': 'AudioMax Studio Headphones',
                'description': 'Professional studio headphones with noise cancellation',
                'price': 299.99,
                'stock': 40,
                'category': 'Audio',
                'brand': 'AudioMax',
                'image': 'studio_headphones.jpg'
            },
            {
                'name': 'PowerTech Wireless Charger',
                'description': 'Fast wireless charging pad with cooling system',
                'price': 79.99,
                'stock': 100,
                'category': 'Accessories',
                'brand': 'PowerTech',
                'image': 'wireless_charger.jpg'
            },
            {
                'name': 'TechPro Gaming Laptop',
                'description': '17-inch gaming laptop with RTX 3080',
                'price': 2499.99,
                'stock': 20,
                'category': 'Laptops',
                'brand': 'TechPro',
                'image': 'gaming_laptop.jpg'
            }
        ]

        # Add products
        for product_data in new_products:
            # Check if product already exists
            existing_product = Product.query.filter_by(Name=product_data['name']).first()
            if existing_product:
                print(f"Product '{product_data['name']}' already exists. Skipping...")
                continue

            # Create new product
            product = Product(
                Name=product_data['name'],
                Description=product_data['description'],
                Price=product_data['price'],
                StockQuantity=product_data['stock'],
                CategoryID=categories[product_data['category']],
                BrandID=brands[product_data['brand']],
                ImageURL=product_data['image'],
                DateAdded=datetime.utcnow(),
                LastUpdated=datetime.utcnow()
            )
            db.session.add(product)
            print(f"Added product: {product_data['name']}")

        try:
            db.session.commit()
            print("\nProducts added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding products: {str(e)}")

if __name__ == '__main__':
    add_products() 