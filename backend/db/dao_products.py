"""
DAO cho các thao tác với CSDL liên quan đến sản phẩm.

Bảng sử dụng:

* products(
  id INTEGER PRIMARY KEY AUTOINCREMENT,   -- khóa chính, tự tăng
  code TEXT,                              -- mã sản phẩm
  name TEXT,                              -- tên sản phẩm
  category TEXT,                          -- danh mục chính
  subcategory TEXT,                       -- danh mục phụ
  color TEXT,                             -- màu sắc
  size TEXT,                              -- kích thước/dung tích
  material TEXT,                          -- chất liệu
  feature TEXT,                           -- đặc điểm bổ sung
  price REAL,                             -- giá
  stock INTEGER,                          -- số lượng tồn
  created_at TEXT,                        -- ngày tạo
  updated_at TEXT                         -- ngày cập nhật
)
"""
from .connection import get_conn
from datetime import datetime


def access_now():
    """Trả về thời gian hiện tại theo định dạng Access (MM/DD/YYYY HH:MM:SS)."""
    return datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")


def create_product(data: dict) -> int:
    """
    Thêm một sản phẩm mới vào bảng products từ dict dữ liệu.

    Args:
        data (dict): dữ liệu sản phẩm (code, name, category, price, stock, ...)

    Returns:
        int: id sản phẩm vừa tạo
    """
    conn = get_conn()
    cur = conn.cursor()
    try:
        created_at = updated_at = access_now()

        cur.execute(
            """
            INSERT INTO products 
            (code, name, category, subcategory, color, size, material, feature, price, stock, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("code"),
                data.get("name"),
                data.get("category"),
                data.get("subcategory"),
                data.get("color"),
                data.get("size"),
                data.get("material"),
                data.get("feature"),
                data.get("price"),
                data.get("stock"),
                created_at,
                updated_at,
            ),
        )

        # Access không hỗ trợ lastrowid → dùng @@IDENTITY
        cur.execute("SELECT @@IDENTITY")
        new_id = cur.fetchone()[0]

        conn.commit()
        return int(new_id)
    finally:
        cur.close()
        conn.close()


def get_product_by_id(product_id: int):
    """Lấy thông tin sản phẩm theo ID."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cur.fetchone()
        if not row:
            return None
        cols = [c[0] for c in cur.description]
        return dict(zip(cols, row))
    finally:
        cur.close()
        conn.close()


def get_all_products():
    """Lấy toàn bộ sản phẩm."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        cur.close()
        conn.close()


def search_products(keyword: str, category: str = None):
    """Tìm sản phẩm theo từ khóa trong code hoặc name, có thể lọc theo category."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        sql = "SELECT * FROM products WHERE (code LIKE ? OR name LIKE ?)"
        params = [f"%{keyword}%", f"%{keyword}%"]

        if category:
            sql += " AND category = ?"
            params.append(category)

        cur.execute(sql, params)
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        cur.close()
        conn.close()


def advanced_search(
    keyword: str = None,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    in_stock: bool = None,
    color: str = None,
    material: str = None,
):
    """Tìm kiếm nâng cao với nhiều điều kiện tùy chọn."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        sql = "SELECT * FROM products WHERE 1=1"
        params = []

        if keyword:
            sql += " AND (code LIKE ? OR name LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])

        if category:
            sql += " AND category = ?"
            params.append(category)

        if min_price is not None:
            sql += " AND price >= ?"
            params.append(min_price)

        if max_price is not None:
            sql += " AND price <= ?"
            params.append(max_price)

        if in_stock:
            sql += " AND stock > 0"

        if color:
            sql += " AND color = ?"
            params.append(color)

        if material:
            sql += " AND material = ?"
            params.append(material)

        cur.execute(sql, params)
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        cur.close()
        conn.close()


def update_stock(product_id: int, new_stock: int):
    """Cập nhật số lượng tồn kho cho sản phẩm."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        updated_at = access_now()
        cur.execute(
            "UPDATE products SET stock = ?, updated_at = ? WHERE id = ?",
            (new_stock, updated_at, product_id),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def decrease_stock(product_id: int, quantity: int) -> bool:
    """Giảm số lượng tồn kho nếu đủ hàng."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
        row = cur.fetchone()
        if not row:
            return False

        current_stock = row[0]
        if current_stock < quantity:
            return False

        new_stock = current_stock - quantity
        updated_at = access_now()
        cur.execute(
            "UPDATE products SET stock = ?, updated_at = ? WHERE id = ?",
            (new_stock, updated_at, product_id),
        )
        conn.commit()
        return True
    finally:
        cur.close()
        conn.close()


def update_product(product_id: int, fields: dict) -> bool:
    """
    Cập nhật sản phẩm (cập nhật một phần).
    Chỉ cho phép: name, price, stock, category, subcategory, color, size, material, feature
    """
    if not fields:
        return False

    allowed = {
        "name",
        "price",
        "stock",
        "category",
        "subcategory",
        "color",
        "size",
        "material",
        "feature",
    }
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return False

    set_clause = ", ".join([f"{k} = ?" for k in updates])
    values = list(updates.values())
    values.append(access_now())  # updated_at
    values.append(product_id)

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE products SET {set_clause}, updated_at = ? WHERE id = ?",
            values,
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        conn.close()


def delete_product(product_id: int) -> bool:
    """Xóa sản phẩm theo ID."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        conn.close()
