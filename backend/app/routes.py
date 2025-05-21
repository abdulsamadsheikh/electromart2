from flask import Blueprint, render_template, abort, request, url_for, flash, redirect, jsonify
from flask_login import login_required, current_user
from app.models import Product, Category, Brand, CustomerOrder, OrderItem, Payment
from app.cart import Cart
from app import db
from decimal import Decimal

# Create a Blueprint. 'main_routes' is the name of the blueprint.
bp = Blueprint('main_routes', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Renders the homepage."""
    try:
        # Example: Fetch a few featured products or categories for the homepage
        featured_products = Product.query.order_by(Product.DateAdded.desc()).limit(6).all()
    except Exception as e:
        # Log the error e
        flash('Could not load featured products at the moment.', 'warning')
        featured_products = []
    return render_template('index.html', title='Welcome to ElectroMart', featured_products=featured_products)

@bp.route('/products')
def products():
    """Renders the main products listing page. Supports filtering by category."""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    sort = request.args.get('sort', 'name_asc')
    
    query = Product.query
    current_category_name = "All Products"

    if category_id:
        category = Category.query.get_or_404(category_id)
        query = query.filter(Product.CategoryID == category_id)
        current_category_name = category.Name

    # Apply sorting
    if sort == 'name_desc':
        query = query.order_by(Product.Name.desc())
    elif sort == 'price_asc':
        query = query.order_by(Product.Price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.Price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.DateAdded.desc())
    else:  # name_asc
        query = query.order_by(Product.Name.asc())

    try:
        # Example: Paginate products, 12 per page
        products_pagination = query.paginate(page=page, per_page=12, error_out=False)
        products_on_page = products_pagination.items
    except Exception as e:
        # Log the error e
        flash('Could not load products at the moment.', 'warning')
        products_pagination = None
        products_on_page = []

    categories = Category.query.order_by(Category.Name.asc()).all()
    
    return render_template('products.html', 
                           title='Products', 
                           products=products_on_page, 
                           pagination=products_pagination,
                           categories=categories,
                           current_category_name=current_category_name,
                           selected_category_id=category_id)

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Renders the product detail page for a single product."""
    try:
        product = Product.query.get_or_404(product_id)
        # Example: Get related products (e.g., same category, different brand, or simply other products)
        related_products = Product.query.filter(
            Product.CategoryID == product.CategoryID, 
            Product.ProductID != product.ProductID
        ).limit(4).all()
    except Exception as e:
        # Log the error e
        flash('Could not load product details.', 'error')
        return redirect(url_for('main_routes.products'))
        
    return render_template('product_detail.html', title=product.Name, product=product, related_products=related_products)

@bp.route('/category/<int:category_id>')
def products_by_category(category_id):
    """Redirects to the products page filtered by the given category."""
    # This route is essentially a shortcut or clean URL to the filtered products page
    return redirect(url_for('main_routes.products', category_id=category_id))

@bp.route('/cart')
def cart():
    """Renders the shopping cart page."""
    cart_items, total_cart_price = Cart.get_items_with_products(Product)
    return render_template('cart.html', title='Your Shopping Cart', cart_items=cart_items, total_cart_price=total_cart_price)

@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Handles adding a product to the cart."""
    try:
        product = Product.query.get_or_404(product_id)
        quantity = int(request.form.get('quantity', 1))
        
        if quantity > product.StockQuantity:
            flash(f'Sorry, only {product.StockQuantity} units available.', 'warning')
            quantity = product.StockQuantity
        
        Cart.add_item(product, quantity)
        flash(f"'{product.Name}' added to cart.", 'success')
    except Exception as e:
        flash('Could not add item to cart.', 'error')
    
    return redirect(request.referrer or url_for('main_routes.products'))

@bp.route('/update_cart_item/<int:product_id>', methods=['POST'])
def update_cart_item(product_id):
    """Handles updating cart item quantity."""
    action = request.form.get('action')
    product = Product.query.get_or_404(product_id)
    cart = Cart.get_cart()
    
    if str(product_id) in cart:
        current_qty = cart[str(product_id)]['quantity']
        if action == 'increase' and current_qty < product.StockQuantity:
            Cart.update_item(product_id, current_qty + 1)
        elif action == 'decrease' and current_qty > 1:
            Cart.update_item(product_id, current_qty - 1)
    
    return redirect(url_for('main_routes.cart'))

@bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Handles removing an item from the cart."""
    Cart.remove_item(product_id)
    flash('Item removed from cart.', 'success')
    return redirect(url_for('main_routes.cart'))

@bp.route('/checkout')
@login_required
def checkout():
    """Renders the checkout page."""
    cart_items, total_cart_price = Cart.get_items_with_products(Product)
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main_routes.cart'))
    return render_template('checkout.html', title='Checkout', cart_items=cart_items, total_cart_price=total_cart_price)

@bp.route('/process_checkout', methods=['POST'])
@login_required
def process_checkout():
    """Process the checkout and create order."""
    cart_items, total_cart_price = Cart.get_items_with_products(Product)
    
    if not cart_items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('main_routes.cart'))
    
    try:
        # Create order
        order = CustomerOrder(
            UserID=current_user.UserID,
            TotalAmount=total_cart_price,
            Status='Pending',
            ShippingAddressLine1=request.form['shipping_address1'],
            ShippingAddressLine2=request.form.get('shipping_address2', ''),
            ShippingCity=request.form['shipping_city'],
            ShippingPostalCode=request.form['shipping_postal_code'],
            ShippingCountry=request.form['shipping_country']
        )
        db.session.add(order)
        db.session.flush()  # This will generate the OrderID without committing
        
        # Create order items and update stock
        for item in cart_items:
            order_item = OrderItem(
                OrderID=order.OrderID,
                ProductID=item['product'].ProductID,
                Quantity=item['quantity'],
                UnitPrice=item['product'].Price,
                Subtotal=item['subtotal']
            )
            # Update stock quantity
            item['product'].StockQuantity -= item['quantity']
            db.session.add(order_item)
        
        # Create payment record
        payment = Payment(
            OrderID=order.OrderID,
            PaymentMethod='Credit Card',  # In a real app, this would come from payment processor
            Amount=total_cart_price,
            Status='Completed',  # In a real app, this would be pending until confirmed
            TransactionID=f'DEMO-{order.OrderID}'  # In a real app, this would come from payment processor
        )
        db.session.add(payment)
        
        db.session.commit()
        Cart.clear()  # Clear the cart after successful order
        flash('Order placed successfully!', 'success')
        return redirect(url_for('auth.order_history'))
        
    except Exception as e:
        db.session.rollback()
        print('Checkout error:', e)
        flash('Could not process your order. Please try again.', 'error')
        return redirect(url_for('main_routes.checkout'))

# Error handlers
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500