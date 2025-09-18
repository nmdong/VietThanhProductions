import pyodbc
from config import Config

# Driver cho .mdb (Access 2003)
CONN_STR = (
    r"Driver={Microsoft Access Driver (*.mdb)};"
    f"DBQ={Config.DB_PATH};"
)

def get_conn():
    # mở mới mỗi lần gọi (simple)
    return pyodbc.connect(CONN_STR, autocommit=False)
