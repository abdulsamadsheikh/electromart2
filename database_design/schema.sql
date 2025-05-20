DROP TABLE IF EXISTS Payment CASCADE;
DROP TABLE IF EXISTS OrderItem CASCADE;
DROP TABLE IF EXISTS CustomerOrder CASCADE;
DROP TABLE IF EXISTS Product CASCADE;
DROP TABLE IF EXISTS AppUser CASCADE;
DROP TABLE IF EXISTS Brand CASCADE;
DROP TABLE IF EXISTS Category CASCADE;

CREATE TABLE Category (
    CategoryID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT
);
COMMENT ON TABLE Category IS 'Represents different categories of electronic products.';
COMMENT ON COLUMN Category.CategoryID IS 'Unique identifier for the category (e.g., 1, 2, 3...).';
COMMENT ON COLUMN Category.Name IS 'Name of the category (e.g., "Smartphones", "Laptops"). Must be unique.';
COMMENT ON COLUMN Category.Description IS 'A brief description of the category.';

CREATE TABLE Brand (
    BrandID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT
);
COMMENT ON TABLE Brand IS 'Represents the brands or manufacturers of electronic products.';
COMMENT ON COLUMN Brand.BrandID IS 'Unique identifier for the brand (e.g., 1, 2, 3...).';
COMMENT ON COLUMN Brand.Name IS 'Name of the brand (e.g., "Apple", "Samsung"). Must be unique.';
COMMENT ON COLUMN Brand.Description IS 'A brief description of the brand.';

CREATE TABLE AppUser (
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
    RegistrationDate TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE AppUser IS 'Represents users (customers) of the website.';
COMMENT ON COLUMN AppUser.UserID IS 'Unique identifier for the user.';
COMMENT ON COLUMN AppUser.Username IS 'Unique username for login.';
COMMENT ON COLUMN AppUser.PasswordHash IS 'Hashed version of the users password.';
COMMENT ON COLUMN AppUser.Email IS 'Users email address (must be unique).';
COMMENT ON COLUMN AppUser.RegistrationDate IS 'Timestamp when the user registered.';

CREATE TABLE Product (
    ProductID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL CHECK (Price > 0),
    StockQuantity INTEGER NOT NULL DEFAULT 0 CHECK (StockQuantity >= 0),
    CategoryID INTEGER NOT NULL,
    BrandID INTEGER NOT NULL,
    ImageURL VARCHAR(255), 
    DateAdded TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    LastUpdated TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    CONSTRAINT fk_category FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID) ON DELETE RESTRICT, 
    CONSTRAINT fk_brand FOREIGN KEY (BrandID) REFERENCES Brand(BrandID) ON DELETE RESTRICT       
);
COMMENT ON TABLE Product IS 'Represents the electronic products available for sale.';
COMMENT ON COLUMN Product.ProductID IS 'Unique identifier for the product.';
COMMENT ON COLUMN Product.Price IS 'Selling price of the product, must be positive.';
COMMENT ON COLUMN Product.StockQuantity IS 'Number of units currently in stock, cannot be negative.';
COMMENT ON COLUMN Product.CategoryID IS 'Foreign key linking to the Category table.';
COMMENT ON COLUMN Product.BrandID IS 'Foreign key linking to the Brand table.';
COMMENT ON COLUMN Product.DateAdded IS 'Timestamp when the product was added.';
COMMENT ON COLUMN Product.LastUpdated IS 'Timestamp when the product was last updated.';

