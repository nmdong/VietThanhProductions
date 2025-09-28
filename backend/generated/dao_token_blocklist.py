import pyodbc
from .connection import get_conn

# DAO for token_blocklist

def fetch_all_token_blocklist():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM [token_blocklist]')
    cols = [c[0] for c in cur.description]
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    cur.close(); conn.close()
    return rows

def fetch_token_blocklist_by_id(record_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM [token_blocklist] WHERE id = ?', record_id)
    row = cur.fetchone()
    if row:
        cols = [c[0] for c in cur.description]
        result = dict(zip(cols, row))
    else:
        result = None
    cur.close(); conn.close()
    return result

def create_token_blocklist(**kwargs):
    conn = get_conn()
    cur = conn.cursor()
    cols = ', '.join([f'[{k}]' for k in kwargs.keys()])
    placeholders = ', '.join(['?'] * len(kwargs))
    sql = f'INSERT INTO [token_blocklist] ({cols}) VALUES ({placeholders})'
    cur.execute(sql, tuple(kwargs.values()))
    cur.execute('SELECT @@IDENTITY')
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close(); conn.close()
    return new_id

def update_token_blocklist(record_id, **kwargs):
    conn = get_conn()
    cur = conn.cursor()
    updates = ', '.join([f'[{k}] = ?' for k in kwargs.keys()])
    sql = f'UPDATE [token_blocklist] SET {updates} WHERE id = ?'
    params = list(kwargs.values()) + [record_id]
    cur.execute(sql, params)
    conn.commit()
    affected = cur.rowcount
    cur.close(); conn.close()
    return affected

def delete_token_blocklist(record_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM [token_blocklist] WHERE id = ?', record_id)
    affected = cur.rowcount
    conn.commit()
    cur.close(); conn.close()
    return affected