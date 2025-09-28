from marshmallow import Schema, fields

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)             # PK, tự tăng, duy nhất cho mỗi sản phẩm
    code = fields.Str(required=True)            # Mã sản phẩm (VD: 05.1157)
    name = fields.Str(required=True)            # Tên đầy đủ của sản phẩm (VD: Ghế bành cà phê màu cam)
    category = fields.Str(required=True)        # Nhóm sản phẩm chính (VD: Ghế, Xô, Rổ...)
    subcategory = fields.Str(required=False)    # Nhóm chi tiết (VD: Ghế bành cà phê, Rổ Nhật R002)
    color = fields.Str(required=False)          # Màu sắc (VD: đỏ, cam, dương mực)
    size = fields.Str(required=False)           # Kích thước/dung tích (VD: 20L, 1 tấc 9, 003)
    material = fields.Str(required=False)       # Chất liệu (mặc định: nhựa, nếu có thể bổ sung thêm)
    feature = fields.Str(required=False)        # Đặc điểm bổ sung (VD: có nắp, mặt trắng, đủ màu)
    price = fields.Float(required=True)         # Giá bán hiện tại
    stock = fields.Int(required=True)           # Số lượng tồn kho
    created_at = fields.DateTime(dump_only=True) # Thời điểm thêm sản phẩm
    updated_at = fields.DateTime(dump_only=True) # Thời điểm cập nhật sản phẩm

