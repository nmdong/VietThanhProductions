"""
Order CRUD routes mapped to db.dao_order.

Endpoints:
- GET /orders
- GET /orders/<id>
- POST /orders
- PUT /orders/<id>
- DELETE /orders/<id>
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
import db.dao_order as dao_order
from utils.response import success_response, error_response, start_request

order_bp = Blueprint("orders", __name__, url_prefix="/orders")

@order_bp.before_request
def before():
    start_request()

@order_bp.route("", methods=["GET"])
def list_orders():
    rows = dao_order.fetch_all_orders()
    return success_response({"orders": rows})

@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    row = dao_order.fetch_order_by_id(order_id)
    if not row:
        return error_response("NOT_FOUND", "Order not found", None, 404)
    return success_response({"order": row})

@order_bp.route("", methods=["POST"])
@jwt_required()
def create_order():
    data = request.get_json(force=True) or {}
    required = ["order_number", "customer_name"]
    if not all(k in data for k in required):
        return error_response("INVALID_INPUT", "order_number and customer_name required", None, 400)
    new_id = dao_order.create_order(
        order_number = data.get("order_number"),
        customer_name = data.get("customer_name"),
        product_id = data.get("product_id"),
        quantity = data.get("quantity", 1),
        unit_price = data.get("unit_price"),
        total_price = data.get("total_price"),
        order_date = data.get("order_date"),
        status = data.get("status", "NEW")
    )
    return success_response({"OrderID": new_id}, 201)

@order_bp.route("/<int:order_id>", methods=["PUT"])
@jwt_required()
def update_order(order_id):
    data = request.get_json(force=True) or {}
    updated = dao_order.update_order(order_id, **data)
    if updated == 0:
        return error_response("NOT_UPDATED", "Order not found or no changes", None, 404)
    updated_row = dao_order.fetch_order_by_id(order_id)
    return success_response({"order": updated_row})

@order_bp.route("/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete_order(order_id):
    deleted = dao_order.delete_order(order_id)
    if deleted == 0:
        return error_response("NOT_FOUND", "Order not found", None, 404)
    return success_response({"deleted": deleted})
