"""
Run the app in production mode using Waitress WSGI server.
"""
from waitress import serve
from app import app
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve(app, host="0.0.0.0", port=5000)
