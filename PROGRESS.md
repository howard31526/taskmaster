# TaskMaster 重構進度追蹤

根據 README 檔案的規劃，將當前的單體檔案重構為模組化架構：

## 狀態更新規則
- [ ] → 未開始
- [/] → 進行中
- [x] → 完成

## 任務清單

1. **[x] 重構資料庫模組**
   - **檔案範圍：** database.py
   - **摘要：** 將 main.py 中的資料庫連線、建表、基本 CRUD 操作抽離到 database.py，包含資料庫連線管理和任務資料模型
   - **驗收條件：** database.py 可獨立運作，提供完整的資料庫操作介面
   - **Commit:** b766127 - refactor(database): 重構資料庫模組並新增專案進度追蹤

2. **[x] 重構配置與認證模組**
   - **檔案範圍：** config.py
   - **摘要：** 將硬編碼的配置值（API_KEY、資料庫路徑等）和認證邏輯從 main.py 移到 config.py
   - **驗收條件：** 配置值可統一管理，認證功能可獨立使用
   - **Commit:** 5a67f0a - refactor(config): 重構配置與認證模組

3. **[x] 重構工具模組**
   - **檔案範圍：** utils.py
   - **摘要：** 將通用的工具函式（日期處理、錯誤處理等）從 main.py 抽離到 utils.py
   - **驗收條件：** utils.py 包含可重用的工具函式
   - **Commit:** 2527af6 - refactor(utils): 重構工具模組為結構化工具類別

4. **[x] 重構 GUI 模組**
   - **檔案範圍：** task_gui.py
   - **摘要：** 將 TaskGUI 類別從 main.py 移到 task_gui.py，分離介面邏輯與業務邏輯
   - **驗收條件：** task_gui.py 可獨立提供完整的桌面介面

5. **[/] 重構 Web API 模組**
   - **檔案範圍：** api_server.py
   - **摘要：** 將 Flask API 路由從 main.py 移到 api_server.py，改善錯誤處理和 JSON 驗證
   - **驗收條件：** api_server.py 可獨立運行 Web API 服務

6. **[ ] 實作資料庫檢查工具**
   - **檔案範圍：** check_db.py
   - **摘要：** 建立獨立的資料庫查詢工具，用於檢視和管理資料庫內容
   - **驗收條件：** check_db.py 可執行資料庫狀態檢查

7. **[ ] 實作備份功能**
   - **檔案範圍：** backup_main.py
   - **摘要：** 將備份邏輯從 main.py 移到 backup_main.py，增強備份功能
   - **驗收條件：** backup_main.py 可獨立執行資料庫備份

8. **[ ] 重構主程式入口**
   - **檔案範圍：** main.py
   - **摘要：** 清理 main.py，只保留程式入口邏輯，引用其他模組
   - **驗收條件：** main.py 簡潔明瞭，各功能正常運作

