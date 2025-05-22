# Third Normal Form (3NF)

## Definition
Third Normal Form (3NF) requires that:
1. The database is in Second Normal Form (2NF)
2. All attributes are directly dependent on the primary key
3. No transitive dependencies exist

## Analysis of Current Schema

### Transitive Dependencies Check

#### Category Table
- No transitive dependencies
- All attributes directly depend on `CategoryID`

#### Brand Table
- No transitive dependencies
- All attributes directly depend on `BrandID`

#### AppUser Table
- No transitive dependencies
- All attributes directly depend on `UserID`
- Address components are independent attributes, not transitively dependent

#### Product Table
- No transitive dependencies
- All attributes directly depend on `ProductID`
- `CategoryID` and `BrandID` are foreign keys, not transitive dependencies

#### CustomerOrder Table
- No transitive dependencies
- All attributes directly depend on `OrderID`
- Shipping address components are independent attributes
- `UserID` is a foreign key, not a transitive dependency

#### OrderItem Table
- No transitive dependencies
- All attributes directly depend on `OrderItemID`
- `Subtotal` is calculated from `Quantity` and `UnitPrice`, but this is a derived value, not a transitive dependency
- `OrderID` and `ProductID` are foreign keys, not transitive dependencies

#### Payment Table
- No transitive dependencies
- All attributes directly depend on `PaymentID`
- `OrderID` is a foreign key, not a transitive dependency

### Potential Transitive Dependencies Addressed

1. **Address Information**
   - In `AppUser` and `CustomerOrder`, address components are kept as separate columns
   - This prevents transitive dependencies that would occur if address was stored as a single field

2. **Order Calculations**
   - `OrderItem.Subtotal` is stored but calculated from `Quantity` and `UnitPrice`
   - This is a derived value, not a transitive dependency
   - The calculation is maintained at the application level

3. **User Information**
   - All user attributes directly depend on `UserID`
   - No transitive dependencies between user attributes

## Conclusion
The current database schema fully satisfies Third Normal Form requirements. The schema is in 2NF, and there are no transitive dependencies present. All attributes are directly dependent on their respective primary keys, and the schema properly handles derived values and foreign key relationships.
