from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'category'

    CategoryID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False, unique=True)
    Description = db.Column(db.Text)

    products = db.relationship('Product', backref='category', lazy=True)

class Brand(db.Model):
    __tablename__ = 'brand'

    BrandID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False, unique=True)
    Description = db.Column(db.Text)

    products = db.relationship('Product', backref='brand', lazy=True)

class AppUser(db.Model):
    __tablename__ = 'appuser'

    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    PasswordHash = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    AddressLine1 = db.Column(db.String(255))
    AddressLine2 = db.Column(db.String(255))
    City = db.Column(db.String(100))
    PostalCode = db.Column(db.String(20))
    Country = db.Column(db.String(50))
    PhoneNumber = db.Column(db.String(20))
    RegistrationDate = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    orders = db.relationship('CustomerOrder', backref='user', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'

    ProductID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Price = db.Column(db.Numeric(10, 2), nullable=False)
    StockQuantity = db.Column(db.Integer, nullable=False, default=0)
    CategoryID = db.Column(db.Integer, db.ForeignKey('category.CategoryID'), nullable=False)
    BrandID = db.Column(db.Integer, db.ForeignKey('brand.BrandID'), nullable=False)
    ImageURL = db.Column(db.String(255))
    DateAdded = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    LastUpdated = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class CustomerOrder(db.Model):
    __tablename__ = 'customerorder'

    OrderID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('appuser.UserID'), nullable=False)
    OrderDate = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    TotalAmount = db.Column(db.Numeric(12, 2), nullable=False)
    Status = db.Column(db.String(50), nullable=False, default='Pending')
    ShippingAddressLine1 = db.Column(db.String(255), nullable=False)
    ShippingAddressLine2 = db.Column(db.String(255))
    ShippingCity = db.Column(db.String(100), nullable=False)
    ShippingPostalCode = db.Column(db.String(20), nullable=False)
    ShippingCountry = db.Column(db.String(50), nullable=False)

    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    payment = db.relationship('Payment', uselist=False, backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'orderitem'

    OrderItemID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('customerorder.OrderID', ondelete="CASCADE"), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ProductID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    UnitPrice = db.Column(db.Numeric(10, 2), nullable=False)
    Subtotal = db.Column(db.Numeric(12, 2), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('OrderID', 'ProductID', name='uq_order_product'),
    )

class Payment(db.Model):
    __tablename__ = 'payment'

    PaymentID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('customerorder.OrderID', ondelete="CASCADE"), nullable=False, unique=True)
    PaymentDate = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    PaymentMethod = db.Column(db.String(50), nullable=False)
    Amount = db.Column(db.Numeric(12, 2), nullable=False)
    Status = db.Column(db.String(50), nullable=False, default='Pending')
    TransactionID = db.Column(db.String(255), unique=True)
