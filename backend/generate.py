# cript Python auto-generate Schema + DAO từ file Access.
# Bạn chỉ cần đưa vào file .mdb hoặc .accdb, script sẽ đọc schema (tên bảng + cột) và
# sinh ra code Python (2 phần: Schema dùng Marshmallow và DAO với CRUD).

# generate.py
# Auto-generate Marshmallow Schema + DAO từ file Access (.accdb)
# Yêu cầu: Python 64-bit + Microsoft Access Database Engine 64-bit + pyodbc

import pyodbc
import os
from config import Config

# ====== Config ======
DB_PATH = r"C:\test\sample_user.accdb"   # đường dẫn file .accdb
OUTPUT_DIR = "generated"
driver = "Microsoft Access Driver (*.mdb, *.accdb)" if Config.DB_PATH.lower().endswith(".accdb") else "Microsoft Access Driver (*.mdb)"

# Kết nối Access 2007+ (.accdb)
CONN_STR = rf"Driver={{{driver}}};DBQ={Config.DB_PATH};"

# ====== Type mapping (ODBC SQL types -> Marshmallow fields) ======
SQL_TYPE_MAP = {
    -6: "fields.Int",    # SQL_TINYINT
    -5: "fields.Int",    # SQL_BIGINT
    4:  "fields.Int",    # SQL_INTEGER
    5:  "fields.Int",    # SQL_SMALLINT
    2:  "fields.Float",  # SQL_NUMERIC
    3:  "fields.Float",  # SQL_DECIMAL
    7:  "fields.Float",  # SQL_REAL
    8:  "fields.Float",  # SQL_DOUBLE
    12: "fields.Str",    # SQL_VARCHAR
    -1: "fields.Str",    # SQL_LONGVARCHAR (Memo)
    -4: "fields.Str",    # SQL_LONGVARBINARY
    16: "fields.Bool",   # SQL_BOOLEAN
}

# ====== DB helpers ======
def get_connection():
    return pyodbc.connect(CONN_STR)

def list_tables():
    conn = get_connection()
    cursor = conn.cursor()
    tables = [row.table_name for row in cursor.tables(tableType="TABLE")]
    conn.close()
    return tables

def list_columns(table):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM [{table}] WHERE 1=0")
    cols = [(c[0], SQL_TYPE_MAP.get(c[1], "fields.Str")) for c in cursor.description]
    conn.close()
    return cols

# ====== Code generators ======
def generate_schema(table, columns):
    class_name = table.capitalize() + "Schema"
    lines = [
        "from marshmallow import Schema, fields",
        "",
        f"class {class_name}(Schema):"
    ]
    for col, field_type in columns:
        if col.lower() == "id":
            lines.append(f"    {col.lower()} = {field_type}(dump_only=True)")
        else:
            lines.append(f"    {col.lower()} = {field_type}(required=True)")
    return "\n".join(lines)

def generate_dao(table, columns):
    lines = [
        "import pyodbc",
        "from .connection import get_conn",
        "",
        f"# DAO for {table}",
        "",
        f"def fetch_all_{table.lower()}():",
        "    conn = get_conn()",
        "    cur = conn.cursor()",
        f"    cur.execute('SELECT * FROM [{table}]')",
        "    cols = [c[0] for c in cur.description]",
        "    rows = [dict(zip(cols, row)) for row in cur.fetchall()]",
        "    cur.close(); conn.close()",
        "    return rows",
        "",
        f"def fetch_{table.lower()}_by_id(record_id):",
        "    conn = get_conn()",
        "    cur = conn.cursor()",
        f"    cur.execute('SELECT * FROM [{table}] WHERE id = ?', record_id)",
        "    row = cur.fetchone()",
        "    if row:",
        "        cols = [c[0] for c in cur.description]",
        "        result = dict(zip(cols, row))",
        "    else:",
        "        result = None",
        "    cur.close(); conn.close()",
        "    return result",
        "",
        f"def create_{table.lower()}(**kwargs):",
        "    conn = get_conn()",
        "    cur = conn.cursor()",
        "    cols = ', '.join([f'[{k}]' for k in kwargs.keys()])",
        "    placeholders = ', '.join(['?'] * len(kwargs))",
        f"    sql = f'INSERT INTO [{table}] ({{cols}}) VALUES ({{placeholders}})'",
        "    cur.execute(sql, tuple(kwargs.values()))",
        "    cur.execute('SELECT @@IDENTITY')",
        "    new_id = cur.fetchone()[0]",
        "    conn.commit()",
        "    cur.close(); conn.close()",
        "    return new_id",
        "",
        f"def update_{table.lower()}(record_id, **kwargs):",
        "    conn = get_conn()",
        "    cur = conn.cursor()",
        "    updates = ', '.join([f'[{k}] = ?' for k in kwargs.keys()])",
        f"    sql = f'UPDATE [{table}] SET {{updates}} WHERE id = ?'",
        "    params = list(kwargs.values()) + [record_id]",
        "    cur.execute(sql, params)",
        "    conn.commit()",
        "    affected = cur.rowcount",
        "    cur.close(); conn.close()",
        "    return affected",
        "",
        f"def delete_{table.lower()}(record_id):",
        "    conn = get_conn()",
        "    cur = conn.cursor()",
        f"    cur.execute('DELETE FROM [{table}] WHERE id = ?', record_id)",
        "    affected = cur.rowcount",
        "    conn.commit()",
        "    cur.close(); conn.close()",
        "    return affected",
    ]
    return "\n".join(lines)

def generate_connection_file():
    return f'''import pyodbc

DB_PATH = r"{DB_PATH}"
CONN_STR = r"Driver={{Microsoft Access Driver (*.accdb)}};DBQ=" + DB_PATH

def get_conn():
    return pyodbc.connect(CONN_STR)
'''

# ====== Main ======
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # connection.py
    conn_file = os.path.join(OUTPUT_DIR, "connection.py")
    with open(conn_file, "w", encoding="utf-8") as f:
        f.write(generate_connection_file())
    print("✅ Generated connection.py")

    # schemas.py
    schema_file = os.path.join(OUTPUT_DIR, "schemas.py")
    with open(schema_file, "w", encoding="utf-8") as f:
        for table in list_tables():
            columns = list_columns(table)
            f.write(generate_schema(table, columns))
            f.write("\n\n")
    print("✅ Generated schemas.py")

    # DAO files
    for table in list_tables():
        columns = list_columns(table)
        dao_file = os.path.join(OUTPUT_DIR, f"dao_{table.lower()}.py")
        with open(dao_file, "w", encoding="utf-8") as f:
            f.write(generate_dao(table, columns))
        print(f"✅ Generated {dao_file}")

if __name__ == "__main__":
    main()
