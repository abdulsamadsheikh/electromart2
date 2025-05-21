from flask import session
from flask_login import current_user
from decimal import Decimal

class Cart:
    @staticmethod
    def _get_cart_key():
        """Get the cart session key for the current user."""
        if current_user.is_authenticated:
            return f'cart_{current_user.UserID}'
        return 'cart_anonymous'

    @staticmethod
    def get_cart():
        """Get the current cart from session."""
        cart_key = Cart._get_cart_key()
        return session.get(cart_key, {})

    @staticmethod
    def save_cart(cart):
        """Save the cart to session."""
        cart_key = Cart._get_cart_key()
        session[cart_key] = cart

    @staticmethod
    def add_item(product, quantity=1):
        """Add an item to the cart."""
        cart = Cart.get_cart()
        product_id = str(product.ProductID)

        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {
                'quantity': quantity,
                'price': float(product.Price),
                'name': product.Name,
                'image_url': product.ImageURL
            }

        # Ensure we don't exceed available stock
        cart[product_id]['quantity'] = min(cart[product_id]['quantity'], product.StockQuantity)
        Cart.save_cart(cart)

    @staticmethod
    def update_item(product_id, quantity):
        """Update item quantity in cart."""
        cart = Cart.get_cart()
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity
            Cart.save_cart(cart)

    @staticmethod
    def remove_item(product_id):
        """Remove an item from cart."""
        cart = Cart.get_cart()
        if str(product_id) in cart:
            del cart[str(product_id)]
            Cart.save_cart(cart)

    @staticmethod
    def get_total():
        """Calculate total price of cart."""
        cart = Cart.get_cart()
        total = Decimal('0.00')
        for item in cart.values():
            total += Decimal(str(item['price'])) * item['quantity']
        return total

    @staticmethod
    def get_items_with_products(Product):
        """Get cart items with their corresponding product objects."""
        cart = Cart.get_cart()
        items = []
        total = Decimal('0.00')

        for product_id, item in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                quantity = min(item['quantity'], product.StockQuantity)
                subtotal = Decimal(str(product.Price)) * quantity
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                total += subtotal

        return items, total

    @staticmethod
    def clear():
        """Clear the cart."""
        cart_key = Cart._get_cart_key()
        session.pop(cart_key, None) 