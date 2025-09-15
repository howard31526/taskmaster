# TaskMaster - All in one file (BAD PRACTICE!)
import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3
import datetime
import json
from flask import Flask,request,jsonify
import threading
import requests
import os

# Global variables everywhere (BAD!)
db_connection = None
app = Flask(__name__)
window = None
current_user = "admin"
DEBUG_MODE = True
API_KEY = "sk-1234567890abcdef"  # Hardcoded API key (VERY BAD!)

def connect_db():
    global db_connection
    try:
        db_connection = sqlite3.connect('tasks.db')
        db_connection.execute('''CREATE TABLE IF NOT EXISTS tasks 
                                (id INTEGER PRIMARY KEY, title TEXT, description TEXT, 
                                priority TEXT, status TEXT, created_at TEXT)''')
        db_connection.commit()
    except:
        print("Database error!")  # Poor error handling

class Task:
    def __init__(self,title,desc,priority="low"):  # Inconsistent naming
        self.title=title  # No spaces around operators
        self.desc= desc   # Inconsistent spacing
        self.priority =priority
        self.status="pending"
        self.created_at=str(datetime.datetime.now())  # String instead of datetime

def add_task(title,description,priority="low"):
    global db_connection
    # No input validation!
    query="INSERT INTO tasks (title,description,priority,status,created_at) VALUES (?,?,?,?,?)"
    try:
        db_connection.execute(query,(title,description,priority,"pending",str(datetime.datetime.now())))
        db_connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")  # Poor error handling
        return False

def get_tasks():
    global db_connection
    cursor=db_connection.execute("SELECT * FROM tasks")  # No error handling
    return cursor.fetchall()

def update_task(task_id,status):
    global db_connection
    query=f"UPDATE tasks SET status='{status}' WHERE id={task_id}"  # SQL injection risk!
    db_connection.execute(query)
    db_connection.commit()

def delete_task(id):
    global db_connection
    query=f"DELETE FROM tasks WHERE id={id}"  # More SQL injection!
    db_connection.execute(query)
    db_connection.commit()

# GUI Code mixed with business logic
class TaskGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TaskMaster")
        self.window.geometry("800x600")
        
        # Create widgets without proper organization
        self.task_listbox = tk.Listbox(self.window, width=80, height=20)
        self.task_listbox.pack(pady=10)
        
        self.title_entry = tk.Entry(self.window, width=50)
        self.title_entry.pack()
        
        self.desc_entry = tk.Text(self.window, width=50, height=5)
        self.desc_entry.pack()
        
        self.add_button = tk.Button(self.window, text="Add Task", command=self.add_task_gui)
        self.add_button.pack()
        
        self.complete_button = tk.Button(self.window, text="Mark Complete", command=self.complete_task)
        self.complete_button.pack()
        
        self.delete_button = tk.Button(self.window, text="Delete", command=self.delete_task_gui)
        self.delete_button.pack()
        
        self.refresh_tasks()
    
    def add_task_gui(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get("1.0", tk.END).strip()
        
        if add_task(title, desc):
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete("1.0", tk.END)
            self.refresh_tasks()
        else:
            messagebox.showerror("Error", "Failed to add task")
    
    def complete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            task_id = self.get_task_id_from_selection(selection[0])
            update_task(task_id, "completed")
            self.refresh_tasks()
    
    def delete_task_gui(self):
        selection = self.task_listbox.curselection()
        if selection:
            task_id = self.get_task_id_from_selection(selection[0])
            delete_task(task_id)
            self.refresh_tasks()
    
    def get_task_id_from_selection(self, index):
        # Fragile way to get task ID
        task_text = self.task_listbox.get(index)
        return int(task_text.split(" - ")[0])
    
    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = get_tasks()
        for task in tasks:
            task_text = f"{task[0]} - {task[1]} ({task[3]})"
            self.task_listbox.insert(tk.END, task_text)
    
    def run(self):
        self.window.mainloop()

# Flask API mixed in the same file
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    tasks = get_tasks()
    # Poor JSON response structure
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    data = request.json  # No validation if json exists
    title = data['title']  # KeyError risk
    desc = data.get('description', '')
    priority = data.get('priority', 'low')
    
    if add_task(title, desc, priority):
        return "OK"  # Non-standard response
    else:
        return "ERROR", 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    delete_task(task_id)
    return "DELETED"  # Poor response

def run_flask():
    app.run(debug=False, port=5000, host='0.0.0.0')  # Security risk!

def backup_database():
    # Poorly implemented backup
    import shutil
    try:
        shutil.copy('tasks.db', 'backup_tasks.db')
        print("Backup created")
    except:
        print("Backup failed")

if __name__ == "__main__":
    connect_db()
    
    # Decide what to run based on command line args (poorly done)
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "gui":
            gui = TaskGUI()
            gui.run()
        elif sys.argv[1] == "api":
            run_flask()
        elif sys.argv[1] == "backup":
            backup_database()
    else:
        print("Usage: python main.py [gui|api|backup]")