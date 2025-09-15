# main_master.py - TaskMaster Master Branch Version
"""
Master 分支版本 - 增加分類和截止日期功能
與 main.py 的主要差異：
1. 新增 category 和 due_date 欄位
2. 中文優先級選項
3. 不同的 API 回應格式
"""

import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3
import datetime
import json
from flask import Flask,request,jsonify
import threading
import requests
import os

# 全域變數 (與 main.py 相同的問題設計)
db_connection = None
app = Flask(__name__)
window = None
current_user = "admin"
DEBUG_MODE = True
API_KEY = "sk-master-branch-key"

# Master 分支特有設定
DEFAULT_CATEGORY = "一般"
DATE_FORMAT = "%Y年%m月%d日"
PRIORITY_OPTIONS = ["低", "中", "高", "緊急"]  # 中文優先級
CATEGORIES = ["工作", "個人", "學習", "購物", "一般"]

def connect_db():
    global db_connection
    try:
        db_connection = sqlite3.connect('tasks_master.db')  # 不同的資料庫檔案
        # Master 分支的資料表結構
        db_connection.execute('''CREATE TABLE IF NOT EXISTS tasks 
                                (id INTEGER PRIMARY KEY, 
                                 title TEXT NOT NULL, 
                                 description TEXT, 
                                 priority TEXT DEFAULT '中', 
                                 status TEXT DEFAULT '待辦', 
                                 created_at TEXT,
                                 category TEXT DEFAULT '一般',
                                 due_date TEXT,
                                 completed_date TEXT)''')
        db_connection.commit()
    except Exception as e:
        print(f"資料庫錯誤: {e}")

# 中文優先級轉換函數
def convert_priority_to_english(chinese_priority):
    """將中文優先級轉換為英文（為了相容性）"""
    mapping = {"低": "low", "中": "medium", "高": "high", "緊急": "urgent"}
    return mapping.get(chinese_priority, "medium")

def convert_priority_to_chinese(english_priority):
    """將英文優先級轉換為中文"""
    mapping = {"low": "低", "medium": "中", "high": "高", "urgent": "緊急"}
    return mapping.get(english_priority, "中")

class Task:
    def __init__(self, title, desc, priority="中", category="一般", due_date=None):
        self.title = title
        self.desc = desc
        self.priority = priority  # 中文優先級
        self.category = category
        self.due_date = due_date
        self.status = "待辦"
        self.created_at = datetime.datetime.now().strftime(DATE_FORMAT)

def add_task_master(title, description, priority="中", category="一般", due_date=None):
    """Master 分支的新增任務函數"""
    global db_connection
    try:
        current_time = datetime.datetime.now().strftime(DATE_FORMAT)
        db_connection.execute(
            "INSERT INTO tasks (title,description,priority,status,created_at,category,due_date) VALUES (?,?,?,?,?,?,?)",
            (title, description, priority, "待辦", current_time, category, due_date)
        )
        db_connection.commit()
        return True
    except Exception as e:
        print(f"新增任務錯誤: {e}")
        return False

def get_tasks_master():
    """Master 分支的取得任務函數"""
    global db_connection
    cursor = db_connection.execute("SELECT id,title,description,priority,status,created_at,category,due_date,completed_date FROM tasks")
    return cursor.fetchall()

def get_today_tasks():
    """取得今日到期的任務"""
    global db_connection
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor = db_connection.execute("SELECT * FROM tasks WHERE due_date = ? AND status != '已完成'", (today,))
    return cursor.fetchall()

# Flask API (Master 分支格式)
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks_master():
    tasks = get_tasks_master()
    # Master 分支的 API 回應格式
    result = []
    for task in tasks:
        result.append({
            "task_id": task[0],
            "task_title": task[1], 
            "task_description": task[2],
            "importance": task[3],  # 不同的欄位名
            "current_state": task[4],  # 不同的欄位名
            "created_time": task[5],
            "category": task[6],
            "deadline": task[7],
            "finished_date": task[8]
        })
    return jsonify({"tasks": result, "total": len(result)})

@app.route('/api/tasks', methods=['POST'])
def api_create_task_master():
    data = request.json
    title = data.get('title', '')
    desc = data.get('description', '')
    priority = data.get('priority', '中')
    category = data.get('category', '一般')
    due_date = data.get('due_date', None)
    
    if add_task_master(title, desc, priority, category, due_date):
        return jsonify({"status": "success", "message": "任務建立成功"})
    else:
        return jsonify({"status": "error", "message": "任務建立失敗"}), 500

