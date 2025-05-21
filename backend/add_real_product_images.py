import os
import requests
from app import create_app, db
from app.models import Product

def download_image(url, filename, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")
        return False

def add_real_product_images():
    app = create_app()
    with app.app_context():
        # Create images directory if it doesn't exist
        static_dir = os.path.join(app.root_path, 'static')
        images_dir = os.path.join(static_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)

        # Dictionary of product images with real URLs
        product_images = {
            'laptop1.jpg': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853',
            'laptop2.jpg': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8',
            'phone1.jpg': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9',
            'phone2.jpg': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9',
            'headphones1.jpg': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e',
            'headphones2.jpg': 'https://images.unsplash.com/photo-1572536147248-ac59a8abfa4b',
            'charger1.jpg': 'https://images.unsplash.com/photo-1605464315542-bda3e2f4e605',
            'charger2.jpg': 'https://images.unsplash.com/photo-1605464315542-bda3e2f4e605',
            'gaming_laptop.jpg': 'https://images.unsplash.com/photo-1593640408182-31c70c8268f7',
            'ultrabook.jpg': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853'
        }

        # Download each image
        for filename, url in product_images.items():
            save_path = os.path.join(images_dir, filename)
            if not os.path.exists(save_path):
                if download_image(url, filename, save_path):
                    # Update product image URL in database
                    product = Product.query.filter_by(ImageURL=filename).first()
                    if product:
                        product.ImageURL = filename
                        db.session.commit()
                        print(f"Updated product image URL for {product.Name}")
            else:
                print(f"Image {filename} already exists")

if __name__ == '__main__':
    add_real_product_images() 