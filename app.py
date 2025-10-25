import os
from flask import Flask, render_template, request, jsonify
import sqlite3

from database import init_db, DB_NAME

app = Flask(__name__)
init_db()  # Initialize the SQLite database

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- Your routes go here (index, users, organizations, API routes) -----------------

if __name__ == "__main__":
    # Use 0.0.0.0 to make the app accessible externally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)