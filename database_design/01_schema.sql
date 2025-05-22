-- Database Schema for ElectroMart E-commerce Platform

-- Drop tables if they exist (in correct order due to dependencies)
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS categories;

-- Categories Table
CREATE TABLE categories (
    CategoryID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT
);

-- Brands Table
CREATE TABLE brands (
    BrandID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT
);

-- Users Table
CREATE TABLE users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    AddressLine1 VARCHAR(255),
    AddressLine2 VARCHAR(255),
    City VARCHAR(100),
    PostalCode VARCHAR(20),
    Country VARCHAR(50),
    PhoneNumber VARCHAR(20),
    RegistrationDate TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Products Table
CREATE TABLE products (
    ProductID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    Price NUMERIC(10,2) NOT NULL CHECK (Price > 0),
    StockQuantity INTEGER NOT NULL DEFAULT 0 CHECK (StockQuantity >= 0),
    CategoryID INTEGER NOT NULL REFERENCES categories(CategoryID),
    BrandID INTEGER NOT NULL REFERENCES brands(BrandID),
    ImageURL VARCHAR(255),
    DateAdded TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    LastUpdated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Orders Table
CREATE TABLE orders (
    OrderID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL REFERENCES users(UserID),
    OrderDate TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    TotalAmount NUMERIC(12,2) NOT NULL CHECK (TotalAmount >= 0),
    Status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    ShippingAddressLine1 VARCHAR(255) NOT NULL,
    ShippingAddressLine2 VARCHAR(255),
    ShippingCity VARCHAR(100) NOT NULL,
    ShippingPostalCode VARCHAR(20) NOT NULL,
    ShippingCountry VARCHAR(50) NOT NULL,
    CONSTRAINT valid_status CHECK (Status IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'))
);

-- Order Items Table
CREATE TABLE order_items (
    OrderItemID SERIAL PRIMARY KEY,
    OrderID INTEGER NOT NULL REFERENCES orders(OrderID),
    ProductID INTEGER NOT NULL REFERENCES products(ProductID),
    Quantity INTEGER NOT NULL CHECK (Quantity > 0),
    UnitPrice NUMERIC(10,2) NOT NULL CHECK (UnitPrice >= 0),
    Subtotal NUMERIC(12,2) NOT NULL CHECK (Subtotal >= 0),
    CONSTRAINT uq_order_product UNIQUE(OrderID, ProductID)
);

-- Payments Table
CREATE TABLE payments (
    PaymentID SERIAL PRIMARY KEY,
    OrderID INTEGER NOT NULL REFERENCES orders(OrderID) UNIQUE,
    PaymentDate TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PaymentMethod VARCHAR(50) NOT NULL,
    Amount NUMERIC(12,2) NOT NULL CHECK (Amount > 0),
    Status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    TransactionID VARCHAR(255) UNIQUE,
    CONSTRAINT valid_payment_status CHECK (Status IN ('Pending', 'Processing', 'Completed', 'Failed', 'Refunded')),
    CONSTRAINT valid_payment_method CHECK (PaymentMethod IN ('Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer'))
);

-- Create Indexes for Performance Optimization
CREATE INDEX idx_products_category ON products(CategoryID);
CREATE INDEX idx_products_brand ON products(BrandID);
CREATE INDEX idx_orders_user ON orders(UserID);
CREATE INDEX idx_order_items_order ON order_items(OrderID);
CREATE INDEX idx_order_items_product ON order_items(ProductID);
CREATE INDEX idx_payments_order ON payments(OrderID);

-- Create Index on frequently searched product attributes
CREATE INDEX idx_products_name ON products(Name);
CREATE INDEX idx_products_price ON products(Price);
CREATE INDEX idx_products_stock ON products(StockQuantity);

-- Create Index for user lookups
CREATE INDEX idx_users_email ON users(Email);
CREATE INDEX idx_users_username ON users(Username); 