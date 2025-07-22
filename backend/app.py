import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory, redirect, url_for
from flask_cors import CORS

# --- Basic Setup ---
APP_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(APP_PATH, '..')
DATABASE_PATH = os.path.join(APP_PATH, 'database.db')

app = Flask(__name__)
CORS(app)

# --- Database Connection ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Admin Login ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] == ADMIN_USERNAME and data['password'] == ADMIN_PASSWORD:
        return jsonify({'success': True})
    return jsonify({'success': False}), 401

# --- Moods API Routes ---
@app.route('/api/moods', methods=['GET'])
def get_moods():
    conn = get_db_connection()
    moods = conn.execute('SELECT * FROM moods').fetchall()
    conn.close()
    return jsonify([dict(row) for row in moods])

# ... (add, update, delete mood routes are unchanged) ...
@app.route('/api/moods', methods=['POST'])
def add_mood():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO moods (name, emoji) VALUES (?, ?)', (data['name'], data['emoji']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/moods/<int:id>', methods=['PUT'])
def update_mood(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE moods SET name = ?, emoji = ? WHERE id = ?', (data['name'], data['emoji'], id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/moods/<int:id>', methods=['DELETE'])
def delete_mood(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM moods WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# --- Foods API Routes ---
# (All food routes are unchanged)
@app.route("/api/suggestions")
def get_suggestions():
    mood_name = request.args.get("mood")
    conn = get_db_connection()
    foods = conn.execute('SELECT f.* FROM foods f JOIN moods m ON f.mood_id = m.id WHERE m.name = ?', (mood_name,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in foods])

@app.route('/api/foods', methods=['GET'])
def get_all_foods():
    conn = get_db_connection()
    foods = conn.execute('SELECT f.id, f.name, f.description, f.imageUrl, m.name as mood FROM foods f JOIN moods m ON f.mood_id = m.id').fetchall()
    conn.close()
    return jsonify([dict(row) for row in foods])

@app.route('/api/foods', methods=['POST'])
def add_food():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO foods (name, description, imageUrl, mood_id) VALUES (?, ?, ?, ?)', (data['name'], data['description'], data['imageUrl'], data['mood_id']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/foods/<int:id>', methods=['PUT'])
def update_food(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE foods SET name = ?, description = ?, imageUrl = ?, mood_id = ? WHERE id = ?', (data['name'], data['description'], data['imageUrl'], data['mood_id'], id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/foods/<int:id>', methods=['DELETE'])
def delete_food(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM foods WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# --- Frontend Serving ---
@app.route('/')
def serve_index():
    return send_from_directory(STATIC_FOLDER, 'index.html')

# ✨ NEW ROUTE to serve the app.html file
@app.route('/app')
def serve_app():
    return send_from_directory(STATIC_FOLDER, 'app.html')

@app.route('/admin')
def redirect_to_admin():
    return redirect(url_for('serve_static', path='admin.html'))

@app.route('/<path:path>')
def serve_static(path):
    # This will serve Logo.jpg, wallpaper.jpg, and admin.html
    return send_from_directory(STATIC_FOLDER, path)

if __name__ == "__main__":
    app.run(debug=True, port=5000)