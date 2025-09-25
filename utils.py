import datetime
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Union

class DateUtils:
    """日期處理工具類別"""

    @staticmethod
    def format_datetime(dt: datetime.datetime) -> str:
        """格式化日期時間為字串"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_datetime(date_str: str) -> Optional[datetime.datetime]:
        """解析日期字串為 datetime 物件"""
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y"
        ]

        for fmt in formats:
            try:
                return datetime.datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

    @staticmethod
    def get_current_timestamp() -> str:
        """取得當前時間戳"""
        return DateUtils.format_datetime(datetime.datetime.now())

    @staticmethod
    def time_ago(dt: datetime.datetime) -> str:
        """計算時間差距描述"""
        now = datetime.datetime.now()
        diff = now - dt

        if diff.days > 0:
            return f"{diff.days} 天前"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} 小時前"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} 分鐘前"
        else:
            return "剛剛"

class ValidationUtils:
    """驗證工具類別"""

    @staticmethod
    def validate_priority(priority: str) -> bool:
        """驗證優先級是否有效"""
        return priority.lower() in ["low", "medium", "high"]

    @staticmethod
    def validate_status(status: str) -> bool:
        """驗證狀態是否有效"""
        return status.lower() in ["pending", "in_progress", "completed"]

    @staticmethod
    def validate_task_title(title: str) -> bool:
        """驗證任務標題"""
        return bool(title and title.strip() and len(title.strip()) <= 200)

    @staticmethod
    def sanitize_text(text: str) -> str:
        """清理文字內容"""
        if not text:
            return ""
        # 移除多餘空白和特殊字元
        cleaned = re.sub(r'\s+', ' ', text.strip())
        # 移除潛在的危險字元
        cleaned = re.sub(r'[<>"\']', '', cleaned)
        return cleaned

class TaskUtils:
    """任務相關工具類別"""

    @staticmethod
    def get_priority_score(priority: str) -> int:
        """取得優先級分數"""
        scores = {"low": 1, "medium": 2, "high": 3}
        return scores.get(priority.lower(), 1)

    @staticmethod
    def format_task_display(task_data: tuple) -> str:
        """格式化任務顯示文字"""
        if len(task_data) >= 4:
            task_id, title, description, priority, status = task_data[:5]
            return f"{task_id} - {title} ({status}) [優先級: {priority}]"
        return str(task_data)

    @staticmethod
    def extract_task_id_from_text(text: str) -> Optional[int]:
        """從文字中萃取任務 ID"""
        try:
            # 假設格式為 "ID - Title..."
            parts = text.split(" - ")
            if parts:
                return int(parts[0])
        except (ValueError, IndexError):
            pass
        return None

class LogUtils:
    """日誌工具類別"""

    @staticmethod
    def setup_logger(name: str, log_file: str = "taskmaster.log") -> logging.Logger:
        """設定日誌記錄器"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # 避免重複添加 handler
        if not logger.handlers:
            # 檔案處理器
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)

            # 格式設定
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger

    @staticmethod
    def log_action(action: str, logger_name: str = "taskmaster"):
        """記錄操作日誌"""
        logger = LogUtils.setup_logger(logger_name)
        logger.info(action)

class FileUtils:
    """檔案處理工具類別"""

    @staticmethod
    def safe_write_json(data: Any, file_path: str) -> bool:
        """安全地寫入 JSON 檔案"""
        try:
            # 確保目錄存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            LogUtils.log_action(f"寫入 JSON 檔案失敗: {e}")
            return False

    @staticmethod
    def safe_read_json(file_path: str) -> Optional[Any]:
        """安全地讀取 JSON 檔案"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            LogUtils.log_action(f"讀取 JSON 檔案失敗: {e}")
        return None

    @staticmethod
    def ensure_directory(dir_path: str) -> bool:
        """確保目錄存在"""
        try:
            os.makedirs(dir_path, exist_ok=True)
            return True
        except Exception as e:
            LogUtils.log_action(f"建立目錄失敗: {e}")
            return False