"""
Main Flask application setup.

Includes:
- JWT authentication & token blocklist.
- Swagger UI docs at /docs/.
- Error handling.
- Auth routes (login, register, refresh, logout).
- Orders routes (CRUD orders + items).
- Products routes (CRUD products).
- Dynamic CRUD routes auto-generated from DAO modules in /generated/.

All endpoints return payload in the project's unified format:
* Success:
  {
    "status": "success",
    "data": {...},
    "meta": {...}
  }
* Error:
  {
    "status": "error",
    "error": {...},
    "meta": {...}
  }
"""

import os, importlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
import yaml
from config import Config
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

# Import routes
from routes.auth_routes import auth_bp
from routes.orders_routes import orders_bp
from routes.products_routes import products_bp

import db.dao_auth as dao_auth

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
jwt = JWTManager(app)

# ----------------------------
# JWT blocklist check
# ----------------------------
@jwt.token_in_blocklist_loader
def check_if_revoked(jwt_header, jwt_payload):
    """Check if the token's JTI is present in blocklist."""
    jti = jwt_payload.get("jti")
    return dao_auth.is_token_revoked(jti)

# ----------------------------
# Error handler chung
# ----------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON-formatted error for unhandled exceptions."""
    return jsonify({
        "status": "error",
        "error": "Internal Server Error",
        "details": str(e)
    }), 500

# ----------------------------
# Swagger setup
# ----------------------------
swagger_path = os.path.join("swagger", "swagger_generated.yaml")
if os.path.exists(swagger_path):
    with open(swagger_path, "r", encoding="utf-8") as f:
        swagger_template = yaml.safe_load(f)
else:
    swagger_template = None

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",   # Docs: http://localhost:5000/docs/
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "security": [
        {"Bearer": []}
    ]
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

# ----------------------------
# Register blueprints
# ----------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(products_bp)

# ----------------------------
# Dynamic import DAO modules
# ----------------------------
DAO_MODULES = {}
gen_dir = os.path.join(os.path.dirname(__file__), "generated")
if os.path.isdir(gen_dir):
    for fname in os.listdir(gen_dir):
        if fname.startswith("dao_") and fname.endswith(".py"):
            module_name = "generated." + fname[:-3]
            key = fname[4:-3]   # dao_users.py -> "users"
            try:
                DAO_MODULES[key] = importlib.import_module(module_name)
            except Exception as e:
                print("Import failed", module_name, e)

# ----------------------------
# Dynamic CRUD endpoints
# ----------------------------
@app.route("/api/<table>", methods=["GET"])
@jwt_required()
def list_records(table):
    """List all records from a given table."""
    if table not in DAO_MODULES:
        return jsonify({"status": "error", "error": "table not found"}), 404
    dao = DAO_MODULES[table]
    fn = getattr(dao, f"fetch_all_{table}", None)
    if not fn:
        return jsonify({"status": "success", "data": []}), 200
    return jsonify({"status": "success", "data": fn()})

@app.route("/api/<table>/<record_id>", methods=["GET"])
@jwt_required()
def get_record(table, record_id):
    """Get single record by ID from a table."""
    if table not in DAO_MODULES:
        return jsonify({"status": "error", "error": "table not found"}), 404
    dao = DAO_MODULES[table]
    fn = getattr(dao, f"fetch_{table}_by_id", None)
    if not fn:
        return jsonify({"status": "error", "error": "not implemented"}), 500
    res = fn(record_id)
    if not res:
        return jsonify({"status": "error", "error": "not found"}), 404
    return jsonify({"status": "success", "data": res})

@app.route("/api/<table>", methods=["POST"])
@jwt_required()
def create_record(table):
    """Create a new record in the given table."""
    if table not in DAO_MODULES:
        return jsonify({"status": "error", "error": "table not found"}), 404
    dao = DAO_MODULES[table]
    fn = getattr(dao, f"create_{table}", None)
    if not fn:
        return jsonify({"status": "error", "error": "not implemented"}), 500
    data = request.get_json(force=True) or {}
    try:
        new_id = fn(**data)
        return jsonify({"status": "success", "data": {"id": new_id}}), 201
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

@app.route("/api/<table>/<record_id>", methods=["PUT"])
@jwt_required()
def update_record(table, record_id):
    """Update an existing record in the given table by ID."""
    if table not in DAO_MODULES:
        return jsonify({"status": "error", "error": "table not found"}), 404
    dao = DAO_MODULES[table]
    fn = getattr(dao, f"update_{table}", None)
    if not fn:
        return jsonify({"status": "error", "error": "not implemented"}), 500
    data = request.get_json(force=True) or {}
    affected = fn(record_id, **data)
    return jsonify({"status": "success", "data": {"updated": affected}})

@app.route("/api/<table>/<record_id>", methods=["DELETE"])
@jwt_required()
def delete_record(table, record_id):
    """Delete a record by ID from the given table."""
    if table not in DAO_MODULES:
        return jsonify({"status": "error", "error": "table not found"}), 404
    dao = DAO_MODULES[table]
    fn = getattr(dao, f"delete_{table}", None)
    if not fn:
        return jsonify({"status": "error", "error": "not implemented"}), 500
    affected = fn(record_id)
    return jsonify({"status": "success", "data": {"deleted": affected}})

# ----------------------------
# Example protected route
# ----------------------------
@app.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    """Return user profile info for the current JWT identity."""
    uid = get_jwt_identity()
    return jsonify({"status": "success", "data": {"msg": "protected", "user_id": uid}})


if __name__ == "__main__":
    from db.connection import init_db

    init_db()
    print("DB initialized, products table is ready!")

    app.run(debug=True, host="0.0.0.0", port=Config.PORT)

