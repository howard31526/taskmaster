# Temporary file for testing - TODO: DELETE THIS
import sqlite3

def quick_test():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.execute("SELECT * FROM tasks LIMIT 5")
    for row in cursor:
        print(row)
    conn.close()

def debug_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.execute("PRAGMA table_info(tasks)")
    print("Table structure:")
    for row in cursor:
        print(row)
    conn.close()

if __name__ == "__main__":
    quick_test()
    debug_database()