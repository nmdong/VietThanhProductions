# swagger/generate_auth_only.py
import yaml, os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

# ================================
# Tạo spec OpenAPI 3.0
# ================================
spec = APISpec(
    title="Access Backend API",
    version="1.0.0",
    openapi_version="3.0.3",   # Dùng OpenAPI 3
    plugins=[MarshmallowPlugin()]
)

template = spec.to_dict()
template.setdefault('paths', {})

# ================================
# JWT security (Bearer)
# ================================
template['components'] = {
    "securitySchemes": {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
}
# Áp dụng global security cho tất cả routes
template['security'] = [{"bearerAuth": []}]

# ================================
# AUTH ROUTES
# ================================
auth_paths = {
    "/auth/login": {
        "post": {
            "summary": "Login to get JWT token",
            "tags": ["Auth"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string"},
                                "password": {"type": "string"}
                            },
                            "required": ["username", "password"]
                        }
                    }
                }
            },
            "responses": {
                "200": {"description": "JWT token returned"},
                "401": {"description": "Unauthorized"}
            }
        }
    },
    "/auth/register": {
        "post": {
            "summary": "Register a new user",
            "tags": ["Auth"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string"},
                                "email": {"type": "string"},
                                "password": {"type": "string"}
                            },
                            "required": ["username", "email", "password"]
                        }
                    }
                }
            },
            "responses": {
                "201": {"description": "User successfully registered"},
                "400": {"description": "Bad request, e.g., user exists or invalid data"}
            }
        }
    },
    "/auth/logout_access": {
        "post": {
            "summary": "Logout (revoke access token)",
            "tags": ["Auth"],
            "responses": {"200": {"description": "Logged out"}},
            "security": [{"bearerAuth": []}]
        }
    },
    "/auth/refresh": {
        "post": {
            "summary": "Refresh JWT token",
            "tags": ["Auth"],
            "responses": {"200": {"description": "New token"}},
            "security": [{"bearerAuth": []}]
        }
    },
    "/auth/me": {
        "get": {
            "summary": "Get current user info",
            "tags": ["Auth"],
            "responses": {
                "200": {"description": "User info returned"},
                "401": {"description": "Unauthorized or invalid token"},
                "404": {"description": "User not found"}
            },
            "security": [{"bearerAuth": []}]
        }
    }
}

template['paths'].update(auth_paths)

# ================================
# Ghi ra file swagger_generated.yaml
# ================================
out = os.path.join("swagger", "swagger_generated.yaml")
os.makedirs("swagger", exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    yaml.safe_dump(template, f, allow_unicode=True, sort_keys=False)

print("Wrote", out)
print("Available routes:", list(template['paths'].keys()))
