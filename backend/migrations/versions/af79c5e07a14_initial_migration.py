"""Initial migration

Revision ID: af79c5e07a14
Revises: 
Create Date: 2025-05-21 20:01:41.847576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af79c5e07a14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brands',
    sa.Column('BrandID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=100), nullable=False),
    sa.Column('Description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('BrandID'),
    sa.UniqueConstraint('Name')
    )
    op.create_table('categories',
    sa.Column('CategoryID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=100), nullable=False),
    sa.Column('Description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('CategoryID'),
    sa.UniqueConstraint('Name')
    )
    op.create_table('users',
    sa.Column('UserID', sa.Integer(), nullable=False),
    sa.Column('Username', sa.String(length=50), nullable=False),
    sa.Column('PasswordHash', sa.String(length=255), nullable=False),
    sa.Column('Email', sa.String(length=100), nullable=False),
    sa.Column('FirstName', sa.String(length=50), nullable=False),
    sa.Column('LastName', sa.String(length=50), nullable=False),
    sa.Column('AddressLine1', sa.String(length=255), nullable=True),
    sa.Column('AddressLine2', sa.String(length=255), nullable=True),
    sa.Column('City', sa.String(length=100), nullable=True),
    sa.Column('PostalCode', sa.String(length=20), nullable=True),
    sa.Column('Country', sa.String(length=50), nullable=True),
    sa.Column('PhoneNumber', sa.String(length=20), nullable=True),
    sa.Column('RegistrationDate', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('UserID'),
    sa.UniqueConstraint('Email'),
    sa.UniqueConstraint('Username')
    )
    op.create_table('orders',
    sa.Column('OrderID', sa.Integer(), nullable=False),
    sa.Column('UserID', sa.Integer(), nullable=False),
    sa.Column('OrderDate', sa.DateTime(timezone=True), nullable=True),
    sa.Column('TotalAmount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('Status', sa.String(length=50), nullable=False),
    sa.Column('ShippingAddressLine1', sa.String(length=255), nullable=False),
    sa.Column('ShippingAddressLine2', sa.String(length=255), nullable=True),
    sa.Column('ShippingCity', sa.String(length=100), nullable=False),
    sa.Column('ShippingPostalCode', sa.String(length=20), nullable=False),
    sa.Column('ShippingCountry', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['UserID'], ['users.UserID'], ),
    sa.PrimaryKeyConstraint('OrderID')
    )
    op.create_table('products',
    sa.Column('ProductID', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=255), nullable=False),
    sa.Column('Description', sa.Text(), nullable=False),
    sa.Column('Price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('StockQuantity', sa.Integer(), nullable=False),
    sa.Column('CategoryID', sa.Integer(), nullable=False),
    sa.Column('BrandID', sa.Integer(), nullable=False),
    sa.Column('ImageURL', sa.String(length=255), nullable=True),
    sa.Column('DateAdded', sa.DateTime(timezone=True), nullable=True),
    sa.Column('LastUpdated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['BrandID'], ['brands.BrandID'], ),
    sa.ForeignKeyConstraint(['CategoryID'], ['categories.CategoryID'], ),
    sa.PrimaryKeyConstraint('ProductID')
    )
    op.create_table('order_items',
    sa.Column('OrderItemID', sa.Integer(), nullable=False),
    sa.Column('OrderID', sa.Integer(), nullable=False),
    sa.Column('ProductID', sa.Integer(), nullable=False),
    sa.Column('Quantity', sa.Integer(), nullable=False),
    sa.Column('UnitPrice', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('Subtotal', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['OrderID'], ['orders.OrderID'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['ProductID'], ['products.ProductID'], ),
    sa.PrimaryKeyConstraint('OrderItemID'),
    sa.UniqueConstraint('OrderID', 'ProductID', name='uq_order_product')
    )
    op.create_table('payments',
    sa.Column('PaymentID', sa.Integer(), nullable=False),
    sa.Column('OrderID', sa.Integer(), nullable=False),
    sa.Column('PaymentDate', sa.DateTime(timezone=True), nullable=True),
    sa.Column('PaymentMethod', sa.String(length=50), nullable=False),
    sa.Column('Amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('Status', sa.String(length=50), nullable=False),
    sa.Column('TransactionID', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['OrderID'], ['orders.OrderID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('PaymentID'),
    sa.UniqueConstraint('OrderID'),
    sa.UniqueConstraint('TransactionID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('order_items')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('categories')
    op.drop_table('brands')
    # ### end Alembic commands ###
