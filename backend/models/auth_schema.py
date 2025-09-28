"""
Schemas for authentication-related tables.

Tables:
- auth_users(id COUNTER PK, username TEXT, password_hash TEXT, email TEXT)
- token_blocklist(jti TEXT PK, token_type TEXT, user_id INTEGER, created_at TEXT)
"""

from marshmallow import Schema, fields


class AuthUserSchema(Schema):
    id = fields.Int(dump_only=True)   # PK, Auto Increment (COUNTER)
    username = fields.Str(required=True)
    password_hash = fields.Str(required=True)
    email = fields.Str(required=False, allow_none=True)


class TokenBlocklistSchema(Schema):
    jti = fields.Str(required=True)   # PK
    token_type = fields.Str(required=True)
    user_id = fields.Int(required=False, allow_none=True)
    created_at = fields.DateTime(required=True)
