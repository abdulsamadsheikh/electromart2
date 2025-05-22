-- Sample Queries for ElectroMart Database

-- 1. Product Management Queries

-- Get all products with their categories and brands
SELECT 
    p.ProductID,
    p.Name AS ProductName,
    p.Price,
    p.StockQuantity,
    c.Name AS CategoryName,
    b.Name AS BrandName
FROM products p
JOIN categories c ON p.CategoryID = c.CategoryID
JOIN brands b ON p.BrandID = b.BrandID;

-- Find low stock products (less than 10 units)
SELECT 
    ProductID,
    Name,
    StockQuantity
FROM products
WHERE StockQuantity < 10
ORDER BY StockQuantity;

-- Get products by category with stock status
SELECT 
    c.Name AS CategoryName,
    p.Name AS ProductName,
    p.Price,
    p.StockQuantity,
    CASE 
        WHEN p.StockQuantity = 0 THEN 'Out of Stock'
        WHEN p.StockQuantity < 10 THEN 'Low Stock'
        ELSE 'In Stock'
    END AS StockStatus
FROM products p
JOIN categories c ON p.CategoryID = c.CategoryID
ORDER BY c.Name, p.Name;

-- 2. Order Management Queries

-- Get recent orders with customer details
SELECT 
    o.OrderID,
    o.OrderDate,
    o.TotalAmount,
    o.Status,
    u.FirstName || ' ' || u.LastName AS CustomerName,
    u.Email
FROM orders o
JOIN users u ON o.UserID = u.UserID
ORDER BY o.OrderDate DESC
LIMIT 10;

-- Get detailed order information
SELECT 
    o.OrderID,
    o.OrderDate,
    u.FirstName || ' ' || u.LastName AS CustomerName,
    p.Name AS ProductName,
    oi.Quantity,
    oi.UnitPrice,
    oi.Subtotal,
    o.TotalAmount,
    o.Status,
    pay.PaymentMethod,
    pay.Status AS PaymentStatus
FROM orders o
JOIN users u ON o.UserID = u.UserID
JOIN order_items oi ON o.OrderID = oi.OrderID
JOIN products p ON oi.ProductID = p.ProductID
LEFT JOIN payments pay ON o.OrderID = pay.OrderID
WHERE o.OrderID = :order_id;

-- 3. Sales Analytics Queries

-- Total sales by category
SELECT 
    c.Name AS CategoryName,
    COUNT(DISTINCT o.OrderID) as NumberOfOrders,
    SUM(oi.Subtotal) as TotalSales
FROM categories c
JOIN products p ON c.CategoryID = p.CategoryID
JOIN order_items oi ON p.ProductID = oi.ProductID
JOIN orders o ON oi.OrderID = o.OrderID
WHERE o.Status != 'Cancelled'
GROUP BY c.CategoryID, c.Name
ORDER BY TotalSales DESC;

-- Best-selling products
SELECT 
    p.Name AS ProductName,
    SUM(oi.Quantity) as TotalQuantitySold,
    SUM(oi.Subtotal) as TotalRevenue,
    COUNT(DISTINCT o.OrderID) as NumberOfOrders
FROM products p
JOIN order_items oi ON p.ProductID = oi.ProductID
JOIN orders o ON oi.OrderID = o.OrderID
WHERE o.Status != 'Cancelled'
GROUP BY p.ProductID, p.Name
ORDER BY TotalQuantitySold DESC
LIMIT 10;

-- 4. Customer Analytics Queries

-- Most valuable customers
SELECT 
    u.UserID,
    u.FirstName || ' ' || u.LastName AS CustomerName,
    COUNT(o.OrderID) as NumberOfOrders,
    SUM(o.TotalAmount) as TotalSpent,
    MAX(o.OrderDate) as LastOrderDate
FROM users u
JOIN orders o ON u.UserID = o.UserID
WHERE o.Status != 'Cancelled'
GROUP BY u.UserID, u.FirstName, u.LastName
ORDER BY TotalSpent DESC
LIMIT 10;

-- Payment method statistics
SELECT 
    PaymentMethod,
    COUNT(*) as NumberOfTransactions,
    SUM(Amount) as TotalAmount,
    ROUND(AVG(Amount), 2) as AverageAmount
FROM payments
WHERE Status = 'Completed'
GROUP BY PaymentMethod
ORDER BY TotalAmount DESC;

-- 5. Inventory Management Queries

-- Update product stock
UPDATE products
SET 
    StockQuantity = StockQuantity + :quantity_change,
    LastUpdated = CURRENT_TIMESTAMP
WHERE ProductID = :product_id;

-- Create trigger for automatic stock update after order
CREATE OR REPLACE FUNCTION update_stock_after_order()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET StockQuantity = StockQuantity - NEW.Quantity
    WHERE ProductID = NEW.ProductID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_order_item_insert
AFTER INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION update_stock_after_order();

-- 6. Search and Filter Queries

-- Search products by name or description
SELECT 
    p.ProductID,
    p.Name,
    p.Description,
    p.Price,
    c.Name AS CategoryName,
    b.Name AS BrandName
FROM products p
JOIN categories c ON p.CategoryID = c.CategoryID
JOIN brands b ON p.BrandID = b.BrandID
WHERE 
    p.Name ILIKE '%' || :search_term || '%' OR 
    p.Description ILIKE '%' || :search_term || '%';

-- Filter products by price range and category
SELECT 
    p.Name,
    p.Price,
    c.Name AS CategoryName,
    b.Name AS BrandName
FROM products p
JOIN categories c ON p.CategoryID = c.CategoryID
JOIN brands b ON p.BrandID = b.BrandID
WHERE 
    p.Price BETWEEN :min_price AND :max_price
    AND (:category_id IS NULL OR p.CategoryID = :category_id)
ORDER BY p.Price; 