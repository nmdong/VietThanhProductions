"""
Authentication routes (register, login, refresh, logout) with JWT.

All endpoints return payload in the project's unified format:
- Success:
  {
    "status": "success",
    "data": {...},
    "meta": {...}
  }
- Error:
  {
    "status": "error",
    "error": {...},
    "meta": {...}
  }
"""

from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
import db.dao_auth as dao_auth
from utils.response import success_response, error_response, start_request

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.before_request
def before():
    """Initialize request metadata for all auth routes."""
    start_request()


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    POST /auth/register
    ---
    tags:
      - Authentication
    summary: Register a new user
    description: Create a new user with username, password, and optional email.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [username, password]
            properties:
              username:
                type: string
              password:
                type: string
              email:
                type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Missing fields or user exists
    """
    # data = request.get_json(force=True) or {}
    req = request.get_json(force=True) or {}

    # Kiểm tra action
    action = req.get("action")
    if action != "register":
        return error_response("INVALID_ACTION", "Expected action 'register'", None, 400)

    # Lấy phần data (payload)
    data = req.get("data") or {}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return error_response("MISSING_FIELDS", "username and password required", None, 400)

    if dao_auth.get_user_by_username(username):
        return error_response("USER_EXISTS", "Username already exists", None, 400)

    pw_hash = generate_password_hash(password)
    user_id = dao_auth.create_user(username, pw_hash, email)
    return success_response({"userId": user_id}, 201)

"""
{
	"action": "login",        // hoặc "order", "remove", "update", ...
    "data": {
        "username": "admin",
        "password": "admin"
    },
    "meta": {                 // optional: thông tin thêm
    "requestId": "abc123",
    "timestamp": "2025-09-22T09:15:00Z",
    "client": "web"
    }
}
"""
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    POST /auth/login
    ---
    tags:
      - Authentication
    summary: Login user
    description: Login with username and password. Returns access and refresh tokens.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [username, password]
            properties:
              username:
                type: string
              password:
                type: string
    responses:
      200:
        description: Login success
      401:
        description: Invalid credentials
    """
    start_request()
    req = request.get_json(force=True) or {}

    # Kiểm tra action
    action = req.get("action")
    if action != "login":
        return error_response("INVALID_ACTION", "Expected action 'login'", None, 400)

    # Lấy phần data (payload)
    data = req.get("data") or {}
    # start_request()
    # data = request.get_json(force=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return error_response("MISSING_CREDENTIALS", "username and password required", None, 400)

    user = dao_auth.get_user_by_username(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return error_response("INVALID_CREDENTIALS", "Invalid username or password", None, 401)

    user_id = str(user["id"])  # ✅ Use user ID as string identity
    access = create_access_token(identity=user_id)
    refresh = create_refresh_token(identity=user_id)

    return success_response({
        "userId": user["id"],
        "token": access,
        "refreshToken": refresh
    }, 200)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    POST /auth/refresh
    ---
    tags:
      - Authentication
    summary: Refresh access token
    description: Use refresh token to obtain a new access token.
    security:
      - bearerAuth: []
    responses:
      200:
        description: New access token generated
      401:
        description: Invalid or missing refresh token
    """
    start_request()
    identity = get_jwt_identity()  # ✅ Returns user ID as string
    new_access = create_access_token(identity=identity)
    return success_response({"token": new_access})


@auth_bp.route("/logout_access", methods=["POST"])
@jwt_required()
def logout_access():
    """
    POST /auth/logout_access
    ---
    tags:
      - Authentication
    summary: Revoke access token
    description: Invalidate the current access token by adding its jti to blocklist.
    security:
      - bearerAuth: []
    responses:
      200:
        description: Access token revoked
    """
    start_request()
    jti = get_jwt()["jti"]
    uid = get_jwt_identity()  # user ID (string)
    dao_auth.add_token_to_blocklist(jti, "access", uid)
    return success_response({"revoked": True})


@auth_bp.route("/logout_refresh", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    """
    POST /auth/logout_refresh
    ---
    tags:
      - Authentication
    summary: Revoke refresh token
    description: Invalidate the current refresh token by adding its jti to blocklist.
    security:
      - bearerAuth: []
    responses:
      200:
        description: Refresh token revoked
    """
    start_request()
    jti = get_jwt()["jti"]
    uid = get_jwt_identity()  # user ID (string)
    dao_auth.add_token_to_blocklist(jti, "refresh", uid)
    return success_response({"revoked": True})


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    """
    GET /auth/me
    ---
    tags:
      - Authentication
    summary: Get current user info
    description: Get authenticated user's information using the access token.
    security:
      - bearerAuth: []
    responses:
      200:
        description: User info returned
      401:
        description: Unauthorized or invalid token
      404:
        description: User not found
    """
    start_request()
    identity = get_jwt_identity()

    # Nếu identity là string thì có thể là user_id
    user_id = identity.get("id") if isinstance(identity, dict) else identity

    if not user_id:
        return error_response("INVALID_TOKEN", "User ID not found in token", None, 401)

    user = dao_auth.get_user_by_id(user_id)
    if not user:
        return error_response("USER_NOT_FOUND", "User does not exist", None, 404)

    user_info = {
        "id": user["id"],
        "username": user["username"],
        "email": user.get("email")
    }

    return success_response({"user": user_info})
