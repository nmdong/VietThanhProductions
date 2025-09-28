"""
Create auth_users and token_blocklist tables in Access DB if not exists.
Run once on server to initialize auth tables.
"""
import pyodbc
from config import Config

def run():
    driver = "Microsoft Access Driver (*.mdb, *.accdb)" if Config.DB_PATH.lower().endswith(".accdb") else "Microsoft Access Driver (*.mdb)"
    conn_str = rf"Driver={{{driver}}};DBQ={Config.DB_PATH};"
    conn = pyodbc.connect(conn_str, autocommit=True)
    cur = conn.cursor()
    try:
        cur.execute("""
        CREATE TABLE auth_users (
            id COUNTER PRIMARY KEY,
            username TEXT(100),
            password_hash TEXT(255),
            email TEXT(100)
        )
        """)
        print("Created auth_users")
    except Exception as e:
        print("auth_users exists or error:", e)
    try:
        cur.execute("""
        CREATE TABLE token_blocklist (
            jti TEXT(255) PRIMARY KEY,
            token_type TEXT(20),
            user_id INTEGER,
            created_at TEXT
        )
        """)
        print("Created token_blocklist")
    except Exception as e:
        print("token_blocklist exists or error:", e)
    cur.close(); conn.close()

if __name__ == "__main__":
    run()
