# 任務: 將 GUI 從 Tkinter 轉換為 CustomTkinter，參考現代化任務管理介面設計

## 規劃項目 (最小可交付粒度: 3-8 項)

- [/] 項目 1: 更新 requirements.txt，新增 customtkinter 依賴套件
  - 檔案範圍: requirements.txt
  - 驗收條件: requirements.txt 包含 customtkinter 套件

- [ ] 項目 2: 轉換 task_gui.py 的基礎匯入和主視窗設定為 CustomTkinter
  - 檔案範圍: task_gui.py
  - 驗收條件: 主視窗使用 CTk() 而非 tk.Tk()，匯入 customtkinter 套件

- [ ] 項目 3: 更新輸入區域 (create_input_section) 使用 CustomTkinter 元件
  - 檔案範圍: task_gui.py (create_input_section 方法)
  - 驗收條件: 標題輸入、描述輸入、優先級選擇使用 CTkEntry, CTkTextbox, CTkRadioButton

- [ ] 項目 4: 更新任務列表區域 (create_task_list_section) 使用 CustomTkinter 風格
  - 檔案範圍: task_gui.py (create_task_list_section 方法)
  - 驗收條件: 任務列表使用 CTkScrollableFrame 或保留 Treeview 但搭配 CTk 風格

- [ ] 項目 5: 更新操作按鈕區域 (create_button_section) 使用 CTkButton
  - 檔案範圍: task_gui.py (create_button_section 方法)
  - 驗收條件: 所有按鈕使用 CTkButton 元件

- [ ] 項目 6: 更新配色方案和樣式，參考現代化設計
  - 檔案範圍: task_gui.py (setup_styles 和 __init__ 方法)
  - 驗收條件: 使用現代化配色（淺色/深色主題支援），圓角設計

- [ ] 項目 7: 更新 messagebox 和其他對話框為 CustomTkinter 版本
  - 檔案範圍: task_gui.py (所有使用 messagebox 的方法)
  - 驗收條件: 使用 CTkMessagebox 或 CTkInputDialog 替代原本的 tk.messagebox

- [ ] 項目 8: 測試並優化整體 UI 體驗
  - 檔案範圍: task_gui.py (所有方法)
  - 驗收條件: GUI 可正常啟動且所有功能運作正常，視覺效果符合現代化設計

## 狀態說明
- [ ] 未開始
- [/] 進行中
- [x] 已完成
