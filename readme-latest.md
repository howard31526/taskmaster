# TaskMaster - 個人任務管理系統

一個簡單而強大的任務管理應用程式，提供桌面介面和 Web API，讓你輕鬆管理日常任務。

## 專案簡介

TaskMaster 是個人任務管理工具，幫助你追蹤和管理日常工作。支援桌面 GUI 操作和 Web API 呼叫，提供靈活的使用方式。

## 主要功能

### 基本功能
- **任務管理**：新增、檢視、刪除任務
- **狀態追蹤**：待辦、進行中、已完成
- **優先級設定**：低、中、高三個等級
- **持久化儲存**：資料保存在本地 SQLite 資料庫

### 核心元件
- `main.py` - 主程式，包含 GUI、資料庫操作和 Flask API（整合式架構）
- `api_server.py` - 獨立的 Flask API 伺服器（port 8080）
- `database.py` - 資料庫管理類別
- `task_gui.py` - GUI 相關程式碼
- `utils.py` - 工具函式
- `config.py` - 設定檔
- `check_db.py` - 資料庫查詢工具
- `backup_main.py` - 資料備份功能

### 介面支援
- **桌面 GUI**：使用 Tkinter 圖形介面（`task_gui.py`）
- **Web API**：RESTful API 介面（`api_server.py`）
- **資料格式**：JSON 回應

## 快速開始

### 安裝

```bash
git clone https://github.com/howard31526/taskmaster.git
cd taskmaster
pip install -r requirements.txt
```

### 使用方式

#### 桌面介面
```bash
python main.py gui
```

#### Web API 服務
```bash
# 整合式 API 伺服器（port 5000）
python main.py api

# 獨立 API 伺服器（port 8080）
python api_server.py
```

#### 資料備份
```bash
python main.py backup
```

#### 資料庫查詢
```bash
python check_db.py
```

## API 端點

- `GET /api/tasks` 或 `/tasks` - 取得所有任務
- `POST /api/tasks` 或 `/tasks` - 建立新任務
- `DELETE /api/tasks/<id>` - 刪除任務

## 資料結構

任務包含以下欄位：
- **id** (INTEGER PRIMARY KEY) - 任務 ID
- **title** (TEXT) - 任務標題
- **description** (TEXT) - 任務描述
- **priority** (TEXT) - 優先級（預設 'low'）
- **status** (TEXT) - 狀態（預設 'pending'）
- **created_at** (TEXT/TIMESTAMP) - 建立時間

## 技術架構

- **語言**：Python 3.11.8
- **GUI 框架**：Tkinter
- **Web 框架**：Flask
- **資料庫**：SQLite
- **API 格式**：RESTful JSON

## 測試

```bash
# 執行單元測試
python -m pytest test.py
# 或
python test.py
```

## 開發環境設定

### 啟動虛擬環境
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 安裝相依套件
```bash
pip install -r requirements.txt
```

## 已知問題與技術債

1. 程式碼組織混亂 - `main.py` 包含太多功能
2. 有兩個不同的 API 伺服器實作（port 5000 和 8080）
3. 資料庫連線管理不一致
4. 缺乏完整的錯誤處理
5. API 回應格式不一致
6. 測試覆蓋率不足
7. 硬編碼的設定值（如 API key、資料庫路徑）

## 開發注意事項

- 修改資料庫操作時，注意有多個不同的實作方式
- GUI 和 API 功能混在同一檔案中，修改時要小心影響範圍
- 使用 Python 3.11.8 開發
- 所有合併必須透過 `/branch-merge` 指令
- 提交流程一律使用 `/pack-zh` 指令

## 授權

本專案採用開放原始碼授權。

## 貢獻

歡迎提交 Issue 和 Pull Request 來改善本專案！
