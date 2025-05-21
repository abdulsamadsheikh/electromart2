import os
import requests
from app import create_app

def download_image(url, filename, save_path):
    """Download an image from URL and save it to the specified path."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        file_path = os.path.join(save_path, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")
        return False

def add_product_images():
    """Download and add product images."""
    app = create_app()
    with app.app_context():
        # Create static/images directory if it doesn't exist
        static_dir = os.path.join(app.root_path, 'static')
        images_dir = os.path.join(static_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)

        # Sample product images (using placeholder images)
        product_images = {
            'ultrabook.jpg': 'https://picsum.photos/800/600?random=1',
            'phone_pro.jpg': 'https://picsum.photos/800/600?random=2',
            'studio_headphones.jpg': 'https://picsum.photos/800/600?random=3',
            'wireless_charger.jpg': 'https://picsum.photos/800/600?random=4',
            'gaming_laptop.jpg': 'https://picsum.photos/800/600?random=5',
            'laptop_pro.jpg': 'https://picsum.photos/800/600?random=6',
            'phone_x.jpg': 'https://picsum.photos/800/600?random=7',
            'headphones.jpg': 'https://picsum.photos/800/600?random=8',
            'charger.jpg': 'https://picsum.photos/800/600?random=9'
        }

        # Download images
        for filename, url in product_images.items():
            if not os.path.exists(os.path.join(images_dir, filename)):
                download_image(url, filename, images_dir)
            else:
                print(f"Image already exists: {filename}")

if __name__ == '__main__':
    add_product_images() 