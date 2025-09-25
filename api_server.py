"""
TaskMaster Web 應用模組
提供 Web 介面和 API 用於任務管理
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'taskmaster_secret_key'

def get_db():
    """取得資料庫連線"""
    return sqlite3.connect('tasks.db')

def init_db():
    """初始化資料庫"""
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY, title TEXT, description TEXT,
                     priority TEXT, status TEXT, created_at TEXT)''')
    conn.commit()
    conn.close()

def get_task_stats():
    """取得任務統計資料"""
    conn = get_db()
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    pending = cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'").fetchone()[0]
    in_progress = cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='in_progress'").fetchone()[0]
    completed = cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='completed'").fetchone()[0]

    conn.close()
    return {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed
    }

@app.route('/')
def index():
    """主頁面"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    conn.close()

    stats = get_task_stats()
    return render_template('index.html', tasks=tasks, stats=stats)

@app.route('/tasks', methods=['POST'])
def create_task():
    """建立新任務"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority = request.form.get('priority', 'low')

    if not title:
        flash('任務標題不能為空', 'error')
        return redirect(url_for('index'))

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title, description, priority, status, created_at) VALUES (?, ?, ?, ?, ?)",
        (title, description, priority, 'pending', str(datetime.datetime.now()))
    )
    conn.commit()
    conn.close()

    flash('任務建立成功', 'success')
    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """更新任務狀態"""
    status = request.form.get('status')

    if status not in ['pending', 'in_progress', 'completed']:
        flash('無效的狀態', 'error')
        return redirect(url_for('index'))

    conn = get_db()
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

    flash('任務狀態更新成功', 'success')
    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """刪除任務"""
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    flash('任務刪除成功', 'success')
    return redirect(url_for('index'))

# API 端點（為前端 AJAX 使用）
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """API: 取得所有任務"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    conn.close()

    task_list = []
    for task in tasks:
        task_list.append({
            'id': task[0],
            'title': task[1],
            'description': task[2],
            'priority': task[3],
            'status': task[4],
            'created_at': task[5]
        })

    return jsonify({'tasks': task_list})

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    """API: 取得統計資料"""
    stats = get_task_stats()
    return jsonify(stats)

def run_web_server():
    """啟動 Web 伺服器"""
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == "__main__":
    run_web_server()