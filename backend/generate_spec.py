import yaml, os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

# ================================
# Tạo spec Swagger 2.0
# ================================
spec = APISpec(
    title="Access Backend API",
    version="1.0.0",
    openapi_version="2.0",  # Swagger 2.0
    plugins=[MarshmallowPlugin()]
)

template = spec.to_dict()

# Chỉ giữ swagger: "2.0", xóa openapi nếu có
template.pop("openapi", None)
template["swagger"] = "2.0"
template.setdefault("paths", {})

# ================================
# JWT security
# ================================
template["securityDefinitions"] = {
    "Bearer": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header",
        "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
    }
}

# ================================
# AUTH ROUTES
# ================================
auth_paths = {
    "/auth/login": {
        "post": {
            "summary": "Login to get JWT token",
            "tags": ["Auth"],
            "parameters": [{
                "in": "body",
                "name": "credentials",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "password": {"type": "string"}
                    },
                    "required": ["username", "password"]
                }
            }],
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
            "parameters": [{
                "in": "body",
                "name": "user",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "email": {"type": "string"},
                        "password": {"type": "string"}
                    },
                    "required": ["username", "email", "password"]
                }
            }],
            "responses": {
                "201": {"description": "User successfully registered"},
                "400": {"description": "Bad request"}
            }
        }
    },
    "/auth/logout_access": {
        "post": {
            "summary": "Logout (revoke access token)",
            "tags": ["Auth"],
            "responses": {"200": {"description": "Logged out"}},
            "security": [{"Bearer": []}]
        }
    },
    "/auth/refresh": {
        "post": {
            "summary": "Refresh JWT token",
            "tags": ["Auth"],
            "responses": {"200": {"description": "New token"}},
            "security": [{"Bearer": []}]
        }
    },
    "/auth/me": {
        "get": {
            "summary": "Get current user info",
            "tags": ["Auth"],
            "responses": {
                "200": {"description": "User info returned"},
                "401": {"description": "Unauthorized"},
                "404": {"description": "User not found"}
            },
            "security": [{"Bearer": []}]
        }
    }
}

# ================================
# ORDERS ROUTES
# ================================
orders_paths = {
    "/orders": {
        "get": {
            "summary": "List all orders",
            "tags": ["Orders"],
            "responses": {"200": {"description": "List of orders"}},
            "security": [{"Bearer": []}]
        },
        "post": {
            "summary": "Create new order",
            "tags": ["Orders"],
            "parameters": [{
                "in": "body",
                "name": "order",
                "required": True,
                "schema": {"type": "object"}
            }],
            "responses": {
                "201": {"description": "Order created"},
                "400": {"description": "Invalid input"}
            },
            "security": [{"Bearer": []}]
        }
    },
    "/orders/{order_id}": {
        "get": {
            "summary": "Get order by ID",
            "tags": ["Orders"],
            "parameters": [{
                "in": "path",
                "name": "order_id",
                "type": "string",
                "required": True
            }],
            "responses": {
                "200": {"description": "Order details"},
                "404": {"description": "Order not found"}
            },
            "security": [{"Bearer": []}]
        },
        "put": {
            "summary": "Update order by ID",
            "tags": ["Orders"],
            "parameters": [
                {
                    "in": "path",
                    "name": "order_id",
                    "type": "string",
                    "required": True
                },
                {
                    "in": "body",
                    "name": "order",
                    "required": True,
                    "schema": {"type": "object"}
                }
            ],
            "responses": {
                "200": {"description": "Order updated"},
                "404": {"description": "Order not found"}
            },
            "security": [{"Bearer": []}]
        },
        "delete": {
            "summary": "Delete order by ID",
            "tags": ["Orders"],
            "parameters": [{
                "in": "path",
                "name": "order_id",
                "type": "string",
                "required": True
            }],
            "responses": {
                "200": {"description": "Order deleted"},
                "404": {"description": "Order not found"}
            },
            "security": [{"Bearer": []}]
        }
    }
}

# ================================
# PRODUCTS ROUTES
# ================================
products_paths = {
    "/products": {
        "get": {
            "summary": "List all products",
            "tags": ["Products"],
            "responses": {"200": {"description": "List of products"}},
            "security": [{"Bearer": []}]
        },
        "post": {
            "summary": "Create new product",
            "tags": ["Products"],
            "parameters": [{
                "in": "body",
                "name": "product",
                "required": True,
                "schema": {"type": "object"}
            }],
            "responses": {
                "201": {"description": "Product created"},
                "400": {"description": "Invalid input"}
            },
            "security": [{"Bearer": []}]
        }
    },
    "/products/{product_id}": {
        "get": {
            "summary": "Get product by ID",
            "tags": ["Products"],
            "parameters": [{
                "in": "path",
                "name": "product_id",
                "type": "string",
                "required": True
            }],
            "responses": {
                "200": {"description": "Product details"},
                "404": {"description": "Product not found"}
            },
            "security": [{"Bearer": []}]
        },
        "put": {
            "summary": "Update product by ID",
            "tags": ["Products"],
            "parameters": [
                {
                    "in": "path",
                    "name": "product_id",
                    "type": "string",
                    "required": True
                },
                {
                    "in": "body",
                    "name": "product",
                    "required": True,
                    "schema": {"type": "object"}
                }
            ],
            "responses": {
                "200": {"description": "Product updated"},
                "404": {"description": "Product not found"}
            },
            "security": [{"Bearer": []}]
        },
        "delete": {
            "summary": "Delete product by ID",
            "tags": ["Products"],
            "parameters": [{
                "in": "path",
                "name": "product_id",
                "type": "string",
                "required": True
            }],
            "responses": {
                "200": {"description": "Product deleted"},
                "404": {"description": "Product not found"}
            },
            "security": [{"Bearer": []}]
        }
    }
}

# ================================
# Gộp tất cả paths
# ================================
template["paths"].update(auth_paths)
template["paths"].update(orders_paths)
template["paths"].update(products_paths)

# ================================
# Ghi ra file swagger_generated.yaml
# ================================
out = os.path.join("swagger", "swagger_generated.yaml")
os.makedirs("swagger", exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    yaml.safe_dump(template, f, allow_unicode=True, default_flow_style=False)

print("Wrote", out)
print("Available routes:", list(template["paths"].keys()))