CREATE TABLE CustomerOrder (
    OrderID SERIAL PRIMARY KEY,
    UserID INTEGER NOT NULL,
    OrderDate TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(12, 2) NOT NULL CHECK (TotalAmount >= 0),
    Status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    ShippingAddressLine1 VARCHAR(255) NOT NULL,
    ShippingAddressLine2 VARCHAR(255),
    ShippingCity VARCHAR(100) NOT NULL,
    ShippingPostalCode VARCHAR(20) NOT NULL,
    ShippingCountry VARCHAR(50) NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (UserID) REFERENCES AppUser(UserID) ON DELETE RESTRICT
);
COMMENT ON TABLE CustomerOrder IS 'Represents individual orders placed by users.';
COMMENT ON COLUMN CustomerOrder.OrderID IS 'Unique identifier for the order.';
COMMENT ON COLUMN CustomerOrder.UserID IS 'Foreign key linking to the AppUser who placed the order.';
COMMENT ON COLUMN CustomerOrder.TotalAmount IS 'Total monetary value of the order, cannot be negative.';
COMMENT ON COLUMN CustomerOrder.Status IS 'Current status of the order (e.g., Pending, Shipped). Consider ENUM type for strict values.';

CREATE TABLE OrderItem (
    OrderItemID SERIAL PRIMARY KEY,
    OrderID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(10, 2) NOT NULL CHECK (UnitPrice >= 0),
    Subtotal DECIMAL(12, 2) NOT NULL CHECK (Subtotal >= 0),
    CONSTRAINT fk_order FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID) ON DELETE CASCADE, -- If an order is deleted, its items are deleted
    CONSTRAINT fk_product FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE RESTRICT, -- Prevent deleting product if it is in an order item
    CONSTRAINT uq_order_product UNIQUE (OrderID, ProductID) -- Ensure a product appears only once per order line
);
COMMENT ON TABLE OrderItem IS 'Represents the line items included in each order.';
COMMENT ON COLUMN OrderItem.OrderItemID IS 'Unique identifier for the order item entry.';
COMMENT ON COLUMN OrderItem.OrderID IS 'Foreign key linking to the CustomerOrder.';
COMMENT ON COLUMN OrderItem.ProductID IS 'Foreign key linking to the Product.';
COMMENT ON COLUMN OrderItem.Quantity IS 'Number of units of this product in the order, must be positive.';
COMMENT ON COLUMN OrderItem.UnitPrice IS 'Price per unit at the time of order. Important as product price can change.';
COMMENT ON COLUMN OrderItem.Subtotal IS 'Calculated as Quantity * UnitPrice.';
COMMENT ON CONSTRAINT uq_order_product ON OrderItem IS 'Ensures that a specific product is listed only once per order. Quantity handles multiples.';

-- Entity: Payment
CREATE TABLE Payment (
    PaymentID SERIAL PRIMARY KEY,
    OrderID INTEGER NOT NULL UNIQUE, -- Assuming one payment record per order for simplicity
    PaymentDate TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PaymentMethod VARCHAR(50) NOT NULL, -- E.g., 'Credit Card', 'PayPal', 'Vipps'
    Amount DECIMAL(12, 2) NOT NULL CHECK (Amount >= 0), -- Should generally match CustomerOrder.TotalAmount
    -- Possible statuses: 'Pending', 'Completed', 'Failed', 'Refunded'
    Status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    TransactionID VARCHAR(255) UNIQUE, -- Optional, from payment gateway, should be unique if present
    CONSTRAINT fk_payment_order FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID) ON DELETE CASCADE -- If an order is deleted, its payment record is also deleted
);
COMMENT ON TABLE Payment IS 'Represents payments made for orders.';
COMMENT ON COLUMN Payment.PaymentID IS 'Unique identifier for the payment.';
COMMENT ON COLUMN Payment.OrderID IS 'Foreign key linking to the CustomerOrder. Marked UNIQUE assuming one payment process per order.';
COMMENT ON COLUMN Payment.PaymentMethod IS 'Method used for payment.';
COMMENT ON COLUMN Payment.Amount IS 'Amount paid, cannot be negative.';
COMMENT ON COLUMN Payment.Status IS 'Status of the payment (e.g., Pending, Completed). Consider ENUM type.';
COMMENT ON COLUMN Payment.TransactionID IS 'Unique transaction identifier from the payment gateway, if applicable.';