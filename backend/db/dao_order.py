"""
DAO for order-related DB operations with multiple products.

Tables used:
- orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT,
    customer_name TEXT,
    order_date TEXT,
    status TEXT,
    total_price REAL
)

- order_items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    total_price REAL
)
"""

from .connection import get_conn
from datetime import datetime


def create_order(order_number: str, customer_name: str, status: str,
                 items: list) -> int:
    """
    Insert a new order with multiple items.

    Args:
        order_number (str): Order number
        customer_name (str): Customer name
        status (str): Order status
        items (list[dict]): List of product items, each dict:
            {
                "product_id": int,
                "quantity": int,
                "unit_price": float
            }

    Returns:
        int: new order id
    """
    conn = get_conn()
    cur = conn.cursor()
    order_date = datetime.utcnow().isoformat()

    # Tính tổng giá đơn hàng
    total_price = sum(i["quantity"] * i["unit_price"] for i in items)

    # Thêm vào bảng orders
    cur.execute("""
        INSERT INTO orders (order_number, customer_name, order_date, status, total_price)
        VALUES (?, ?, ?, ?, ?)
    """, (order_number, customer_name, order_date, status, total_price))
    cur.execute("SELECT @@IDENTITY")
    order_id = int(cur.fetchone()[0])

    # Thêm từng sản phẩm vào order_items
    for i in items:
        qty = i["quantity"]
        unit_price = i["unit_price"]
        subtotal = qty * unit_price
        cur.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, i["product_id"], qty, unit_price, subtotal))

    conn.commit()
    cur.close(); conn.close()
    return order_id


def get_order_by_id(order_id: int):
    """
    Retrieve order with all its items.
    """
    conn = get_conn()
    cur = conn.cursor()

    # Lấy thông tin order
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order_row = cur.fetchone()
    if not order_row:
        cur.close(); conn.close(); return None
    order_cols = [c[0] for c in cur.description]
    order_data = dict(zip(order_cols, order_row))

    # Lấy danh sách items
    cur.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    item_rows = cur.fetchall()
    item_cols = [c[0] for c in cur.description]
    items = [dict(zip(item_cols, r)) for r in item_rows]

    order_data["items"] = items

    cur.close(); conn.close()
    return order_data


def get_orders_by_customer(customer_name: str):
    """
    Retrieve all orders (with items) for a given customer.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM orders WHERE customer_name = ?", (customer_name,))
    order_ids = [row[0] for row in cur.fetchall()]
    cur.close(); conn.close()

    return [get_order_by_id(oid) for oid in order_ids]


def update_order_status(order_id: int, new_status: str):
    """
    Update order status.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    cur.close(); conn.close()


def add_item_to_order(order_id: int, product_id: int, quantity: int, unit_price: float):
    """
    Add new item to an existing order and update total_price.
    """
    conn = get_conn()
    cur = conn.cursor()
    subtotal = quantity * unit_price

    # Thêm item
    cur.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
        VALUES (?, ?, ?, ?, ?)
    """, (order_id, product_id, quantity, unit_price, subtotal))

    # Cập nhật tổng giá đơn hàng
    cur.execute("UPDATE orders SET total_price = total_price + ? WHERE id = ?", (subtotal, order_id))

    conn.commit()
    cur.close(); conn.close()

def get_all_orders():
    """
    Retrieve all orders with their items.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM orders ORDER BY order_date DESC")
    order_ids = [row[0] for row in cur.fetchall()]
    cur.close(); conn.close()
    return [get_order_by_id(oid) for oid in order_ids]


def delete_order(order_id: int) -> bool:
    """
    Delete an order and its items.
    Returns True if deleted, False if not found.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM orders WHERE id = ?", (order_id,))
    if cur.fetchone()[0] == 0:
        cur.close(); conn.close()
        return False

    cur.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
    cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    cur.close(); conn.close()
    return True

