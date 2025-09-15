import datetime
import json
import sqlite3
import hashlib

# 混雜的工具函數
def format_date(date_str):
    # 日期處理不佳
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        return datetime.datetime.now()

def hash_password(password):
    # W弱加密
    return hashlib.md5(password.encode()).hexdigest()

def validate_email(email):
    # 信箱驗證很糟
    return "@" in email

def get_task_count():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def backup_data():
    # 另一個備份函數（與 main.py 重複）
    conn = sqlite3.connect("tasks.db")
    cursor = conn.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    
    with open("backup.json", "w") as f:
        json.dump(data, f)
    
    conn.close()

def log_action(action):
    # 日誌記錄不佳
    with open("debug.log", "a") as f:
        f.write(f"{datetime.datetime.now()}: {action}\n")

# 隨機的輔助函數
def calculate_priority_score(priority):
    scores = {"low": 1, "medium": 2, "high": 3}
    return scores.get(priority, 1)

def clean_text(text):
    # 文字清理過於單一
    return text.strip().replace("\n", " ")