import sqlite3

DB_NAME = 'orguser.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Organizations table
    c.execute('''
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT
        )
    ''')
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            organization_id INTEGER NOT NULL,
            FOREIGN KEY(organization_id) REFERENCES organizations(id)
        )
    ''')
    conn.commit()
    conn.close()