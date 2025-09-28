from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

class Config:
    DB_PATH = os.getenv("DB_PATH", r"C:\test\sample_user.accdb")
    PORT = int(os.getenv("PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_this_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
