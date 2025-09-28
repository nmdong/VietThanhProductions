from marshmallow import Schema, fields

class OrderItemSchema(Schema):
    product_id = fields.Int(required=True)     # Tham chiếu tới Product.id
    product_name = fields.Str(dump_only=True)  # Tên sản phẩm (load từ Product)
    price = fields.Float(required=True)        # Giá tại thời điểm đặt
    quantity = fields.Int(required=True)       # Số lượng đặt
    subtotal = fields.Float(dump_only=True)    # Thành tiền = price * quantity


class OrderSchema(Schema):
    id = fields.Int(dump_only=True)                  # PK, tự tăng
    customer_name = fields.Str(required=True)        # Tên khách hàng
    customer_phone = fields.Str(required=True)       # SĐT khách hàng
    customer_address = fields.Str(required=False)    # Địa chỉ giao hàng
    items = fields.List(fields.Nested(OrderItemSchema), required=True)  # Danh sách sản phẩm trong đơn
    total_amount = fields.Float(dump_only=True)      # Tổng số tiền (tính từ items)
    status = fields.Str(required=True,
                        validate=lambda x: x in ["pending", "confirmed", "shipped", "completed", "canceled"])
    created_at = fields.DateTime(dump_only=True)     # Ngày đặt
    updated_at = fields.DateTime(dump_only=True)     # Ngày cập nhật

