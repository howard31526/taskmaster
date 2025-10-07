# TaskMaster 專案檔案說明文件

> **最後更新日期：** 2025-10-07
> **專案版本：** 1.0.0
> **本文件說明：** 此文件描述 main 分支中各檔案的作用，並標記無用或過時的檔案

---

## 📋 目錄

- [核心程式檔案](#核心程式檔案)
- [設定與工具檔案](#設定與工具檔案)
- [測試與開發檔案](#測試與開發檔案)
- [文件檔案](#文件檔案)
- [靜態資源與模板](#靜態資源與模板)
- [設定與版本控制](#設定與版本控制)
- [無用或過時的檔案](#無用或過時的檔案)
- [自動生成的檔案](#自動生成的檔案)

---

## 核心程式檔案

### ✅ `main.py`
**用途：** 主程式入口點
**功能：**
- 統一的命令行介面，提供 GUI、Web、備份、檢查等模式
- 整合所有功能模組的啟動邏輯
- 資料庫初始化功能
- 命令行參數解析與路由

**執行方式：**
```bash
python main.py gui      # 啟動 GUI 介面
python main.py web      # 啟動 Web 伺服器
python main.py backup   # 執行備份
python main.py check    # 檢查資料庫
```

**狀態：** ✅ 正在使用

---

### ✅ `api_server.py`
**用途：** 獨立的 Flask Web 伺服器
**功能：**
- 提供 RESTful API 端點（/api/tasks, /tasks 等）
- Web 介面的路由處理
- 任務的 CRUD 操作 API
- 資料庫連線管理
- 統計資料 API

**執行方式：**
```bash
python api_server.py    # 啟動於 Port 5000
```

**API 端點：**
- `GET /` - 主頁面
- `GET /api/tasks` - 取得所有任務
- `POST /tasks` - 建立新任務
- `POST /tasks/<id>/update` - 更新任務狀態
- `POST /tasks/<id>/delete` - 刪除任務
- `GET /api/stats` - 取得統計資料

**狀態：** ✅ 正在使用

**已知問題：** 與 main.py 的 API 功能有重複，存在兩個不同 port 的實作

---

### ✅ `database.py`
**用途：** 資料庫管理模組
**功能：**
- `DatabaseManager` 類別：封裝所有資料庫操作
- 資料庫連線管理
- 任務的 CRUD 操作（新增、查詢、更新、刪除）
- 資料庫初始化與表格建立
- Type hints 支援，提升程式碼可讀性

**主要方法：**
- `init_database()` - 初始化資料庫
- `add_task()` - 新增任務
- `get_tasks()` - 取得所有任務
- `update_task_status()` - 更新任務狀態
- `delete_task()` - 刪除任務
- `get_task_by_id()` - 依 ID 查詢任務

**狀態：** ✅ 正在使用

---

### ✅ `task_gui.py`
**用途：** Tkinter 圖形使用者介面
**功能：**
- `TaskGUI` 類別：完整的桌面 GUI 應用程式
- 任務新增、編輯、刪除介面
- 任務列表顯示（使用 Treeview）
- 狀態更新操作（待辦、進行中、完成）
- 優先級設定介面
- 使用 ttk 元件提供現代化外觀

**主要功能區域：**
- 標題區域
- 新增任務輸入區域（標題、描述、優先級）
- 任務列表顯示區域
- 操作按鈕區域（完成、進行中、刪除、重新整理）

**狀態：** ✅ 正在使用

---

### ✅ `utils.py`
**用途：** 工具函式庫
**功能：**

**工具類別：**
1. **`DateUtils`** - 日期時間處理
   - 格式化日期時間
   - 解析日期字串
   - 計算時間差距（多久以前）

2. **`ValidationUtils`** - 資料驗證
   - 驗證優先級（low/medium/high）
   - 驗證狀態（pending/in_progress/completed）
   - 驗證任務標題
   - 清理文字內容（防止注入攻擊）

3. **`TaskUtils`** - 任務相關工具
   - 取得優先級分數
   - 格式化任務顯示
   - 從文字萃取任務 ID

4. **`LogUtils`** - 日誌記錄
   - 設定日誌記錄器
   - 記錄操作日誌

5. **`FileUtils`** - 檔案處理
   - 安全讀寫 JSON 檔案
   - 確保目錄存在

**狀態：** ✅ 正在使用

---

### ✅ `config.py`
**用途：** 應用程式設定管理
**功能：**

**`Config` 類別：**
- 資料庫路徑設定
- API 伺服器設定（host, port, API key）
- 應用程式設定（debug 模式、secret key）
- 預設使用者設定
- API 金鑰驗證

**`AuthManager` 類別：**
- 簡單的認證管理
- 使用者登入/登出
- 認證狀態檢查
- 需要認證的裝飾器

**環境變數支援：**
- `DATABASE_PATH`
- `API_HOST` / `API_PORT`
- `API_KEY`
- `DEBUG_MODE`
- `SECRET_KEY`
- `DEFAULT_USER`

**狀態：** ✅ 正在使用

**注意事項：** 包含硬編碼的 API key（sk-1234567890abcdef），建議使用環境變數

---

## 設定與工具檔案

### ✅ `check_db.py`
**用途：** 資料庫檢查與維護工具
**功能：**
- `DatabaseChecker` 類別：全面的資料庫檢查工具
- 檢查資料庫連線狀態
- 顯示表格結構資訊
- 顯示統計資訊（任務數量、狀態分布、優先級分布）
- 列出所有任務
- 搜尋任務功能
- 資料完整性驗證（檢查空標題、無效狀態、無效優先級、無效日期）
- 資料庫清理功能（移除無效資料）

**執行方式：**
```bash
python check_db.py              # 完整檢查
python check_db.py stats        # 僅顯示統計
python check_db.py list 20      # 顯示 20 筆任務
python check_db.py search "關鍵字"  # 搜尋任務
python check_db.py check        # 驗證資料完整性
python check_db.py cleanup      # 清理無效資料
```

**狀態：** ✅ 正在使用

---

### ✅ `backup_main.py`
**用途：** 資料備份模組
**功能：**
- 資料庫備份功能（基本實作）
- 舊版程式碼的備份點

**內容：**
```python
# 包含舊的 GUI 程式碼和資料庫操作函式
# 標記為 TODO: 待確認新版本運作後移除
```

**狀態：** ⚠️ 部分功能已被整合到其他模組，檔案中保留舊程式碼供參考

---

## 測試與開發檔案

### ⚠️ `test.py`
**用途：** 單元測試
**功能：**
- 測試任務建立
- 測試資料庫操作
- 使用 unittest 框架

**執行方式：**
```bash
python -m pytest test.py
python test.py
```

**狀態：** ⚠️ 測試不完整

**已知問題：**
- 測試覆蓋率不足
- 某些測試因架構問題無法正確執行
- 缺少 API 端點測試
- 缺少錯誤條件測試
- 缺少 GUI 互動測試
- 檔案中有註解說明測試架構問題

---

### ❌ `temp.py`
**用途：** 臨時測試檔案
**功能：**
- 快速測試資料庫連線
- 查看資料庫表格結構
- 簡單的除錯工具

**內容：**
```python
def quick_test():
    # 快速查詢任務
def debug_database():
    # 顯示表格結構
```

**狀態：** ❌ 應該刪除（檔案開頭註解寫著 "TODO: DELETE THIS"）

---

## 文件檔案

### ✅ `README.md`
**用途：** 專案主要說明文件
**內容：**
- 專案介紹與功能特色
- 系統需求與安裝指南
- 使用說明與 API 文件
- 專案架構說明
- 開發指南與測試說明
- 已知問題清單
- 貢獻指南與授權資訊

**狀態：** ✅ 正在使用，內容完整詳細

---

### ✅ `CLAUDE.md`
**用途：** Claude Code 開發指引
**內容：**
- 專案概述
- 開發環境設定
- 常用指令
- 程式碼架構說明
- 資料庫結構
- API 端點列表
- 已知問題與技術債
- 分支合併策略（必須使用 `/branch-merge` 指令）
- 提交流程（使用 `/pack-zh` 指令）

**狀態：** ✅ 正在使用

**特別注意：**
- 文件要求使用中文回應
- 禁止直接使用 `git merge`
- 所有合併必須透過 `/branch-merge` 指令
- 提交必須使用 `/pack-zh` 指令

---

### ✅ `requirements.txt`
**用途：** Python 依賴套件清單
**內容：**
```
Flask>=2.3.0
requests>=2.28.0
```

**狀態：** ✅ 正在使用

**注意：** 註解中提到 tkinter 和 sqlite3 為內建模組，不需列出

---

## 靜態資源與模板

### ✅ `templates/` 目錄
**用途：** Flask HTML 模板
**內容：**
- `base.html` - 基礎模板
- `index.html` - 主頁面模板

**狀態：** ✅ 正在使用

---

### ✅ `static/` 目錄
**用途：** 靜態檔案（CSS、JavaScript）
**結構：**
```
static/
├── css/    # CSS 樣式檔案
└── js/     # JavaScript 檔案
```

**狀態：** ✅ 正在使用

---

## 設定與版本控制

### ✅ `.gitignore`
**用途：** Git 忽略檔案清單
**內容：** 指定不需要版本控制的檔案（如 `__pycache__/`, `*.pyc`, `venv/`, `tasks.db` 等）

**狀態：** ✅ 正在使用

---

### ✅ `.github/workflows/`
**用途：** GitHub Actions 工作流程設定
**內容：** CI/CD 自動化流程設定

**狀態：** ✅ 正在使用

---

### ✅ `.claude/`
**用途：** Claude Code 設定目錄
**內容：**
- `commands/` - 自訂命令
- `settings.local.json` - 本地設定

**狀態：** ✅ 正在使用

---

## 無用或過時的檔案

### ❌ `temp.py`
**原因：**
- 檔案開頭註解明確標示 "TODO: DELETE THIS"
- 僅用於臨時測試和除錯
- 功能已被 `check_db.py` 取代

**建議：** 刪除此檔案

---

### ⚠️ `backup_main.py`
**原因：**
- 檔案註解寫著 "Backup of main.py before refactoring"
- 註解標示 "TODO: Remove this file after confirming new version works"
- 包含舊版程式碼，僅作為參考備份

**現狀：**
- 目前僅包含簡單的舊程式碼片段
- 新版本已在 `main.py` 中穩定運作

**建議：**
- 短期內可保留作為參考
- 長期應該刪除或移至專門的備份目錄

---

### ⚠️ `test.py`
**原因：**
- 測試不完整且部分測試無法正確運作
- 檔案內註解列出許多缺失的測試項目
- 架構問題導致某些測試無法驗證

**現狀：** 檔案存在但測試覆蓋率嚴重不足

**建議：**
- 需要重寫和擴充測試
- 不建議刪除，但需要大幅改進

---

### ❌ 不明檔案（根目錄中）
在專案根目錄發現幾個不明檔案名稱：
- `VARCHAR(20),           -- Different from main branch (uses 'status')`
- `e Operations STABLE`
- `ion 2.1.0-master`
- `k Management STABLE`
- `ql`
- `ter`

**原因：**
- 檔案名稱異常，看起來像是損壞或錯誤建立的檔案
- 不符合專案命名規範
- 無法判斷用途

**建議：** 檢查並刪除這些異常檔案

---

## 自動生成的檔案

### 🔄 `tasks.db`
**用途：** SQLite 資料庫檔案
**狀態：** 執行時自動建立，不應納入版本控制（已在 .gitignore 中）

---

### 🔄 `taskmaster.log`
**用途：** 應用程式日誌檔案
**狀態：** 由 `LogUtils` 自動建立

---

### 🔄 `backup_tasks.db`
**用途：** 資料庫備份檔案
**狀態：** 執行備份指令時自動建立

---

### 🔄 `backups/` 目錄
**用途：** 備份檔案儲存目錄
**狀態：** 執行備份功能時自動建立

---

### 🔄 `log_history/` 目錄
**用途：** 歷史日誌檔案
**狀態：** 系統自動建立

---

### 🔄 `merge_logs/` 目錄
**用途：** 合併操作日誌
**狀態：** 使用 `/branch-merge` 指令時自動建立

---

### 🔄 `push_logs/` 目錄
**用途：** 推送操作日誌
**狀態：** 使用 `/pack-zh` 指令時自動建立

---

## 📊 檔案分類統計

| 分類 | 檔案數量 | 說明 |
|------|---------|------|
| ✅ 核心程式檔案 | 6 個 | main.py, api_server.py, database.py, task_gui.py, utils.py, config.py |
| ✅ 工具檔案 | 2 個 | check_db.py, backup_main.py |
| ✅ 文件檔案 | 3 個 | README.md, CLAUDE.md, requirements.txt |
| ✅ 模板與靜態資源 | 2 個目錄 | templates/, static/ |
| ⚠️ 需要改進 | 2 個 | test.py（測試不完整）, backup_main.py（待移除） |
| ❌ 應該刪除 | 1+ 個 | temp.py 及根目錄的異常檔案 |
| 🔄 自動生成 | 7 個 | tasks.db, *.log, 備份檔案, 日誌目錄等 |

---

## 🎯 建議的清理行動

### 立即刪除
1. ✅ `temp.py` - 臨時測試檔案，已標記待刪除
2. ✅ 根目錄中的異常檔案（如 `VARCHAR(20),...` 等）

### 短期內處理
1. ⚠️ 改進 `test.py` - 補充完整的測試覆蓋
2. ⚠️ 評估 `backup_main.py` - 確認新版本穩定後刪除

### 長期改進
1. 🔧 解決兩個 API 伺服器並存的問題（main.py 和 api_server.py）
2. 🔧 統一資料庫連線管理方式
3. 🔧 移除硬編碼的設定值（如 API key）
4. 🔧 增加完整的錯誤處理機制

---

## 📝 總結

### 正在使用的核心檔案（不可刪除）
- `main.py` - 主程式入口
- `api_server.py` - Web 伺服器
- `database.py` - 資料庫管理
- `task_gui.py` - GUI 介面
- `utils.py` - 工具函式庫
- `config.py` - 設定管理
- `check_db.py` - 資料庫檢查工具

### 重要文件（不可刪除）
- `README.md` - 專案說明
- `CLAUDE.md` - 開發指引
- `requirements.txt` - 依賴清單

### 可以刪除的檔案
- ❌ `temp.py` - 臨時測試檔案
- ❌ 根目錄異常檔案

### 需要改進的檔案
- ⚠️ `test.py` - 測試覆蓋率不足
- ⚠️ `backup_main.py` - 僅作備份參考，可考慮移除

---

**文件結束**
