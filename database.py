import sqlite3
import os

DATABASE_PATH = "tasks.db"  # Hardcoded path

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
        
    def connect(self):
        try:
            self.connection = sqlite3.connect(DATABASE_PATH)
            self.create_tables()
        except Exception as e:
            print(f"Database connection failed: {e}")
    
    def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'low',
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.connection.execute(query)
        self.connection.commit()
    
    def close(self):
        if self.connection:
            self.connection.close()

# Global instance (bad practice)
db_manager = DatabaseManager()