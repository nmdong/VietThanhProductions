import os
import pyodbc
import win32com.client
from config import Config

def create_mdb(path):
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn_str = f"Provider=Microsoft.Jet.OLEDB.4.0;Data Source={path};"
    cat = win32com.client.Dispatch("ADOX.Catalog")
    cat.Create(conn_str)
    print("Created MDB:", path)

def create_users_table(db_path):
    conn_str = f"Driver={{Microsoft Access Driver (*.mdb)}};DBQ={db_path};"
    conn = pyodbc.connect(conn_str, autocommit=True)
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE users (id COUNTER PRIMARY KEY, name TEXT(100), email TEXT(100), age INTEGER)")
        print("Created table users")
    except Exception as e:
        print("Create table failed (maybe exists):", e)
    finally:
        cur.close(); conn.close()

if __name__ == "__main__":
    p = Config.DB_PATH
    if not os.path.exists(p):
        create_mdb(p)
    create_users_table(p)
