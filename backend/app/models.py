from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from backend.app import db, login_manager # Import db and login_manager

# User loader function required by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(AppUser, int(user_id)) # Use db.session.get for SQLAlchemy 2.0+

class Category(db.Model):
    __tablename__ = 'category' # Should match your PostgreSQL table name (typically lowercase)
    categoryid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    products = db.relationship('Product', backref='category', lazy='dynamic') # 'dynamic' for query building

    def __repr__(self):
        return f"<Category {self.name}>"

class Brand(db.Model):
    __tablename__ = 'brand'
    brandid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    products = db.relationship('Product', backref='brand', lazy='dynamic')

    def __repr__(self):
        return f"<Brand {self.name}>"

class AppUser(UserMixin, db.Model): # Inherit from UserMixin
    __tablename__ = 'appuser'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    passwordhash = db.Column(db.String(255), nullable=False) # Increased length for future hash algorithms
    email = db.Column(db.String(100), nullable=False, unique=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    addressline1 = db.Column(db.String(255))
    addressline2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    postalcode = db.Column(db.String(20))
    country = db.Column(db.String(50))
    phonenumber = db.Column(db.String(20))
    registrationdate = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    orders = db.relationship('CustomerOrder', backref='user', lazy='dynamic')

    # For UserMixin, Flask-Login needs an 'id' property.
    # Our primary key is 'userid', so we can alias it or Flask-Login might pick it up.
    # Explicitly, you can do:
    def get_id(self):
        return str(self.userid)

    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

    def __repr__(self):
        return f"<AppUser {self.username}>"

class Product(db.Model):
    __tablename__ = 'product'
    productid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False) # Add Check constraint in DB
    stockquantity = db.Column(db.Integer, nullable=False, default=0) # Add Check constraint in DB
    categoryid = db.Column(db.Integer, db.ForeignKey('category.categoryid'), nullable=False)
    brandid = db.Column(db.Integer, db.ForeignKey('brand.brandid'), nullable=False)
    imageurl = db.Column(db.String(255))
    dateadded = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    lastupdated = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # category = db.relationship('Category', backref='products') # Handled by backref in Category
    # brand = db.relationship('Brand', backref='products') # Handled by backref in Brand
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')

    def __repr__(self):
        return f"<Product {self.name}>"

class CustomerOrder(db.Model):
    __tablename__ = 'customerorder'
    orderid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('appuser.userid'), nullable=False)
    orderdate = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    totalamount = db.Column(db.Numeric(12, 2), nullable=False) # Add Check constraint in DB
    status = db.Column(db.String(50), nullable=False, default='Pending')
    shippingaddressline1 = db.Column(db.String(255), nullable=False)
    shippingaddressline2 = db.Column(db.String(255))
    shippingcity = db.Column(db.String(100), nullable=False)
    shippingpostalcode = db.Column(db.String(20), nullable=False)
    shippingcountry = db.Column(db.String(50), nullable=False)

    # user = db.relationship('AppUser', backref='orders') # Handled by backref in AppUser
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan') # One-to-one

    def __repr__(self):
        return f"<CustomerOrder {self.orderid}>"

class OrderItem(db.Model):
    __tablename__ = 'orderitem'
    orderitemid = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer, db.ForeignKey('customerorder.orderid', ondelete='CASCADE'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid', ondelete='RESTRICT'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False) # Add Check constraint in DB
    unitprice = db.Column(db.Numeric(10, 2), nullable=False) # Add Check constraint in DB
    subtotal = db.Column(db.Numeric(12, 2), nullable=False) # Add Check constraint in DB

    # order = db.relationship('CustomerOrder', backref='items') # Handled by backref in CustomerOrder
    # product = db.relationship('Product', backref='order_items') # Handled by backref in Product

    # To enforce uniqueness of (orderid, productid) at the model/app level if desired,
    # or rely on the DB constraint already defined in schema.sql
    __table_args__ = (db.UniqueConstraint('orderid', 'productid', name='uq_order_product_sa'),)


    def __repr__(self):
        return f"<OrderItem {self.orderitemid} (Order: {self.orderid}, Product: {self.productid})>"

class Payment(db.Model):
    __tablename__ = 'payment'
    paymentid = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer, db.ForeignKey('customerorder.orderid', ondelete='CASCADE'), nullable=False, unique=True)
    paymentdate = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    paymentmethod = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False) # Add Check constraint in DB
    status = db.Column(db.String(50), nullable=False, default='Pending')
    transactionid = db.Column(db.String(255), unique=True, nullable=True) # Nullable because it might not always exist

    # order = db.relationship('CustomerOrder', backref='payment') # Handled by backref in CustomerOrder

    def __repr__(self):
        return f"<Payment {self.paymentid} for Order {self.orderid}>"