# 任務: 將GUI從標準Tkinter遷移至CustomTkinter

## 規劃項目 (最小可交付粒度)

- [x] 項目 1: 新增 CustomTkinter 依賴套件
  - 檔案範圍: requirements.txt
  - 驗收條件: requirements.txt 包含 customtkinter 套件
  - ✅ Commit: `1073a56` - feat: 新增 customtkinter 依賴套件

- [ ] 項目 2: 更新 task_gui.py 的基礎架構 - 導入和主視窗設定
  - 檔案範圍: task_gui.py
  - 驗收條件: 主視窗使用 CTk() 而非 Tk()，導入 customtkinter 模組

- [ ] 項目 3: 轉換輸入區域元件為 CustomTkinter 元件
  - 檔案範圍: task_gui.py (create_input_section 方法)
  - 驗收條件: 使用 CTkLabel, CTkEntry, CTkTextbox, CTkRadioButton, CTkButton 替換標準元件

- [ ] 項目 4: 轉換任務列表區域為 CustomTkinter 元件
  - 檔案範圍: task_gui.py (create_task_list_section 方法)
  - 驗收條件: 使用 CustomTkinter 的 Scrollable Frame 或其他適合的容器元件

- [ ] 項目 5: 轉換操作按鈕區域為 CustomTkinter 元件
  - 檔案範圍: task_gui.py (create_button_section 方法)
  - 驗收條件: 所有按鈕使用 CTkButton，採用現代化樣式

- [ ] 項目 6: 更新樣式設定和主題配置
  - 檔案範圍: task_gui.py (setup_styles 方法)
  - 驗收條件: 使用 CustomTkinter 的主題系統，設定深色/淺色模式

- [ ] 項目 7: 更新對話框為 CustomTkinter 版本
  - 檔案範圍: task_gui.py (所有使用 messagebox 的方法)
  - 驗收條件: 使用 CTkMessageBox 或其他 CustomTkinter 對話框元件

- [ ] 項目 8: 測試並調整視覺效果
  - 檔案範圍: task_gui.py
  - 驗收條件: GUI 可正常啟動，所有功能運作正常，外觀符合 CustomTkinter 風格

## 狀態說明
- [ ] 未開始
- [/] 進行中
- [x] 已完成
