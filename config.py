import os
from typing import Optional

class Config:
    """應用程式配置管理類別"""

    # 資料庫設定
    DATABASE_PATH = os.getenv("DATABASE_PATH", "tasks.db")

    # API 設定 (整合 main.py 的 API_KEY)
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", "5000"))
    API_KEY = os.getenv("API_KEY", "sk-1234567890abcdef")

    # 應用程式設定 (整合 main.py 的 DEBUG_MODE)
    DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

    # 預設使用者設定 (整合 main.py 的 current_user)
    DEFAULT_USER = os.getenv("DEFAULT_USER", "admin")

    @classmethod
    def get_database_path(cls) -> str:
        """取得資料庫檔案路徑"""
        return cls.DATABASE_PATH

    @classmethod
    def get_api_config(cls) -> dict:
        """取得 API 伺服器配置"""
        return {
            "host": cls.API_HOST,
            "port": cls.API_PORT,
            "debug": cls.DEBUG_MODE
        }

    @classmethod
    def validate_api_key(cls, api_key: str) -> bool:
        """驗證 API 金鑰"""
        return api_key == cls.API_KEY

class AuthManager:
    """認證管理類別"""

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.current_user = None

    def login(self, username: str, password: Optional[str] = None) -> bool:
        """使用者登入驗證"""
        # 簡化的認證邏輯，實際應用中應該使用更安全的方式
        if username == self.config.DEFAULT_USER:
            self.current_user = username
            return True
        return False

    def logout(self) -> None:
        """使用者登出"""
        self.current_user = None

    def is_authenticated(self) -> bool:
        """檢查是否已認證"""
        return self.current_user is not None

    def get_current_user(self) -> Optional[str]:
        """取得當前使用者"""
        return self.current_user

    def require_auth(self, func):
        """裝飾器：需要認證才能執行的函式"""
        def wrapper(*args, **kwargs):
            if not self.is_authenticated():
                raise PermissionError("需要登入才能執行此操作")
            return func(*args, **kwargs)
        return wrapper