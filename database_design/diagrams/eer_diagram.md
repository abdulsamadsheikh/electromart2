erDiagram
    categories {
        INTEGER CategoryID PK "Unique identifier for the category"
        VARCHAR_100 Name "Name of the category (Unique, Not Null)"
        TEXT Description "A brief description of the category"
    }

    brands {
        INTEGER BrandID PK "Unique identifier for the brand"
        VARCHAR_100 Name "Name of the brand (Unique, Not Null)"
        TEXT Description "A brief description of the brand"
    }

    users {
        INTEGER UserID PK "Unique identifier for the user"
        VARCHAR_50 Username "Unique username for login (Not Null)"
        VARCHAR_255 PasswordHash "Hashed version of the user's password (Not Null)"
        VARCHAR_100 Email "User's email address (Unique, Not Null)"
        VARCHAR_50 FirstName "User's first name (Not Null)"
        VARCHAR_50 LastName "User's last name (Not Null)"
        VARCHAR_255 AddressLine1 "Primary address line"
        VARCHAR_255 AddressLine2 "Secondary address line (Optional)"
        VARCHAR_100 City "City"
        VARCHAR_20 PostalCode "Postal code"
        VARCHAR_50 Country "Country"
        VARCHAR_20 PhoneNumber "Phone number (Optional)"
        TIMESTAMP_WITH_TIME_ZONE RegistrationDate "Timestamp when the user registered (Default CURRENT_TIMESTAMP)"
    }

    products {
        INTEGER ProductID PK "Unique identifier for the product"
        VARCHAR_255 Name "Product name (Not Null)"
        TEXT Description "Detailed product description (Not Null)"
        NUMERIC_10_2 Price "Selling price of the product (Not Null)"
        INTEGER StockQuantity "Number of units currently in stock (Not Null, Default 0)"
        INTEGER CategoryID FK "Foreign key linking to categories"
        INTEGER BrandID FK "Foreign key linking to brands"
        VARCHAR_255 ImageURL "Optional image URL"
        TIMESTAMP_WITH_TIME_ZONE DateAdded "Timestamp when the product was added (Default CURRENT_TIMESTAMP)"
        TIMESTAMP_WITH_TIME_ZONE LastUpdated "Timestamp when the product was last updated (Default CURRENT_TIMESTAMP)"
    }

    orders {
        INTEGER OrderID PK "Unique identifier for the order"
        INTEGER UserID FK "Foreign key linking to the user who placed the order"
        TIMESTAMP_WITH_TIME_ZONE OrderDate "Timestamp when order was placed (Default CURRENT_TIMESTAMP)"
        NUMERIC_12_2 TotalAmount "Total monetary value of the order (Not Null)"
        VARCHAR_50 Status "Current status of the order (Not Null, Default 'Pending')"
        VARCHAR_255 ShippingAddressLine1 "Shipping address line 1 (Not Null)"
        VARCHAR_255 ShippingAddressLine2 "Shipping address line 2 (Optional)"
        VARCHAR_100 ShippingCity "Shipping city (Not Null)"
        VARCHAR_20 ShippingPostalCode "Shipping postal code (Not Null)"
        VARCHAR_50 ShippingCountry "Shipping country (Not Null)"
    }

    order_items {
        INTEGER OrderItemID PK "Unique identifier for the order item entry"
        INTEGER OrderID FK "Foreign key linking to the orders table"
        INTEGER ProductID FK "Foreign key linking to the products table"
        INTEGER Quantity "Number of units of this product in the order (Not Null)"
        NUMERIC_10_2 UnitPrice "Price per unit at the time of order (Not Null)"
        NUMERIC_12_2 Subtotal "Calculated as Quantity * UnitPrice (Not Null)"
    }

    payments {
        INTEGER PaymentID PK "Unique identifier for the payment"
        INTEGER OrderID FK "Foreign key linking to the orders table (Unique)"
        TIMESTAMP_WITH_TIME_ZONE PaymentDate "Timestamp when payment was made (Default CURRENT_TIMESTAMP)"
        VARCHAR_50 PaymentMethod "Method used for payment (Not Null)"
        NUMERIC_12_2 Amount "Amount paid (Not Null)"
        VARCHAR_50 Status "Status of the payment (Not Null, Default 'Pending')"
        VARCHAR_255 TransactionID "Unique transaction identifier from payment gateway (Optional, Unique)"
    }

    %% Relationships
    categories ||--|{ products : "contains"
    brands ||--|{ products : "manufactures"
    users ||--|{ orders : "places"
    orders ||--|{ order_items : "details"
    products ||--o{ order_items : "appears_in"
    orders ||--|| payments : "has_one_payment_for"