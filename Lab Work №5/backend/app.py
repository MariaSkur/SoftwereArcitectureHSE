import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)  # разрешаем запросы с фронтенда

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'eventdb'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres')
    )
    return conn

@app.route('/api/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM events ORDER BY id;')
    events = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    name = data['name']
    date = data['date']
    location = data['location']
    description = data.get('description', '')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        'INSERT INTO events (name, date, location, description) VALUES (%s, %s, %s, %s) RETURNING *;',
        (name, date, location, description)
    )
    new_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_event), 201

@app.route('/api/events/<int:id>', methods=['GET'])
def get_event(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM events WHERE id = %s;', (id,))
    event = cur.fetchone()
    cur.close()
    conn.close()
    if event:
        return jsonify(event)
    return jsonify({'error': 'Event not found'}), 404

@app.route('/api/events/<int:id>', methods=['PUT'])
def update_event(id):
    data = request.get_json()
    name = data['name']
    date = data['date']
    location = data['location']
    description = data.get('description', '')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        'UPDATE events SET name = %s, date = %s, location = %s, description = %s WHERE id = %s RETURNING *;',
        (name, date, location, description, id)
    )
    updated_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_event:
        return jsonify(updated_event)
    return jsonify({'error': 'Event not found'}), 404

@app.route('/api/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM events WHERE id = %s;', (id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if deleted:
        return '', 204
    return jsonify({'error': 'Event not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
