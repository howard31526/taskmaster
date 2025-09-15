# config_master.py - Master 分支設定檔
"""
Master 分支專用設定
與 main 分支的差異：中文化、新增功能設定
"""

# 應用程式設定
APP_TITLE = "任務管理系統 v1.2"
APP_VERSION = "1.2-master"
WINDOW_SIZE = "900x700"
DATABASE_FILE = "tasks_master.db"

# 中文化設定
LANGUAGE = "zh-TW"
DATE_FORMAT = "%Y年%m月%d日"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%Y年%m月%d日 %H:%M"

# 功能選項
PRIORITY_OPTIONS = ["低", "中", "高", "緊急"]
CATEGORY_OPTIONS = ["工作", "個人", "學習", "購物", "一般"]
STATUS_OPTIONS = ["待辦", "進行中", "已完成", "已取消"]

# 預設值
DEFAULT_PRIORITY = "中"
DEFAULT_CATEGORY = "一般"
DEFAULT_STATUS = "待辦"

# API 設定
API_PORT = 5001  # 與 main 分支不同 (main 用 5000)
API_HOST = "127.0.0.1"
API_PREFIX = "/api"

# GUI 設定
FONT_FAMILY = "Microsoft JhengHei"  # 中文字體
FONT_SIZE = 10
TITLE_FONT_SIZE = 16

# 顏色設定
COLORS = {
    "緊急": "#FF4444",  # 紅色
    "高": "#FF8800",    # 橘色
    "中": "#4488FF",    # 藍色
    "低": "#88AA88"     # 綠色
}

# 功能開關
ENABLE_CATEGORIES = True
ENABLE_DUE_DATES = True
ENABLE_TIME_TRACKING = False  # 未來功能
ENABLE_NOTIFICATIONS = False  # 未來功能

class MasterConfig:
    """Master 分支設定類別"""
    
    def __init__(self):
        self.app_title = APP_TITLE
        self.version = APP_VERSION
        self.database = DATABASE_FILE
        
    def get_database_url(self):
        return f"sqlite:///{DATABASE_FILE}"
    
    def get_api_base_url(self):
        return f"http://{API_HOST}:{API_PORT}{API_PREFIX}"
    
    def get_priority_color(self, priority):
        return COLORS.get(priority, "#888888")
    
    def validate_priority(self, priority):
        return priority if priority in PRIORITY_OPTIONS else DEFAULT_PRIORITY
    
    def validate_category(self, category):
        return category if category in CATEGORY_OPTIONS else DEFAULT_CATEGORY

# 與 main 分支的差異說明
DIFFERENCES_FROM_MAIN = {
    "database_file": "tasks_master.db vs tasks.db",
    "api_port": "5001 vs 5000", 
    "language": "中文 vs 英文",
    "new_features": ["分類功能", "截止日期", "今日任務檢視"],
    "gui_changes": ["更大視窗", "新增輸入欄位", "中文標籤"],
    "api_format": "不同的回應格式和欄位名稱"
}

if __name__ == "__main__":
    config = MasterConfig()
    print(f"Master 分支設定:")
    print(f"應用程式: {config.app_title}")
    print(f"版本: {config.version}")
    print(f"資料庫: {config.database}")
    print(f"API 網址: {config.get_api_base_url()}")