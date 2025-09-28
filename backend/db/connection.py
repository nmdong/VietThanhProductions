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
