---

## 📁 login.py - 半完成的登入功能

### 內容設計：
```python
# login.py - User Authentication System (Work In Progress)
"""
INCOMPLETE IMPLEMENTATION
Started: 2024-01-12
Status: 50% complete
Issues: Password hashing, session management, database integration

TODO:
- Implement proper password hashing
- Add session management
- Database schema for users
- Password reset functionality
- Email verification
"""

import hashlib
import sqlite3
import datetime
import secrets
from functools import wraps

class UserAuthentication:
    def __init__(self, db_path='tasks.db'):
        self.db_path = db_path
        self.init_user_table()
    
    def init_user_table(self):
        """Initialize user table - INCOMPLETE"""
        conn = sqlite3.connect(self.db_path)
        # TODO: This schema conflicts with main branch expectations
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                salt VARCHAR(50) NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                failed_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def hash_password(self, password, salt=None):
        """Password hashing - INSECURE IMPLEMENTATION"""
        # TODO: Use bcrypt or scrypt instead of MD5
        # This is temporary for testing only
        if not salt:
            salt = secrets.token_hex(16)
        
        # WARNING: MD5 is not secure for passwords!
        password_hash = hashlib.md5((password + salt).encode()).hexdigest()
        return password_hash, salt
    
    def create_user(self, username, email, password):
        """Create new user - PARTIAL IMPLEMENTATION"""
        # TODO: Add input validation
        # TODO: Check for existing users properly
        # TODO: Add email verification
        
        password_hash, salt = self.hash_password(password)
        
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute('''
                INSERT INTO users (username, email, password_hash, salt)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, salt))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # User already exists - but error handling is incomplete
            return False
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user - INCOMPLETE AND INSECURE"""
        # TODO: Implement rate limiting
        # TODO: Add account lockout after failed attempts
        # TODO: Proper session management
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute('''
            SELECT user_id, username, password_hash, salt, failed_attempts, locked_until
            FROM users WHERE username = ? AND is_active = 1
        ''', (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return None
        
        user_id, username, stored_hash, salt, failed_attempts, locked_until = user
        
        # TODO: Check if account is locked
        if locked_until and datetime.datetime.now() < datetime.datetime.fromisoformat(locked_until):
            return {'error': 'Account temporarily locked'}
        
        # Verify password
        password_hash, _ = self.hash_password(password, salt)
        
        if password_hash == stored_hash:
            # TODO: Reset failed attempts, update last_login
            return {
                'user_id': user_id,
                'username': username,
                'authenticated': True
            }
        else:
            # TODO: Increment failed attempts, implement lockout
            return None

# INCOMPLETE: Session management
active_sessions = {}  # This should be in database or Redis

def create_session(user_id):
    """Create user session - TEMPORARY IMPLEMENTATION"""
    session_token = secrets.token_urlsafe(32)
    active_sessions[session_token] = {
        'user_id': user_id,
        'created_at': datetime.datetime.now(),
        'expires_at': datetime.datetime.now() + datetime.timedelta(hours=24)
    }
    return session_token

def validate_session(session_token):
    """Validate session - INCOMPLETE"""
    if session_token not in active_sessions:
        return None
    
    session = active_sessions[session_token]
    if datetime.datetime.now() > session['expires_at']:
        del active_sessions[session_token]
        return None
    
    return session

# Decorator for protected routes - INCOMPLETE
def require_login(f):
    """Authentication decorator - NOT FULLY IMPLEMENTED"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Get session token from request headers
        # TODO: Integrate with Flask request context
        session_token = "dummy_token"  # Placeholder
        
        session = validate_session(session_token)
        if not session:
            return {"error": "Authentication required"}, 401
        
        return f(*args, **kwargs)
    return decorated_function

# Integration points with main app - INCOMPLETE
def integrate_with_main_app():
    """Integration with main.py - NEEDS WORK"""
    # TODO: Modify main.py to use authentication
    # TODO: Add login/logout routes to Flask app
    # TODO: Protect existing API endpoints
    # TODO: Add user context to task operations
    pass

if __name__ == "__main__":
    # Test code - INCOMPLETE
    auth = UserAuthentication()
    
    # Create test user
    result = auth.create_user("admin", "admin@test.com", "password123")
    print(f"User creation: {result}")
    
    # Test authentication
    user = auth.authenticate_user("admin", "password123")
    print(f"Authentication: {user}")
    
    # TODO: Add more comprehensive tests
    # TODO: Test error conditions
    # TODO: Test session management
    
    print("⚠️  LOGIN SYSTEM IS INCOMPLETE")
    print("⚠️  DO NOT USE IN PRODUCTION")
    print("⚠️  SECURITY ISSUES NEED TO BE RESOLVED")