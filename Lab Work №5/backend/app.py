import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'eventdb'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres')
    )
    return conn

# Получить все проекты
@app.route('/api/projects', methods=['GET'])
def get_projects():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM projects ORDER BY id;')
    projects = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(projects)

# Создать новый проект
@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    name = data['name']
    date = data['date']
    location = data['location']
    description = data.get('description', '')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        'INSERT INTO projects (name, date, location, description) VALUES (%s, %s, %s, %s) RETURNING *;',
        (name, date, location, description)
    )
    new_project = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_project), 201

# Получить проект по id
@app.route('/api/projects/<int:id>', methods=['GET'])
def get_project(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM projects WHERE id = %s;', (id,))
    project = cur.fetchone()
    cur.close()
    conn.close()
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

# Обновить проект
@app.route('/api/projects/<int:id>', methods=['PUT'])
def update_project(id):
    data = request.get_json()
    name = data['name']
    date = data['date']
    location = data['location']
    description = data.get('description', '')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        'UPDATE projects SET name = %s, date = %s, location = %s, description = %s WHERE id = %s RETURNING *;',
        (name, date, location, description, id)
    )
    updated_project = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_project:
        return jsonify(updated_project)
    return jsonify({'error': 'Project not found'}), 404

# Удалить проект
@app.route('/api/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM projects WHERE id = %s;', (id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if deleted:
        return '', 204
    return jsonify({'error': 'Project not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
