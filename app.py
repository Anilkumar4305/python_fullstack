from flask import Flask, render_template, request, jsonify
import sqlite3
from database import init_db, DB_NAME

app = Flask(__name__)
init_db()  # Initialize database

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------- FRONTEND ROUTES -----------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organizations')
def organizations_page():
    return render_template('organizations.html')

@app.route('/users')
def users_page():
    return render_template('users.html')

# ----------------- REST API ROUTES -----------------
# Organizations CRUD
@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    conn = get_db_connection()
    orgs = conn.execute('SELECT * FROM organizations').fetchall()
    conn.close()
    return jsonify([dict(org) for org in orgs])

@app.route('/api/organizations', methods=['POST'])
def add_organization():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO organizations (name, address) VALUES (?, ?)', (data['name'], data.get('address')))
    conn.commit()
    org_id = cur.lastrowid
    conn.close()
    return jsonify({"id": org_id, "name": data['name'], "address": data.get('address')}), 201

@app.route('/api/organizations/<int:id>', methods=['PUT'])
def update_organization(id):
    data = request.json
    conn = get_db_connection()
    conn.execute('UPDATE organizations SET name = ?, address = ? WHERE id = ?', (data.get('name'), data.get('address'), id))
    conn.commit()
    conn.close()
    return jsonify({"id": id, "name": data.get('name'), "address": data.get('address')})

@app.route('/api/organizations/<int:id>', methods=['DELETE'])
def delete_organization(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM organizations WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted successfully"})

# Users CRUD
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, email, organization_id) VALUES (?, ?, ?)',
                (data['name'], data['email'], data['organization_id']))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return jsonify({"id": user_id, "name": data['name'], "email": data['email'], "organization_id": data['organization_id']}), 201

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    conn = get_db_connection()
    conn.execute('UPDATE users SET name = ?, email = ?, organization_id = ? WHERE id = ?',
                 (data.get('name'), data.get('email'), data.get('organization_id'), id))
    conn.commit()
    conn.close()
    return jsonify({"id": id, "name": data.get('name'), "email": data.get('email'), "organization_id": data.get('organization_id')})

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)