from .connection import get_conn

def fetch_all_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, age FROM users")
    cols = [c[0] for c in cur.description]
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return rows

def fetch_user_by_id(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, age FROM users WHERE id = ?", user_id)
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close(); return None
    cols = [c[0] for c in cur.description]
    result = dict(zip(cols, row))
    cur.close(); conn.close()
    return result

def create_user(name, email, age):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", (name, email, age))
    # lấy id vừa tạo
    cur.execute("SELECT @@IDENTITY")
    lastid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return int(lastid)

def update_user(user_id, name=None, email=None, age=None):
    conn = get_conn()
    cur = conn.cursor()
    updates, params = [], []
    if name is not None:
        updates.append("name = ?"); params.append(name)
    if email is not None:
        updates.append("email = ?"); params.append(email)
    if age is not None:
        updates.append("age = ?"); params.append(age)
    if not updates:
        cur.close(); conn.close(); return 0
    params.append(user_id)
    sql = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    cur.execute(sql, params)
    affected = cur.rowcount
    conn.commit()
    cur.close(); conn.close()
    return affected

def delete_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", user_id)
    affected = cur.rowcount
    conn.commit()
    cur.close(); conn.close()
    return affected
