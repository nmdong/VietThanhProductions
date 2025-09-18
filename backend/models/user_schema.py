from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, description="Tên người dùng")
    email = fields.Email(required=True, description="Email")
    age = fields.Int(required=True, description="Tuổi")
