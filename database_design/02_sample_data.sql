-- Sample Data Population for ElectroMart Database

-- Categories
INSERT INTO categories (Name, Description) VALUES
    ('Laptops', 'Portable computers for work and play'),
    ('Smartphones', 'Latest mobile devices'),
    ('Accessories', 'Essential gadget accessories'),
    ('Audio', 'Headphones and speakers'),
    ('Tablets', 'Portable touchscreen devices'),
    ('Cameras', 'Digital cameras and accessories');

-- Brands
INSERT INTO brands (Name, Description) VALUES
    ('TechPro', 'Premium technology products'),
    ('SmartGear', 'Innovative smart devices'),
    ('AudioMax', 'High-quality audio equipment'),
    ('PowerTech', 'Reliable power accessories'),
    ('PixelPro', 'Professional camera equipment'),
    ('TabTech', 'Premium tablet manufacturer');

-- Sample Users (passwords are hashed)
INSERT INTO users (Username, PasswordHash, Email, FirstName, LastName, AddressLine1, City, PostalCode, Country) VALUES
    ('abdul', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLxH1b9X5UJKeES', 'abdul@ntno.no', 'Abdul', 'NTNO', '123 Main St', 'New York', '10001', 'USA'),
    ('bilal', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLxH1b9X5UJKeES', 'bilal@ntno.no', 'Bilal', 'NTNO', '456 Park Ave', 'Los Angeles', '90001', 'USA'),
    ('ole', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLxH1b9X5UJKeES', 'ole@ntno.no', 'Ole', 'NTNO', '789 Oak Rd', 'Chicago', '60601', 'USA');

-- Products
INSERT INTO products (Name, Description, Price, StockQuantity, CategoryID, BrandID, ImageURL) VALUES
    ('TechPro Laptop Pro', '15-inch professional laptop with latest processor', 1299.99, 50, 1, 1, 'laptop1.jpg'),
    ('SmartGear Phone X', 'Latest smartphone with 5G capability', 899.99, 100, 2, 2, 'phone_x.jpg'),
    ('AudioMax Wireless Headphones', 'Premium noise-canceling headphones', 249.99, 75, 4, 3, 'headphones1.jpg'),
    ('PowerTech Fast Charger', '65W USB-C fast charger', 49.99, 200, 3, 4, 'charger1.jpg'),
    ('SmartGear Phone Pro', 'Flagship smartphone with 256GB storage', 1099.99, 50, 2, 2, 'phone_pro.jpg'),
    ('TechPro Laptop Air', '13-inch ultralight laptop', 999.99, 30, 1, 1, 'laptop2.jpg'),
    ('AudioMax Earbuds Pro', 'True wireless earbuds with ANC', 179.99, 150, 4, 3, 'headphones2.jpg'),
    ('PowerTech Wireless Charger', '15W Qi wireless charging pad', 39.99, 100, 3, 4, 'wireless_charger.jpg');

-- Sample Orders
INSERT INTO orders (UserID, TotalAmount, Status, ShippingAddressLine1, ShippingCity, ShippingPostalCode, ShippingCountry) VALUES
    (1, 1349.98, 'Delivered', '123 Main St', 'New York', '10001', 'USA'),
    (2, 1279.98, 'Shipped', '456 Park Ave', 'Los Angeles', '90001', 'USA'),
    (3, 289.98, 'Processing', '789 Oak Rd', 'Chicago', '60601', 'USA');

-- Order Items
INSERT INTO order_items (OrderID, ProductID, Quantity, UnitPrice, Subtotal) VALUES
    (1, 1, 1, 1299.99, 1299.99),
    (1, 4, 1, 49.99, 49.99),
    (2, 2, 1, 899.99, 899.99),
    (2, 3, 1, 249.99, 249.99),
    (3, 4, 2, 49.99, 99.98),
    (3, 8, 1, 39.99, 39.99);

-- Payments
INSERT INTO payments (OrderID, PaymentMethod, Amount, Status, TransactionID) VALUES
    (1, 'Credit Card', 1349.98, 'Completed', 'TXN123456'),
    (2, 'PayPal', 1279.98, 'Completed', 'TXN789012'),
    (3, 'Debit Card', 289.98, 'Processing', 'TXN345678'); 