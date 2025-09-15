# quick_fix.py - Emergency fixes for demo day
"""
URGENT FIXES FOR DEMO - DO NOT MERGE TO PRODUCTION
These are temporary workarounds that need proper solutions later
"""
import sqlite3
import datetime
from functools import wraps

# HACK: Quick fix for database threading issue
# TODO: Implement proper connection pooling
def quick_db_fix(func):
    """Temporary decorator to handle DB threading issues"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.ProgrammingError as e:
            if "thread" in str(e).lower():
                # Force new connection for each request
                print(f"WARNING: Threading issue detected, using fallback: {e}")
                return fallback_db_operation(*args, **kwargs)
            raise
    return wrapper

def fallback_db_operation(*args, **kwargs):
    """Emergency fallback for DB operations"""
    conn = sqlite3.connect('tasks.db', check_same_thread=False)
    try:
        cursor = conn.execute("SELECT * FROM tasks")
        result = cursor.fetchall()
        return result
    finally:
        conn.close()

# HACK: Quick authentication bypass for demo
def demo_auth_bypass():
    """DANGER: Bypasses authentication for demo purposes"""
    return {
        'user_id': 'demo_user',
        'username': 'admin', 
        'permissions': ['read', 'write', 'delete', 'admin'],
        'bypass_reason': 'DEMO_MODE_ACTIVE'
    }

# Quick fix for date formatting issues
def format_demo_date(date_str):
    """Temporary date formatter for demo"""
    if not date_str:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Handle multiple date formats that are causing issues
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%m/%d/%Y %H:%M',
    ]
    
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            continue
    
    # Fallback: return current time with warning
    print(f"WARNING: Could not parse date '{date_str}', using current time")
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

# Emergency task priority fix
PRIORITY_MAPPING = {
    # Old system used numbers, new system uses strings
    '1': 'high',
    '2': 'medium', 
    '3': 'low',
    'urgent': 'high',
    'normal': 'medium',
    'later': 'low'
}

def normalize_priority(priority):
    """Quick fix to normalize different priority formats"""
    if str(priority).lower() in PRIORITY_MAPPING:
        return PRIORITY_MAPPING[str(priority).lower()]
    return 'medium'  # Safe default

# DEMO ONLY: Mock email sending
def mock_email_service(to, subject, body):
    """Mock email for demo - logs instead of sending"""
    print(f"[DEMO EMAIL] To: {to}")
    print(f"[DEMO EMAIL] Subject: {subject}")
    print(f"[DEMO EMAIL] Body: {body[:100]}...")
    return True

if __name__ == "__main__":
    print("⚠️  DEMO QUICK FIXES LOADED")
    print("⚠️  DO NOT USE IN PRODUCTION")
    print("⚠️  REMEMBER TO REMOVE AFTER DEMO")