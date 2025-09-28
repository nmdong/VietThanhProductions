"""
Order routes (CRUD operations for orders and their items).

These endpoints handle creation, retrieval, updating, and deletion of orders,
as well as management of order details (multiple products per order).

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

from flask import Blueprint, jsonify
from marshmallow import ValidationError
from db import dao_order
from models.order_schema import OrderSchema
from utils.response import parse_request

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

"""
{
  "action": "order",
  "data": {
    "order_number": "ORD001",
    "customer_name": "Nguyen Van A",
    "status": "pending",
    "items": [
      { "product_id": 1, "quantity": 2, "unit_price": 15000 },
      { "product_id": 2, "quantity": 1, "unit_price": 20000 }
    ]
  },
  "meta": {
    "requestId": "abc123",
    "timestamp": "2025-09-22T09:15:00Z",
    "client": "web"
  }
}

"""
@orders_bp.route("/", methods=["POST"])
def create_order():
    """
    POST /orders/
    ---
    tags:
      - Orders
    summary: Create a new order
    description: Create a new order with customer details and a list of order items (wrapped in {action, data, meta} format).
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [action, data]
            properties:
              action:
                type: string
                example: order
              data:
                type: object
                required: [order_number, customer_name, status, items]
                properties:
                  order_number:
                    type: string
                  customer_name:
                    type: string
                  status:
                    type: string
                  items:
                    type: array
                    items:
                      type: object
                      required: [product_id, quantity, unit_price]
                      properties:
                        product_id:
                          type: integer
                        quantity:
                          type: integer
                        unit_price:
                          type: number
              meta:
                type: object
                description: Optional metadata
    responses:
      201:
        description: Order created successfully
      400:
        description: Invalid input or missing fields
    """
    data, meta, error = parse_request("order")
    if error:
        return error

    try:
        validated = order_schema.load(data)
    except ValidationError as err:
        return jsonify({
            "status": "error",
            "error": err.messages,
            "meta": meta
        }), 400

    try:
        order_id = dao_order.create_order(
            order_number=validated["order_number"],
            customer_name=validated["customer_name"],
            status=validated["status"],
            items=validated["items"]
        )
        order = dao_order.get_order_by_id(order_id)
        return jsonify({
            "status": "success",
            "data": order_schema.dump(order),
            "meta": meta
        }), 201
    except ValueError as e:
        return jsonify({
            "status": "error",
            "error": {"message": str(e)},
            "meta": meta
        }), 400


@orders_bp.route("/", methods=["GET"])
def list_orders():
    """
    GET /orders/
    ---
    tags:
      - Orders
    summary: List all orders
    description: Retrieve a list of all orders with their details (including items).
    responses:
      200:
        description: Orders returned successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: success
                data:
                  type: array
                  items:
                    $ref: '#/components/schemas/Order'
                meta:
                  type: object
    """
    orders = dao_order.get_all_orders()
    return jsonify({
        "status": "success",
        "data": orders_schema.dump(orders),
        "meta": {}
    })


@orders_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """
    GET /orders/{order_id}
    ---
    tags:
      - Orders
    summary: Get an order by ID
    description: Retrieve a single order and its items using the order ID.
    parameters:
      - name: order_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Order retrieved successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
      404:
        description: Order not found
    """
    order = dao_order.get_order_by_id(order_id)
    if not order:
        return jsonify({
            "status": "error",
            "error": {"message": "Order not found"},
            "meta": {}
        }), 404
    return jsonify({
        "status": "success",
        "data": order_schema.dump(order),
        "meta": {}
    })

"""
{
  "action": "update",
  "data": {
    "status": "shipped"
  },
  "meta": {
    "requestId": "upd001",
    "client": "mobile"
  }
}

"""
@orders_bp.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    """
    PUT /orders/{order_id}
    ---
    tags:
      - Orders
    summary: Update an order
    description: Update the status of an existing order.
    parameters:
      - name: order_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              status:
                type: string
                example: shipped
    responses:
      200:
        description: Order updated successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
      400:
        description: Missing or invalid status
      404:
        description: Order not found
    """
    data, meta, error = parse_request("update")
    if error:
        return error

    if "status" not in data:
        return jsonify({
            "status": "error",
            "error": {"message": "Missing status"},
            "meta": meta
        }), 400

    dao_order.update_order_status(order_id, data["status"])
    order = dao_order.get_order_by_id(order_id)
    if not order:
        return jsonify({
            "status": "error",
            "error": {"message": "Order not found"},
            "meta": meta
        }), 404
    return jsonify({
        "status": "success",
        "data": order_schema.dump(order),
        "meta": meta
    })

"""
{
  "action": "remove",
  "data": {},
  "meta": {
    "requestId": "del123"
  }
}
"""
@orders_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    """
    DELETE /orders/{order_id}
    ---
    tags:
      - Orders
    summary: Delete an order
    description: Delete an existing order along with its items.
    parameters:
      - name: order_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Order deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Order 123 deleted
      404:
        description: Order not found
    """
    data, meta, error = parse_request("remove")
    if error:
        return error

    deleted = dao_order.delete_order(order_id)
    if not deleted:
        return jsonify({
            "status": "error",
            "error": {"message": "Order not found"},
            "meta": meta
        }), 404
    return jsonify({
        "status": "success",
        "data": {"message": f"Order {order_id} deleted"},
        "meta": meta
    })

"""
{
  "action": "add_item",
  "data": {
    "product_id": 3,
    "quantity": 5,
    "unit_price": 12000
  },
  "meta": {
    "requestId": "itm999",
    "client": "web"
  }
}
"""
@orders_bp.route("/<int:order_id>/items", methods=["POST"])
def add_item(order_id):
    """
    POST /orders/{order_id}/items
    ---
    tags:
      - Orders
    summary: Add item to order
    description: Add a product as an item to an existing order.
    parameters:
      - name: order_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - product_id
              - quantity
              - unit_price
            properties:
              product_id:
                type: integer
                example: 101
              quantity:
                type: integer
                example: 2
              unit_price:
                type: number
                format: float
                example: 19.99
    responses:
      201:
        description: Item added successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
      400:
        description: Missing required fields or invalid data
      404:
        description: Order not found
    """
    data, meta, error = parse_request("add_item")
    if error:
        return error

    if not all(k in data for k in ("product_id", "quantity", "unit_price")):
        return jsonify({
            "status": "error",
            "error": {"message": "Missing product_id, quantity or unit_price"},
            "meta": meta
        }), 400

    try:
        dao_order.add_item_to_order(order_id, data["product_id"], data["quantity"], data["unit_price"])
        order = dao_order.get_order_by_id(order_id)
        if not order:
            return jsonify({
                "status": "error",
                "error": {"message": "Order not found"},
                "meta": meta
            }), 404
        return jsonify({
            "status": "success",
            "data": order_schema.dump(order),
            "meta": meta
        }), 201
    except ValueError as e:
        return jsonify({
            "status": "error",
            "error": {"message": str(e)},
            "meta": meta
        }), 400
