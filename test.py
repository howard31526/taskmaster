import unittest
from main import Task, add_task, get_tasks
import sqlite3
import os

class TestTaskManager(unittest.TestCase):
    
    def setUp(self):
        # Create test database
        self.test_db = "test_tasks.db"
        conn = sqlite3.connect(self.test_db)
        conn.execute('''CREATE TABLE tasks 
                       (id INTEGER PRIMARY KEY, title TEXT, description TEXT, 
                        priority TEXT, status TEXT, created_at TEXT)''')
        conn.close()
    
    def tearDown(self):
        # Cleanup
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_task_creation(self):
        task = Task("Test Task", "Test Description")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, "pending")
    
    def test_add_task(self):
        # This test doesn't actually work because of global db_connection
        result = add_task("New Task", "Description", "high")
        # Can't verify because of poor architecture
    
    # Missing tests for:
    # - API endpoints
    # - Error conditions  
    # - Database operations
    # - GUI interactions
    
if __name__ == '__main__':
    unittest.main()