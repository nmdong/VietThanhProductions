"""
Product routes (CRUD operations).

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
from flask_jwt_extended import jwt_required
from utils.response import success_response, error_response, start_request, parse_request
from db.dao_products import (
    create_product,
    get_product_by_id,
    get_all_products,
    update_product,
    delete_product,
    advanced_search
)

products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.before_request
def before():
    """Initialize request metadata for all product routes."""
    start_request()


@products_bp.route("/", methods=["GET"])
@jwt_required()
def list_products():
    """
    GET /products/
    ---
    tags:
      - Products
    summary: List all products
    description: Retrieve all products in the system.
    security:
      - bearerAuth: []
    responses:
      200:
        description: List of products
        content:
          application/json:
            example:
              status: success
              data:
                products:
                  - id: 1
                    code: "P001"
                    name: "Laptop"
                    price: 1200.5
                    stock: 10
                  - id: 2
                    code: "P002"
                    name: "Phone"
                    price: 800.0
                    stock: 5
              meta: {}
    """
    products = get_all_products()
    return success_response({"products": products})


@products_bp.route("/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id):
    """
    GET /products/{product_id}
    ---
    tags:
      - Products
    summary: Get product by ID
    description: Retrieve product details using its unique ID.
    parameters:
      - name: product_id
        in: path
        required: true
        schema:
          type: integer
    security:
      - bearerAuth: []
    responses:
      200:
        description: Product found
        content:
          application/json:
            example:
              status: success
              data:
                product:
                  id: 1
                  code: "P001"
                  name: "Laptop"
                  price: 1200.5
                  stock: 10
              meta: {}
      404:
        description: Product not found
    """
    product = get_product_by_id(product_id)
    if not product:
        return error_response("NOT_FOUND", "Product not found", None, 404)
    return success_response({"product": product})

"""
{
  "action": "create",
  "data": { ... },
  "meta": {
    "requestId": "xxx",
    "timestamp": "2025-09-22T10:00:00Z",
    "client": "web"
  }
}
"""
@products_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    """
    POST /products/
    ---
    tags:
      - Products
    summary: Create a new product
    description: Add a new product with code, name, price, stock, etc.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [code, name, category, price, stock]
            properties:
              code: { type: string }
              name: { type: string }
              category: { type: string }
              subcategory: { type: string }
              color: { type: string }
              size: { type: string }
              material: { type: string }
              feature: { type: string }
              price: { type: number }
              stock: { type: integer }
          example:
            code: "P003"
            name: "Tablet"
            category: "Electronics"
            price: 450.0
            stock: 20
    security:
      - bearerAuth: []
    responses:
      201:
        description: Product created
        content:
          application/json:
            example:
              status: success
              data:
                productId: 3
              meta: {}
      400:
        description: Missing fields
    """
    data, meta, error = parse_request("create")
    if error:
        return error    # error là tuple (jsonify(...), status_code)

    try:
        product_id = create_product(data)
        return success_response({"productId": product_id}, 201)
    except Exception as e:
        return error_response("CREATE_FAILED", str(e), None, 500)


@products_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update(product_id):
    """
    PUT /products/{product_id}
    ---
    tags:
      - Products
    summary: Update a product
    description: Update details of a product by ID.
    parameters:
      - name: product_id
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
              code: { type: string }
              name: { type: string }
              category: { type: string }
              subcategory: { type: string }
              color: { type: string }
              size: { type: string }
              material: { type: string }
              feature: { type: string }
              price: { type: number }
              stock: { type: integer }
          example:
            name: "Tablet Pro"
            price: 600.0
            stock: 15
    security:
      - bearerAuth: []
    responses:
      200:
        description: Product updated
        content:
          application/json:
            example:
              status: success
              data:
                updated: true
              meta: {}
      404:
        description: Product not found
    """
    # data = request.get_json(force=True) or {}
    data, meta, error = parse_request("update_product")
    if error:
        return error

    try:
        updated = update_product(product_id, data)
        if not updated:
            return error_response("NOT_FOUND", "Product not found", None, 404)
        return success_response({"updated": True})
    except Exception as e:
        return error_response("UPDATE_FAILED", str(e), None, 500)


@products_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete(product_id):
    """
    DELETE /products/{product_id}
    ---
    tags:
      - Products
    summary: Delete a product
    description: Remove a product by ID.
    parameters:
      - name: product_id
        in: path
        required: true
        schema:
          type: integer
    security:
      - bearerAuth: []
    responses:
      200:
        description: Product deleted
        content:
          application/json:
            example:
              status: success
              data:
                deleted: true
              meta: {}
      404:
        description: Product not found
    """
    try:
        deleted = delete_product(product_id)
        if not deleted:
            return error_response("NOT_FOUND", "Product not found", None, 404)
        return success_response({"deleted": True})
    except Exception as e:
        return error_response("DELETE_FAILED", str(e), None, 500)

"""
{
  "action": "advanced_search",
  "data": {
    "keyword": "tablet",
    "category": "Electronics",
    "min_price": 300,
    "max_price": 800,
    "in_stock": true,
    "color": "black",
    "material": "plastic"
  },
  "meta": {
    "requestId": "req-adv-001"
  }
}
"""
@products_bp.route("/search/advanced", methods=["POST"])
@jwt_required()
def search_advanced():
    """
    POST /products/search/advanced
    ---
    tags:
      - Products
    summary: Advanced search products
    description: Search products with multiple optional filters (keyword, category, price range, stock, color, material).
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
                enum: [advanced_search]
              data:
                type: object
                properties:
                  keyword: { type: string }
                  category: { type: string }
                  min_price: { type: number }
                  max_price: { type: number }
                  in_stock: { type: boolean }
                  color: { type: string }
                  material: { type: string }
              meta:
                type: object
          example:
            action: advanced_search
            data:
              keyword: "tablet"
              category: "Electronics"
              min_price: 300
              max_price: 800
              in_stock: true
              color: "black"
              material: "plastic"
            meta:
              requestId: "req-adv-001"
    security:
      - bearerAuth: []
    responses:
      200:
        description: Search results
        content:
          application/json:
            example:
              status: success
              data:
                - id: 12
                  code: "PRD-0012"
                  name: "Tablet Pro"
                  category: "Electronics"
                  price: 650.0
                  stock: 20
              meta:
                requestId: "req-adv-001"
    """
    data, meta, err = parse_request("advanced_search")
    if err:
        return err

    try:
        products = advanced_search(
            keyword=data.get("keyword"),
            category=data.get("category"),
            min_price=data.get("min_price"),
            max_price=data.get("max_price"),
            in_stock=data.get("in_stock"),
            color=data.get("color"),
            material=data.get("material"),
        )
        return success_response(products, 200)
    except Exception as e:
        return error_response("SEARCH_FAILED", str(e), meta, 500)
