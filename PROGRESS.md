# 任務: 將 GUI 從 Tkinter 換成 CustomTkinter，參考現代化設計風格

## 規劃項目 (最小可交付粒度: 3-8 項)

- [ ] 項目 1: 更新依賴套件，新增 customtkinter
  - 檔案範圍: requirements.txt
  - 驗收條件: requirements.txt 包含 customtkinter 套件

- [ ] 項目 2: 轉換基礎匯入和主視窗設定
  - 檔案範圍: task_gui.py (第 1-25 行)
  - 驗收條件: 使用 customtkinter 取代 tkinter 的基礎匯入，主視窗使用 CTk 而非 Tk

- [ ] 項目 3: 更新輸入區域元件 (新增任務區)
  - 檔案範圍: task_gui.py (第 55-88 行，create_input_section 方法)
  - 驗收條件: 使用 CTkEntry、CTkTextbox、CTkRadioButton 等現代化元件

- [ ] 項目 4: 更新任務列表區域
  - 檔案範圍: task_gui.py (第 89-121 行，create_task_list_section 方法)
  - 驗收條件: 使用 CTkScrollableFrame 或其他適合的 customtkinter 元件顯示任務列表

- [ ] 項目 5: 更新操作按鈕區域
  - 檔案範圍: task_gui.py (第 122-141 行，create_button_section 方法)
  - 驗收條件: 所有按鈕改用 CTkButton，並套用現代化樣式

- [ ] 項目 6: 更新配色方案和樣式
  - 檔案範圍: task_gui.py (整體樣式設定)
  - 驗收條件: 套用現代化配色（參考圖片的藍、紫、粉、橙色調），移除舊的 ttk.Style 設定

- [ ] 項目 7: 更新對話框元件
  - 檔案範圍: task_gui.py (所有使用 messagebox 的地方)
  - 驗收條件: 改用 customtkinter 的對話框元件 (CTkMessagebox 或其他替代方案)

- [ ] 項目 8: 測試並優化整體 UI
  - 檔案範圍: task_gui.py (全檔案)
  - 驗收條件: GUI 能正常啟動並運作，視覺風格符合現代化設計

## 狀態說明
- [ ] 未開始
- [/] 進行中
- [x] 已完成
