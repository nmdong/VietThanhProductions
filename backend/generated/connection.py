import pyodbc

DB_PATH = r"C:\test\sample_user.accdb"
CONN_STR = r"Driver={Microsoft Access Driver (*.accdb)};DBQ=" + DB_PATH

def get_conn():
    return pyodbc.connect(CONN_STR)
