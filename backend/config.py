from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    DB_PATH = os.getenv("DB_PATH", r"C:\test\sample_db.mdb")
    PORT = int(os.getenv("PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
