erDiagram
    Category {
        SERIAL CategoryID PK "Unique ID for category"
        VARCHAR_100 Name "Name of the category (Unique, Not Null)"
        TEXT Description "Optional description"
    }

    Brand {
        SERIAL BrandID PK "Unique ID for brand"
        VARCHAR_100 Name "Name of the brand (Unique, Not Null)"
        TEXT Description "Optional description"
    }

    Product {
        SERIAL ProductID PK "Unique ID for product"
        VARCHAR_255 Name "Product name (Not Null)"
        TEXT Description "Detailed product description (Not Null)"
        DECIMAL_10_2 Price "Selling price (Not Null, >0)"
        INTEGER StockQuantity "Current stock (Not Null, >=0, Default 0)"
        INTEGER CategoryID FK "Links to Category"
        INTEGER BrandID FK "Links to Brand"
        VARCHAR_255 ImageURL "Optional image URL"
        TIMESTAMP DateAdded "When product was added (Not Null, Default NOW)"
        TIMESTAMP LastUpdated "When product was last updated (Not Null, Default NOW)"
    }

    AppUser {
        SERIAL UserID PK "Unique ID for user"
        VARCHAR_50 Username "Login username (Unique, Not Null)"
        VARCHAR_255 PasswordHash "Hashed password (Not Null)"
        VARCHAR_100 Email "User email (Unique, Not Null)"
        VARCHAR_50 FirstName "User's first name (Not Null)"
        VARCHAR_50 LastName "User's last name (Not Null)"
        VARCHAR_255 AddressLine1 "Primary address line"
        VARCHAR_255 AddressLine2 "Secondary address line (Optional)"
        VARCHAR_100 City "City"
        VARCHAR_20 PostalCode "Postal code"
        VARCHAR_50 Country "Country"
        VARCHAR_20 PhoneNumber "Phone number (Optional)"
        TIMESTAMP RegistrationDate "When user registered (Not Null, Default NOW)"
    }

    CustomerOrder {
        SERIAL OrderID PK "Unique ID for order"
        INTEGER UserID FK "Links to AppUser who placed the order"
        TIMESTAMP OrderDate "When order was placed (Not Null, Default NOW)"
        DECIMAL_12_2 TotalAmount "Total value of the order (Not Null, >=0)"
        VARCHAR_50 Status "Order status (Not Null, Default 'Pending')"
        VARCHAR_255 ShippingAddressLine1 "Shipping address line 1 (Not Null)"
        VARCHAR_255 ShippingAddressLine2 "Shipping address line 2 (Optional)"
        VARCHAR_100 ShippingCity "Shipping city (Not Null)"
        VARCHAR_20 ShippingPostalCode "Shipping postal code (Not Null)"
        VARCHAR_50 ShippingCountry "Shipping country (Not Null)"
    }

    OrderItem {
        SERIAL OrderItemID PK "Unique ID for an order item line"
        INTEGER OrderID FK "Links to CustomerOrder"
        INTEGER ProductID FK "Links to Product"
        INTEGER Quantity "Number of units (Not Null, >0)"
        DECIMAL_10_2 UnitPrice "Price per unit at time of order (Not Null)"
        DECIMAL_12_2 Subtotal "Quantity * UnitPrice (Not Null)"
    }

    Payment {
        SERIAL PaymentID PK "Unique ID for payment"
        INTEGER OrderID FK "Links to CustomerOrder (Unique)"
        TIMESTAMP PaymentDate "When payment was made (Not Null, Default NOW)"
        VARCHAR_50 PaymentMethod "Method of payment (Not Null)"
        DECIMAL_12_2 Amount "Amount paid (Not Null, >=0)"
        VARCHAR_50 Status "Payment status (Not Null, Default 'Pending')"
        VARCHAR_255 TransactionID "Gateway transaction ID (Optional)"
    }

    %% Defining Relationships
    Category ||--|{ Product : "contains"
    Brand ||--|{ Product : "manufactures"
    AppUser ||--|{ CustomerOrder : "places"
    CustomerOrder ||--|{ OrderItem : "details"
    Product ||--o{ OrderItem : "appears in"
    CustomerOrder ||--|| Payment : "has one"