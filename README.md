# TaskMaster - 個人任務管理系統

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

一個功能完整的任務管理應用程式，提供桌面 GUI 介面和 RESTful API 服務，讓您輕鬆管理日常任務。

## 目錄

- [功能特色](#功能特色)
- [系統需求](#系統需求)
- [安裝指南](#安裝指南)
- [使用說明](#使用說明)
- [API 文件](#api-文件)
- [專案架構](#專案架構)
- [開發指南](#開發指南)
- [測試](#測試)
- [已知問題](#已知問題)
- [貢獻指南](#貢獻指南)
- [授權資訊](#授權資訊)

## 功能特色

### 核心功能

- **任務管理**：建立、檢視、編輯、刪除任務
- **狀態追蹤**：支援待辦(pending)、進行中(in_progress)、已完成(completed)三種狀態
- **優先級設定**：低(low)、中(medium)、高(high)三個等級
- **持久化儲存**：使用 SQLite 資料庫，資料安全可靠
- **資料備份**：內建備份功能，保護重要資料

### 介面支援

- **桌面 GUI**：基於 Tkinter 的圖形化介面，操作直覺簡單
- **Web API**：RESTful API 服務，支援第三方整合
- **多種啟動模式**：GUI、API、備份模式可選

### 資料結構

每個任務包含以下欄位：
- `id`：任務唯一識別碼 (自動生成)
- `title`：任務標題 (必填)
- `description`：任務詳細描述
- `priority`：優先級 (預設: low)
- `status`：任務狀態 (預設: pending)
- `created_at`：建立時間 (自動記錄)

## 系統需求

- **Python**：3.11.8 或更高版本（建議使用 3.10+）
- **作業系統**：Windows、macOS、Linux
- **依賴套件**：
  - Flask >= 2.3.0 (Web API)
  - requests >= 2.28.0 (HTTP 請求)
  - tkinter (GUI，Python 內建)
  - sqlite3 (資料庫，Python 內建)

## 安裝指南

### 1. 複製專案

```bash
git clone https://github.com/howard31526/taskmaster.git
cd taskmaster
```

### 2. 建立虛擬環境（建議）

**Windows：**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS：**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 4. 驗證安裝

```bash
python main.py --help
```

## 使用說明

### 啟動 GUI 介面

```bash
python main.py gui
```

啟動圖形化介面，適合一般使用者操作。

### 啟動 API 服務

**方式一：使用 main.py (Port 5000)**
```bash
python main.py api
```

**方式二：使用獨立 API 服務 (Port 8080)**
```bash
python api_server.py
```

### 執行資料備份

```bash
python main.py backup
```

備份檔案將儲存至 `backups/` 目錄。

### 檢查資料庫

```bash
python check_db.py
```

查看資料庫內容和統計資訊。

## API 文件

### 基本資訊

- **Base URL (main.py)**：`http://localhost:5000`
- **Base URL (api_server.py)**：`http://localhost:8080`
- **內容格式**：JSON

### API 端點

#### 1. 取得所有任務

```http
GET /api/tasks
GET /tasks
```

**回應範例：**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "完成專案文件",
      "description": "撰寫 README 和 API 文件",
      "priority": "high",
      "status": "in_progress",
      "created_at": "2025-10-07 10:30:00"
    }
  ]
}
```

#### 2. 建立新任務

```http
POST /api/tasks
POST /tasks
```

**請求範例：**
```json
{
  "title": "新任務標題",
  "description": "任務描述",
  "priority": "medium",
  "status": "pending"
}
```

**回應範例：**
```json
{
  "message": "Task created successfully",
  "task_id": 2
}
```

#### 3. 刪除任務

```http
DELETE /api/tasks/<task_id>
```

**回應範例：**
```json
{
  "message": "Task deleted successfully"
}
```

### 錯誤處理

API 使用標準 HTTP 狀態碼：

- `200 OK`：請求成功
- `201 Created`：資源建立成功
- `400 Bad Request`：請求參數錯誤
- `404 Not Found`：資源不存在
- `500 Internal Server Error`：伺服器錯誤

## 專案架構

```
taskmaster/
├── main.py              # 主程式（整合 GUI、API、備份）
├── api_server.py        # 獨立 API 伺服器
├── database.py          # 資料庫管理類別
├── task_gui.py          # GUI 介面程式碼
├── config.py            # 設定檔
├── utils.py             # 工具函式
├── check_db.py          # 資料庫檢查工具
├── backup_main.py       # 備份功能模組
├── test.py              # 單元測試
├── requirements.txt     # Python 依賴套件
├── README.md            # 專案說明文件
├── CLAUDE.md            # Claude Code 開發指引
├── tasks.db             # SQLite 資料庫（執行時自動建立）
└── backups/             # 備份檔案目錄（自動建立）
```

### 核心模組說明

| 檔案 | 功能說明 |
|------|---------|
| `main.py` | 主程式入口，整合 GUI、API 和備份功能 |
| `api_server.py` | 獨立的 Flask API 伺服器（Port 8080） |
| `database.py` | 資料庫連線、CRUD 操作管理 |
| `task_gui.py` | Tkinter GUI 介面實作 |
| `config.py` | 應用程式設定和認證功能 |
| `utils.py` | 通用工具函式 |
| `check_db.py` | 資料庫內容檢查工具 |
| `backup_main.py` | 資料備份與還原功能 |
| `test.py` | 單元測試程式 |

## 開發指南

### 開發環境設定

1. **啟動虛擬環境**
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

2. **安裝開發依賴**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8  # 測試與程式碼品質工具
   ```

3. **查閱開發指引**

   請參閱 [CLAUDE.md](CLAUDE.md) 了解：
   - 專案概述與架構
   - 程式碼規範
   - 分支管理策略
   - 提交流程規範

### 資料庫結構

SQLite 資料庫 `tasks.db`，包含 `tasks` 表格：

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'low',
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 程式碼風格

- 遵循 PEP 8 編碼規範
- 使用有意義的變數和函式名稱
- 適當添加註解和文件字串
- 建議使用 `black` 進行程式碼格式化

## 測試

### 執行測試

```bash
# 使用 pytest
python -m pytest test.py

# 直接執行測試檔
python test.py
```

### 測試涵蓋範圍

- 資料庫 CRUD 操作
- API 端點功能
- 資料驗證邏輯
- 錯誤處理機制

## 已知問題

目前專案存在以下技術債與待改進項目：

1. **架構問題**
   - `main.py` 包含過多功能，需要重構
   - 存在兩個不同的 API 伺服器實作（Port 5000 和 8080）

2. **程式碼品質**
   - 資料庫連線管理不一致
   - 缺乏完整的錯誤處理機制
   - API 回應格式不統一
   - 存在硬編碼的設定值

3. **測試與文件**
   - 測試覆蓋率不足
   - 部分功能缺少文件說明

4. **功能缺失**
   - 缺少任務編輯功能
   - 缺少任務搜尋和篩選
   - 缺少使用者認證機制
   - 缺少任務分類標籤

詳細資訊請參閱 [CLAUDE.md](CLAUDE.md)。

## 貢獻指南

歡迎貢獻程式碼、回報問題或提出建議！

### 提交流程

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更（請遵循專案的提交規範）
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 注意事項

- 請先閱讀 [CLAUDE.md](CLAUDE.md) 了解專案規範
- 所有合併必須透過 `/branch-merge` 指令
- 提交時請使用 `/pack-zh` 指令
- 確保測試通過後再提交 PR

## 授權資訊

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

## 聯絡方式

- **專案連結**：[https://github.com/howard31526/taskmaster](https://github.com/howard31526/taskmaster)
- **問題回報**：[Issues](https://github.com/howard31526/taskmaster/issues)

---

**開發版本**：1.0.0
**最後更新**：2025-10-12
