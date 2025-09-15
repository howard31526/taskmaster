# utils_master.py - Master 分支工具函數
import datetime
import json
import sqlite3

# Master 分支特有的日期格式
DATE_FORMAT_CHINESE = "%Y年%m月%d日"
DATE_FORMAT_ISO = "%Y-%m-%d"

def format_chinese_date(date_str):
    """格式化為中文日期"""
    if not date_str:
        return datetime.datetime.now().strftime(DATE_FORMAT_CHINESE)
    
    try:
        # 嘗試解析 ISO 格式
        dt = datetime.datetime.strptime(date_str, DATE_FORMAT_ISO)
        return dt.strftime(DATE_FORMAT_CHINESE)
    except ValueError:
        try:
            # 嘗試解析中文格式
            dt = datetime.datetime.strptime(date_str, DATE_FORMAT_CHINESE)
            return date_str  # 已經是中文格式
        except ValueError:
            return datetime.datetime.now().strftime(DATE_FORMAT_CHINESE)

def format_iso_date(date_str):
    """格式化為 ISO 日期"""
    if not date_str:
        return datetime.datetime.now().strftime(DATE_FORMAT_ISO)
    
    try:
        # 嘗試解析中文格式
        dt = datetime.datetime.strptime(date_str, DATE_FORMAT_CHINESE)
        return dt.strftime(DATE_FORMAT_ISO)
    except ValueError:
        try:
            # 嘗試解析 ISO 格式
            dt = datetime.datetime.strptime(date_str, DATE_FORMAT_ISO)
            return date_str  # 已經是 ISO 格式
        except ValueError:
            return datetime.datetime.now().strftime(DATE_FORMAT_ISO)

def validate_category(category):
    """驗證分類是否有效"""
    valid_categories = ["工作", "個人", "學習", "購物", "一般"]
    return category if category in valid_categories else "一般"

def validate_priority(priority):
    """驗證優先級是否有效"""
    valid_priorities = ["低", "中", "高", "緊急"]
    return priority if priority in valid_priorities else "中"

def convert_task_data_for_api(task_tuple):
    """將資料庫元組轉換為 API 格式"""
    return {
        "task_id": task_tuple[0],
        "task_title": task_tuple[1],
        "task_description": task_tuple[2],
        "importance": task_tuple[3],
        "current_state": task_tuple[4],
        "created_time": task_tuple[5],
        "category": task_tuple[6],
        "deadline": task_tuple[7],
        "finished_date": task_tuple[8]
    }

def get_task_statistics():
    """取得任務統計資訊"""
    conn = sqlite3.connect('tasks_master.db')
    
    # 按分類統計
    cursor = conn.execute("SELECT category, COUNT(*) FROM tasks GROUP BY category")
    category_stats = dict(cursor.fetchall())
    
    # 按優先級統計
    cursor = conn.execute("SELECT priority, COUNT(*) FROM tasks GROUP BY priority")
    priority_stats = dict(cursor.fetchall())
    
    # 按狀態統計
    cursor = conn.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    status_stats = dict(cursor.fetchall())
    
    conn.close()
    
    return {
        "by_category": category_stats,
        "by_priority": priority_stats,
        "by_status": status_stats
    }

def export_tasks_to_json():
    """匯出任務為 JSON 格式"""
    conn = sqlite3.connect('tasks_master.db')
    cursor = conn.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    
    task_list = []
    for task in tasks:
        task_dict = {
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "priority": task[3],
            "status": task[4],
            "created_at": task[5],
            "category": task[6],
            "due_date": task[7],
            "completed_date": task[8]
        }
        task_list.append(task_dict)
    
    return json.dumps(task_list, ensure_ascii=False, indent=2)

# Master 分支特有的功能
def get_overdue_tasks():
    """取得逾期任務"""
    conn = sqlite3.connect('tasks_master.db')
    today = datetime.datetime.now().strftime(DATE_FORMAT_ISO)
    cursor = conn.execute(
        "SELECT * FROM tasks WHERE due_date < ? AND status != '已完成'", 
        (today,)
    )
    overdue_tasks = cursor.fetchall()
    conn.close()
    return overdue_tasks

def get_upcoming_tasks(days=7):
    """取得即將到期的任務"""
    conn = sqlite3.connect('tasks_master.db')
    today = datetime.datetime.now()
    future_date = (today + datetime.timedelta(days=days)).strftime(DATE_FORMAT_ISO)
    today_str = today.strftime(DATE_FORMAT_ISO)
    
    cursor = conn.execute(
        "SELECT * FROM tasks WHERE due_date BETWEEN ? AND ? AND status != '已完成'",
        (today_str, future_date)
    )
    upcoming_tasks = cursor.fetchall()
    conn.close()
    return upcoming_tasks

if __name__ == "__main__":
    # 測試函數
    print("Master 分支工具函數測試")
    print(f"中文日期: {format_chinese_date('2024-09-15')}")
    print(f"ISO 日期: {format_iso_date('2024年9月15日')}")
    print(f"任務統計: {get_task_statistics()}")