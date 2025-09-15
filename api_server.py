from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)
app.config['DEBUG'] = True  # Debug mode in production code!

# Another database connection method
def get_db():
    return sqlite3.connect('tasks.db')

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    db = get_db()
    cursor = db.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    db.close()
    
    # Inconsistent response format from main.py
    result = []
    for task in tasks:
        result.append({
            'id': task[0],
            'title': task[1],
            'description': task[2],
            'priority': task[3],
            'status': task[4],
            'created_at': task[5]
        })
    
    return jsonify({'tasks': result})

@app.route('/tasks', methods=['POST'])
def create_new_task():
    # No content-type validation
    data = request.get_json()
    
    db = get_db()
    db.execute('INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)',
               (data['title'], data.get('description', ''), data.get('priority', 'medium')))
    db.commit()
    db.close()
    
    return jsonify({'status': 'created'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Different port than main.py