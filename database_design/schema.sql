DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS brands CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

CREATE TABLE categories (
    CategoryID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT
);
COMMENT ON TABLE categories IS 'Represents different categories of electronic products.';
COMMENT ON COLUMN categories.CategoryID IS 'Unique identifier for the category (e.g., 1, 2, 3...).';
COMMENT ON COLUMN categories.Name IS 'Name of the category (e.g., "Smartphones", "Laptops"). Must be unique.';
COMMENT ON COLUMN categories.Description IS 'A brief description of the category.';

CREATE TABLE brands (
    BrandID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT
);
COMMENT ON TABLE brands IS 'Represents the brands or manufacturers of electronic products.';
COMMENT ON COLUMN brands.BrandID IS 'Unique identifier for the brand (e.g., 1, 2, 3...).';
COMMENT ON COLUMN brands.Name IS 'Name of the brand (e.g., "Apple", "Samsung"). Must be unique.';
COMMENT ON COLUMN brands.Description IS 'A brief description of the brand.';

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
COMMENT ON TABLE users IS 'Represents users (customers) of the website.';
COMMENT ON COLUMN users.UserID IS 'Unique identifier for the user.';
COMMENT ON COLUMN users.Username IS 'Unique username for login.';
COMMENT ON COLUMN users.PasswordHash IS 'Hashed version of the users password.';
COMMENT ON COLUMN users.Email IS 'Users email address (must be unique).';
COMMENT ON COLUMN users.RegistrationDate IS 'Timestamp when the user registered.';

CREATE TABLE products (
    ProductID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    Price NUMERIC(10, 2) NOT NULL,
    StockQuantity INTEGER NOT NULL DEFAULT 0,
    CategoryID INTEGER NOT NULL,
    BrandID INTEGER NOT NULL,
    ImageURL VARCHAR(255),
    DateAdded TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    LastUpdated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_category FOREIGN KEY (CategoryID) REFERENCES categories(CategoryID),
    CONSTRAINT fk_brand FOREIGN KEY (BrandID) REFERENCES brands(BrandID)
);
COMMENT ON TABLE products IS 'Represents the electronic products available for sale.';
COMMENT ON COLUMN products.ProductID IS 'Unique identifier for the product.';
COMMENT ON COLUMN products.Price IS 'Selling price of the product.';
COMMENT ON COLUMN products.StockQuantity IS 'Number of units currently in stock.';
COMMENT ON COLUMN products.CategoryID IS 'Foreign key linking to the categories table.';
COMMENT ON COLUMN products.BrandID IS 'Foreign key linking to the brands table.';
COMMENT ON COLUMN products.DateAdded IS 'Timestamp when the product was added.';
COMMENT ON COLUMN products.LastUpdated IS 'Timestamp when the product was last updated.';

CREATE TABLE orders (
    OrderID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    OrderDate TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    TotalAmount NUMERIC(12, 2) NOT NULL,
    Status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    ShippingAddressLine1 VARCHAR(255) NOT NULL,
    ShippingAddressLine2 VARCHAR(255),
    ShippingCity VARCHAR(100) NOT NULL,
    ShippingPostalCode VARCHAR(20) NOT NULL,
    ShippingCountry VARCHAR(50) NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (UserID) REFERENCES users(UserID)
);
COMMENT ON TABLE orders IS 'Represents individual orders placed by users.';
COMMENT ON COLUMN orders.OrderID IS 'Unique identifier for the order.';
COMMENT ON COLUMN orders.UserID IS 'Foreign key linking to the user who placed the order.';
COMMENT ON COLUMN orders.TotalAmount IS 'Total monetary value of the order.';
COMMENT ON COLUMN orders.Status IS 'Current status of the order (e.g., Pending, Shipped).';

CREATE TABLE order_items (
    OrderItemID SERIAL PRIMARY KEY,
    OrderID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    UnitPrice NUMERIC(10, 2) NOT NULL,
    Subtotal NUMERIC(12, 2) NOT NULL,
    CONSTRAINT fk_order FOREIGN KEY (OrderID) REFERENCES orders(OrderID) ON DELETE CASCADE,
    CONSTRAINT fk_product FOREIGN KEY (ProductID) REFERENCES products(ProductID),
    CONSTRAINT uq_order_product UNIQUE (OrderID, ProductID)
);
COMMENT ON TABLE order_items IS 'Represents the line items included in each order.';
COMMENT ON COLUMN order_items.OrderItemID IS 'Unique identifier for the order item entry.';
COMMENT ON COLUMN order_items.OrderID IS 'Foreign key linking to the orders table.';
COMMENT ON COLUMN order_items.ProductID IS 'Foreign key linking to the products table.';
COMMENT ON COLUMN order_items.Quantity IS 'Number of units of this product in the order.';
COMMENT ON COLUMN order_items.UnitPrice IS 'Price per unit at the time of order.';
COMMENT ON COLUMN order_items.Subtotal IS 'Calculated as Quantity * UnitPrice.';

CREATE TABLE payments (
    PaymentID SERIAL PRIMARY KEY,
    OrderID INTEGER NOT NULL UNIQUE,
    PaymentDate TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PaymentMethod VARCHAR(50) NOT NULL,
    Amount NUMERIC(12, 2) NOT NULL,
    Status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    TransactionID VARCHAR(255) UNIQUE,
    CONSTRAINT fk_payment_order FOREIGN KEY (OrderID) REFERENCES orders(OrderID) ON DELETE CASCADE
);
COMMENT ON TABLE payments IS 'Represents payments made for orders.';
COMMENT ON COLUMN payments.PaymentID IS 'Unique identifier for the payment.';
COMMENT ON COLUMN payments.OrderID IS 'Foreign key linking to the orders table.';
COMMENT ON COLUMN payments.PaymentMethod IS 'Method used for payment.';
COMMENT ON COLUMN payments.Amount IS 'Amount paid.';
COMMENT ON COLUMN payments.Status IS 'Status of the payment (e.g., Pending, Completed).';
COMMENT ON COLUMN payments.TransactionID IS 'Unique transaction identifier from the payment gateway, if applicable.';

-- Create indexes for better performance
CREATE INDEX idx_products_category ON products(CategoryID);
CREATE INDEX idx_products_brand ON products(BrandID);
CREATE INDEX idx_orders_user ON orders(UserID);
CREATE INDEX idx_order_items_order ON order_items(OrderID);
CREATE INDEX idx_order_items_product ON order_items(ProductID);
CREATE INDEX idx_payments_order ON payments(OrderID);