# Boyce-Codd Normal Form (BCNF)

## Definition
Boyce-Codd Normal Form (BCNF) is a higher level of normalization than 3NF. A table is in BCNF if and only if for every one of its non-trivial functional dependencies X → Y, X is a superkey—that is, X is either a candidate key or a superset of a candidate key.

## Analysis of Current Schema

To verify BCNF, we need to examine all functional dependencies in each table.

### `categories` Table
-   **Primary Key**: `CategoryID`
-   **Functional Dependencies**:
    -   `CategoryID` → `Name`, `Description`
-   **Candidate Keys**: `CategoryID`, `Name` (since Name is UNIQUE)
-   **Analysis**:
    -   For `CategoryID` → `Name`, `Description`: `CategoryID` is a candidate key.
    -   For `Name` → `CategoryID`, `Description`: `Name` is a candidate key.
-   **Conclusion**: The `categories` table is in BCNF.

### `brands` Table
-   **Primary Key**: `BrandID`
-   **Functional Dependencies**:
    -   `BrandID` → `Name`, `Description`
-   **Candidate Keys**: `BrandID`, `Name` (since Name is UNIQUE)
-   **Analysis**:
    -   For `BrandID` → `Name`, `Description`: `BrandID` is a candidate key.
    -   For `Name` → `BrandID`, `Description`: `Name` is a candidate key.
-   **Conclusion**: The `brands` table is in BCNF.

### `users` Table
-   **Primary Key**: `UserID`
-   **Functional Dependencies**:
    -   `UserID` → `Username`, `PasswordHash`, `Email`, `FirstName`, `LastName`, `AddressLine1`, `AddressLine2`, `City`, `PostalCode`, `Country`, `PhoneNumber`, `RegistrationDate`
-   **Candidate Keys**: `UserID`, `Username`, `Email` (since Username and Email are UNIQUE)
-   **Analysis**:
    -   For `UserID` → All other attributes: `UserID` is a candidate key.
    -   For `Username` → All other attributes (excluding UserID if not functionally dependent on Username alone, but here it can be considered as Username determines a unique user): `Username` is a candidate key.
    -   For `Email` → All other attributes: `Email` is a candidate key.
-   **Conclusion**: The `users` table is in BCNF.

### `products` Table
-   **Primary Key**: `ProductID`
-   **Functional Dependencies**:
    -   `ProductID` → `Name`, `Description`, `Price`, `StockQuantity`, `CategoryID`, `BrandID`, `ImageURL`, `DateAdded`, `LastUpdated`
-   **Candidate Keys**: `ProductID`
-   **Analysis**:
    -   For `ProductID` → All other attributes: `ProductID` is a candidate key.
-   **Conclusion**: The `products` table is in BCNF.

### `orders` Table
-   **Primary Key**: `OrderID`
-   **Functional Dependencies**:
    -   `OrderID` → `UserID`, `OrderDate`, `TotalAmount`, `Status`, `ShippingAddressLine1`, `ShippingAddressLine2`, `ShippingCity`, `ShippingPostalCode`, `ShippingCountry`
-   **Candidate Keys**: `OrderID`
-   **Analysis**:
    -   For `OrderID` → All other attributes: `OrderID` is a candidate key.
-   **Conclusion**: The `orders` table is in BCNF.

### `order_items` Table
-   **Primary Key**: `OrderItemID`
-   **Composite Key**: (`OrderID`, `ProductID`) is a UNIQUE constraint, making it a candidate key.
-   **Functional Dependencies**:
    -   `OrderItemID` → `OrderID`, `ProductID`, `Quantity`, `UnitPrice`, `Subtotal`
    -   (`OrderID`, `ProductID`) → `OrderItemID`, `Quantity`, `UnitPrice`, `Subtotal`
-   **Candidate Keys**: `OrderItemID`, (`OrderID`, `ProductID`)
-   **Analysis**:
    -   For `OrderItemID` → All other attributes: `OrderItemID` is a candidate key.
    -   For (`OrderID`, `ProductID`) → `OrderItemID`, `Quantity`, `UnitPrice`, `Subtotal`: (`OrderID`, `ProductID`) is a candidate key.
-   **Conclusion**: The `order_items` table is in BCNF.

### `payments` Table
-   **Primary Key**: `PaymentID`
-   **Functional Dependencies**:
    -   `PaymentID` → `OrderID`, `PaymentDate`, `PaymentMethod`, `Amount`, `Status`, `TransactionID`
    -   `OrderID` → `PaymentID`, `PaymentDate`, `PaymentMethod`, `Amount`, `Status`, `TransactionID` (since OrderID is UNIQUE in payments)
    -   `TransactionID` → `PaymentID`, `OrderID`, `PaymentDate`, `PaymentMethod`, `Amount`, `Status` (since TransactionID is UNIQUE)
-   **Candidate Keys**: `PaymentID`, `OrderID`, `TransactionID`
-   **Analysis**:
    -   For each candidate key, it functionally determines all other attributes in the table.
-   **Conclusion**: The `payments` table is in BCNF.

## Overall Conclusion
All tables in the ElectroMart database schema are in Boyce-Codd Normal Form (BCNF). For every non-trivial functional dependency X → Y, X is a superkey.