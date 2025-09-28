"""
DAO for authentication-related DB operations.

Tables used:
- auth_users(id COUNTER PK, username TEXT, password_hash TEXT, email TEXT)
- token_blocklist(jti TEXT PK, token_type TEXT, user_id INTEGER, created_at TEXT)
"""
from .connection import get_conn
from datetime import datetime

def create_user(username: str, password_hash: str, email: str = None) -> int:
    """
    Insert a new user in auth_users.

    Returns:
        int: new user id
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO auth_users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email))
    cur.execute("SELECT @@IDENTITY")
    new_id = int(cur.fetchone()[0])
    conn.commit()
    cur.close()
    conn.close()
    return new_id

def get_user_by_username(username: str):
    """
    Retrieve user record by username.

    Returns:
        dict or None
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, email FROM auth_users WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close(); return None
    cols = [c[0] for c in cur.description]
    res = dict(zip(cols, row))
    cur.close(); conn.close()
    return res

def get_user_by_id(user_id: int):
    """
    Retrieve user record by ID.

    Returns:
        dict or None
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, email FROM auth_users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close(); return None
    cols = [c[0] for c in cur.description]
    res = dict(zip(cols, row))
    cur.close(); conn.close()
    return res


def add_token_to_blocklist(jti: str, token_type: str, user_id: int = None):
    """
    Add a token JTI to token_blocklist (revoke).
    """
    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    try:
        cur.execute("INSERT INTO token_blocklist (jti, token_type, user_id, created_at) VALUES (?, ?, ?, ?)",
                    (jti, token_type, user_id, created_at))
        conn.commit()
    except Exception:
        # ignore duplicate or errors
        pass
    finally:
        cur.close(); conn.close()

def is_token_revoked(jti: str) -> bool:
    """
    Return True if JTI present in blocklist.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM token_blocklist WHERE jti = ?", (jti,))
    count = int(cur.fetchone()[0])
    cur.close(); conn.close()
    return count > 0
