import sqlite3
import datetime
from typing import List, Tuple, Optional

class Task:
    def __init__(self, title: str, description: str = "", priority: str = "low"):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = "pending"
        self.created_at = datetime.datetime.now()

class DatabaseManager:
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_database(self):
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        priority TEXT DEFAULT 'low',
                        status TEXT DEFAULT 'pending',
                        created_at TEXT
                    )
                """)
                conn.commit()
        except Exception as e:
            raise Exception(f"Database initialization failed: {e}")

    def add_task(self, title: str, description: str = "", priority: str = "low") -> bool:
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO tasks (title, description, priority, status, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (title, description, priority, "pending", str(datetime.datetime.now())))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding task: {e}")
            return False

    def get_tasks(self) -> List[Tuple]:
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return []

    def update_task_status(self, task_id: int, status: str) -> bool:
        try:
            with self.get_connection() as conn:
                conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating task: {e}")
            return False

    def delete_task(self, task_id: int) -> bool:
        try:
            with self.get_connection() as conn:
                conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False

    def get_task_by_id(self, task_id: int) -> Optional[Tuple]:
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching task: {e}")
            return None