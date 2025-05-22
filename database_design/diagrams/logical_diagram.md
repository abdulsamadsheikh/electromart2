classDiagram
    direction LR

    class categories {
        +Integer CategoryID (PK)
        +String Name (UNIQUE)
        +String Description
    }

    class brands {
        +Integer BrandID (PK)
        +String Name (UNIQUE)
        +String Description
    }

    class users {
        +Integer UserID (PK)
        +String Username (UNIQUE)
        +String PasswordHash
        +String Email (UNIQUE)
        +String FirstName
        +String LastName
        +String AddressLine1
        +String AddressLine2
        +String City
        +String PostalCode
        +String Country
        +String PhoneNumber
        +Timestamp RegistrationDate
    }

    class products {
        +Integer ProductID (PK)
        +String Name
        +String Description
        +Numeric Price
        +Integer StockQuantity
        +Integer CategoryID (FK)
        +Integer BrandID (FK)
        +String ImageURL
        +Timestamp DateAdded
        +Timestamp LastUpdated
    }

    class orders {
        +Integer OrderID (PK)
        +Integer UserID (FK)
        +Timestamp OrderDate
        +Numeric TotalAmount
        +String Status
        +String ShippingAddressLine1
        +String ShippingAddressLine2
        +String ShippingCity
        +String ShippingPostalCode
        +String ShippingCountry
    }

    class order_items {
        +Integer OrderItemID (PK)
        +Integer OrderID (FK)
        +Integer ProductID (FK)
        +Integer Quantity
        +Numeric UnitPrice
        +Numeric Subtotal
        +Constraint uq_order_product (OrderID, ProductID)
    }

    class payments {
        +Integer PaymentID (PK)
        +Integer OrderID (FK, UNIQUE)
        +Timestamp PaymentDate
        +String PaymentMethod
        +Numeric Amount
        +String Status
        +String TransactionID (UNIQUE)
    }

    categories "1" -- "*" products : CategoryID
    brands "1" -- "*" products : BrandID
    users "1" -- "*" orders : UserID
    orders "1" -- "*" order_items : OrderID
    products "1" -- "*" order_items : ProductID
    orders "1" -- "1" payments : OrderID