@app.route('/api/tasks/today', methods=['GET'])
def api_get_today_tasks():
    """Master 分支新增的今日任務 API"""
    tasks = get_today_tasks()
    return jsonify({"today_tasks": tasks, "count": len(tasks)})

def run_flask_master():
    app.run(debug=True, port=5001, host='0.0.0.0')  # 不同的 port

# GUI 類別 (Master 版本)
class TaskGUIMaster:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("任務管理系統 v1.2")  # 中文標題
        self.window.geometry("900x700")  # 更大的視窗
        
        self.setup_widgets()
        
    def setup_widgets(self):
        # 標題
        title_label = tk.Label(self.window, text="任務管理系統", font=("Arial", 16))
        title_label.pack(pady=10)
        
        # 輸入區域
        input_frame = tk.Frame(self.window)
        input_frame.pack(pady=10)
        
        # 任務標題
        tk.Label(input_frame, text="任務標題:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)
        
        # 任務描述
        tk.Label(input_frame, text="任務描述:").grid(row=1, column=0, sticky="w")
        self.desc_entry = tk.Text(input_frame, width=30, height=3)
        self.desc_entry.grid(row=1, column=1, padx=5)
        
        # 優先級選擇 (中文)
        tk.Label(input_frame, text="優先級:").grid(row=2, column=0, sticky="w")
        self.priority_var = tk.StringVar(value="中")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, 
                                    values=PRIORITY_OPTIONS, state="readonly")
        priority_combo.grid(row=2, column=1, padx=5, sticky="w")
        
        # 分類選擇 (新增功能)
        tk.Label(input_frame, text="分類:").grid(row=3, column=0, sticky="w")
        self.category_var = tk.StringVar(value="一般")
        category_combo = ttk.Combobox(input_frame, textvariable=self.category_var,
                                    values=CATEGORIES, state="readonly")
        category_combo.grid(row=3, column=1, padx=5, sticky="w")
        
        # 截止日期 (新增功能)
        tk.Label(input_frame, text="截止日期:").grid(row=4, column=0, sticky="w")
        self.due_date_entry = tk.Entry(input_frame, width=15)
        self.due_date_entry.grid(row=4, column=1, padx=5, sticky="w")
        tk.Label(input_frame, text="(格式: YYYY-MM-DD)", font=("Arial", 8)).grid(row=4, column=2)
        
        # 按鈕區域
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="新增任務", command=self.add_task_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="標記完成", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="刪除任務", command=self.delete_task_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="今日任務", command=self.show_today_tasks).pack(side=tk.LEFT, padx=5)  # 新功能
        
        # 任務列表
        self.task_listbox = tk.Listbox(self.window, width=100, height=20)
        self.task_listbox.pack(pady=10)
        
        self.refresh_tasks()
    
    def add_task_gui(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get("1.0", tk.END).strip()
        priority = self.priority_var.get()
        category = self.category_var.get()
        due_date = self.due_date_entry.get() if self.due_date_entry.get() else None
        
        if add_task_master(title, desc, priority, category, due_date):
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete("1.0", tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.refresh_tasks()
            messagebox.showinfo("成功", "任務新增成功！")
        else:
            messagebox.showerror("錯誤", "任務新增失敗")
    
    def show_today_tasks(self):
        """顯示今日任務 (新功能)"""
        today_tasks = get_today_tasks()
        if today_tasks:
            task_list = "\n".join([f"• {task[1]} ({task[6]})" for task in today_tasks])
            messagebox.showinfo("今日任務", f"今天到期的任務:\n\n{task_list}")
        else:
            messagebox.showinfo("今日任務", "今天沒有到期的任務！")
    
    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = get_tasks_master()
        for task in tasks:
            # Master 分支的顯示格式
            due_info = f" (截止: {task[7]})" if task[7] else ""
            task_text = f"[{task[6]}] {task[1]} - {task[3]}{due_info}"
            self.task_listbox.insert(tk.END, task_text)
    
    def complete_task(self):
        # 簡化的完成功能
        messagebox.showinfo("功能", "完成功能尚未實作")
    
    def delete_task_gui(self):
        # 簡化的刪除功能
        messagebox.showinfo("功能", "刪除功能尚未實作")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    connect_db()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "gui":
            gui = TaskGUIMaster()
            gui.run()
        elif sys.argv[1] == "api":
            run_flask_master()
        elif sys.argv[1] == "backup":
            print("Master 分支備份功能")
    else:
        print("使用方法: python main_master.py [gui|api|backup]")