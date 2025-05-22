# Second Normal Form (2NF)

## Definition
Second Normal Form (2NF) requires that:
1. The database is in First Normal Form (1NF)
2. All non-key attributes are fully functionally dependent on the primary key
3. No partial dependencies exist

## Analysis of Current Schema

### Functional Dependencies

#### Category Table
- `CategoryID` → `Name`, `Description`
- All attributes are fully dependent on the primary key

#### Brand Table
- `BrandID` → `Name`, `Description`
- All attributes are fully dependent on the primary key

#### AppUser Table
- `UserID` → `Username`, `PasswordHash`, `Email`, `FirstName`, `LastName`, `AddressLine1`, `AddressLine2`, `City`, `PostalCode`, `Country`, `PhoneNumber`, `RegistrationDate`
- All attributes are fully dependent on the primary key

#### Product Table
- `ProductID` → `Name`, `Description`, `Price`, `StockQuantity`, `CategoryID`, `BrandID`, `ImageURL`, `DateAdded`, `LastUpdated`
- All attributes are fully dependent on the primary key
- `CategoryID` and `BrandID` are foreign keys, not partial dependencies

#### CustomerOrder Table
- `OrderID` → `UserID`, `OrderDate`, `TotalAmount`, `Status`, `ShippingAddressLine1`, `ShippingAddressLine2`, `ShippingCity`, `ShippingPostalCode`, `ShippingCountry`
- All attributes are fully dependent on the primary key
- `UserID` is a foreign key, not a partial dependency

#### OrderItem Table
- `OrderItemID` → `OrderID`, `ProductID`, `Quantity`, `UnitPrice`, `Subtotal`
- All attributes are fully dependent on the primary key
- `OrderID` and `ProductID` are foreign keys, not partial dependencies

#### Payment Table
- `PaymentID` → `OrderID`, `PaymentDate`, `PaymentMethod`, `Amount`, `Status`, `TransactionID`
- All attributes are fully dependent on the primary key
- `OrderID` is a foreign key, not a partial dependency

### Partial Dependencies Check
- No composite primary keys exist in the schema
- All tables use single-column primary keys
- Therefore, no partial dependencies are possible

## Conclusion
The current database schema fully satisfies Second Normal Form requirements. The schema is in 1NF, and all non-key attributes are fully functionally dependent on their respective primary keys. There are no partial dependencies present in the schema.
