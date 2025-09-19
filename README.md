TaskMaster - 個人任務管理系統
---
一個簡單的任務管理應用程式，提供桌面介面和 Web API，讓你輕鬆管理日常任務。
專案簡介
TaskMaster 是個人任務管理工具，幫助你追蹤和管理日常工作。支援桌面 GUI 操作和 Web API 呼叫。
---
## 功能需求 ##

**基本功能：**
任務管理：新增、檢視、刪除任務
狀態追蹤：待辦、進行中、已完成
優先級設定：低、中、高三個等級
持久化儲存：資料保存在本地資料庫
認證功能 ----> config.py
其他支援工具 ----> utils.py
資料庫設定 ----> database.py
查詢資料 ----> check_db.py
備份資料 ----> backup_main.py

**介面支援：**
桌面 GUI：Tkinter 圖形介面 ----> task_gui.py
Web API：RESTful API 介面 ----> api_server.py
資料格式：JSON 回應

**資料結構**
任務包含：標題、描述、優先級、狀態、建立時間

## 快速開始 ##

# 安裝
git clone https://github.com/howard31526/taskmaster.git
cd taskmaster
pip install -r requirements.txt

# 使用
**桌面介面**
python main.py gui

**Web API 服務**
python main.py api

**技術架構**
語言：Python 3.10+
GUI：Tkinter
Web 框架：Flask
資料庫：SQLite
API：RESTful JSON
