from flask import Blueprint, request, jsonify
from db import dao_user
from models.user_schema import UserSchema

user_bp = Blueprint("user", __name__, url_prefix="")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route("/users", methods=["GET"])
def get_users():
    return jsonify(users_schema.dump(dao_user.fetch_all_users()))

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = dao_user.fetch_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_schema.dump(user))

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user_id = dao_user.create_user(data["name"], data["email"], data["age"])
    new_user = dao_user.fetch_user_by_id(user_id)
    return jsonify(user_schema.dump(new_user)), 201

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json(force=True)
    # validate partial allowed — you can validate fields manually if needed
    updated = dao_user.update_user(
        user_id,
        name=data.get("name"),
        email=data.get("email"),
        age=data.get("age")
    )
    if updated == 0:
        return jsonify({"error": "User not found or no fields updated"}), 404
    updated_user = dao_user.fetch_user_by_id(user_id)
    return jsonify(user_schema.dump(updated_user))

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    deleted = dao_user.delete_user(user_id)
    if deleted == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"deleted": deleted})
