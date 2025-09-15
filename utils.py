import datetime
import json
import sqlite3
import hashlib

# Mixed utility functions
def format_date(date_str):
    # Poor date handling
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        return datetime.datetime.now()

def hash_password(password):
    # Weak hashing
    return hashlib.md5(password.encode()).hexdigest()

def validate_email(email):
    # Poor email validation
    return "@" in email

def get_task_count():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def backup_data():
    # Another backup function (duplicate of main.py)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    
    with open("backup.json", "w") as f:
        json.dump(data, f)
    
    conn.close()

def log_action(action):
    # Poor logging
    with open("debug.log", "a") as f:
        f.write(f"{datetime.datetime.now()}: {action}\n")

# Random helper functions
def calculate_priority_score(priority):
    scores = {"low": 1, "medium": 2, "high": 3}
    return scores.get(priority, 1)

def clean_text(text):
    # Basic text cleaning
    return text.strip().replace("\n", " ")