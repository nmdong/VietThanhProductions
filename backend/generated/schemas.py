from marshmallow import Schema, fields

class Auth_usersSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password_hash = fields.Str(required=True)
    email = fields.Str(required=True)

from marshmallow import Schema, fields

class Token_blocklistSchema(Schema):
    jti = fields.Str(required=True)
    token_type = fields.Str(required=True)
    user_id = fields.Str(required=True)
    created_at = fields.Str(required=True)

