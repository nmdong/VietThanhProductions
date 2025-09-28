"""
Schemas for orders table.

Columns:
- id (Int, PK, Auto increment)
- order_number (Str)
- customer_name (Str)
- product_id (Int, nullable)
- quantity (Int, default 1)
- unit_price (Float, nullable)
- total_price (Float, computed if None)
- order_date (DateTime in ISO string)
- status (Str, default "NEW")
"""

from marshmallow import Schema, fields


class OrderSchema(Schema):
    id = fields.Int(dump_only=True)  # PK, Auto increment
    order_number = fields.Str(required=True)
    customer_name = fields.Str(required=True)
    product_id = fields.Int(required=False, allow_none=True)
    quantity = fields.Int(required=True)
    unit_price = fields.Float(required=False, allow_none=True)
    total_price = fields.Float(required=False, allow_none=True)
    order_date = fields.DateTime(required=True)
    status = fields.Str(required=True)
