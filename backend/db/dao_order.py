"""
DAO for orders table (assumes table 'orders' exists).
Columns used: id, order_number, customer_name, product_id, quantity, unit_price, total_price, order_date, status
"""
from .connection import get_conn
from datetime import datetime

def fetch_all_orders():
    """
    Return list of all orders
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, order_number, customer_name, product_id, quantity, unit_price, total_price, order_date, status FROM orders")
    cols = [c[0] for c in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    cur.close(); conn.close()
    return rows

def fetch_order_by_id(order_id: int):
    """
    Return order dict or None
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, order_number, customer_name, product_id, quantity, unit_price, total_price, order_date, status FROM orders WHERE id = ?", (order_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close(); return None
    cols = [c[0] for c in cur.description]
    res = dict(zip(cols, row))
    cur.close(); conn.close()
    return res

def create_order(order_number: str, customer_name: str, product_id: int = None, quantity: int = 1, unit_price: float = None, total_price: float = None, order_date: str = None, status: str = "NEW") -> int:
    """
    Insert new order. If total_price is None, compute from unit_price * quantity.
    order_date: ISO string or None → stored as string/Access datetime depending driver.
    Returns new order id.
    """
    if order_date is None:
        order_date = datetime.utcnow().isoformat()
    if total_price is None:
        unit = unit_price or 0.0
        total_price = unit * (quantity or 0)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (order_number, customer_name, product_id, quantity, unit_price, total_price, order_date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (order_number, customer_name, product_id, quantity, unit_price, total_price, order_date, status)
    )
    cur.execute("SELECT @@IDENTITY")
    new_id = int(cur.fetchone()[0])
    conn.commit()
    cur.close(); conn.close()
    return new_id

def update_order(order_id: int, **kwargs) -> int:
    """
    Update order fields passed in kwargs. Returns affected rows count.
    """
    if not kwargs:
        return 0
    # if quantity/unit_price changed and no total_price, recompute
    if ("quantity" in kwargs or "unit_price" in kwargs) and "total_price" not in kwargs:
        cur_order = fetch_order_by_id(order_id)
        if cur_order:
            q = kwargs.get("quantity", cur_order.get("quantity") or 0)
            u = kwargs.get("unit_price", cur_order.get("unit_price") or 0)
            kwargs["total_price"] = (q or 0) * (u or 0)
    updates = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    params = list(kwargs.values()) + [order_id]
    conn = get_conn()
    cur = conn.cursor()
    sql = f"UPDATE orders SET {updates} WHERE id = ?"
    cur.execute(sql, params)
    affected = cur.rowcount
    conn.commit()
    cur.close(); conn.close()
    return affected

def delete_order(order_id: int) -> int:
    """
    Delete order by id. Return affected rows.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    affected = cur.rowcount
    conn.commit()
    cur.close(); conn.close()
    return affected
