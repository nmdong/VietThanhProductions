import pyodbc
from config import Config

def _driver_for_path(path: str) -> str:
    p = path.lower()
    if p.endswith(".accdb"):
        return "Microsoft Access Driver (*.mdb, *.accdb)"
    return "Microsoft Access Driver (*.mdb)"

def get_conn():
    driver = _driver_for_path(Config.DB_PATH)
    conn_str = rf"Driver={{{driver}}};DBQ={Config.DB_PATH};"
    return pyodbc.connect(conn_str, autocommit=False)

def safe_create(cur, ddl, name):
    try:
        cur.execute(ddl)
        print(f"✅ Table '{name}' created.")
    except Exception as e:
        if "already exists" in str(e):
            print(f"ℹ️ Table '{name}' already exists.")
        else:
            print(f"⚠️ Error creating '{name}':", e)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    TABLES = {
        "products": """
            CREATE TABLE products (
                id AUTOINCREMENT PRIMARY KEY,
                code TEXT(50),
                name TEXT(255),
                category TEXT(100),
                subcategory TEXT(100),
                color TEXT(50),
                size TEXT(50),
                material TEXT(100),
                feature TEXT(255),
                price DOUBLE,
                stock LONG,
                created_at DATETIME,
                updated_at DATETIME
            )
        """,
        "orders": """
            CREATE TABLE orders (
                id AUTOINCREMENT PRIMARY KEY,
                customer_name TEXT(255),
                total_amount DOUBLE,
                status TEXT(50),
                created_at DATETIME,
                updated_at DATETIME
            )
        """,
        "order_items": """
            CREATE TABLE order_items (
                id AUTOINCREMENT PRIMARY KEY,
                order_id LONG,
                product_id LONG,
                quantity LONG,
                price DOUBLE
            )
        """,
        "users": """
            CREATE TABLE users (
                id AUTOINCREMENT PRIMARY KEY,
                username TEXT(100),
                password TEXT(255),
                email TEXT(255),
                created_at DATETIME
            )
        """
    }

    for name, ddl in TABLES.items():
        safe_create(cur, ddl, name)

    conn.commit()
    cur.close()
    conn.close()
