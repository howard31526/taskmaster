import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional
import customtkinter as ctk

from database import DatabaseManager
from utils import TaskUtils, ValidationUtils, LogUtils
from config import Config


class TaskGUI:
    """TaskMaster 桌面圖形介面"""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager(Config.get_database_path())
        self.logger = LogUtils.setup_logger("task_gui")

        # 設定 CustomTkinter 外觀
        ctk.set_appearance_mode("system")  # 可選: "light", "dark", "system"
        ctk.set_default_color_theme("dark-blue")  # 使用淡藍色主題

        self.window = ctk.CTk()
        self.window.title("TaskMaster - 任務管理系統")
        self.window.geometry("900x700")

        self.setup_styles()
        self.create_widgets()
        self.refresh_tasks()

    def setup_styles(self):
        """設定 UI 樣式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 配置樣式
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Custom.TButton', font=('Arial', 10))
        style.configure('Custom.Treeview', font=('Arial', 9))
        style.configure('Custom.Treeview.Heading', font=('Arial', 10, 'bold'))

    def create_widgets(self):
        """建立 UI 元件"""
        # 標題區域
        title_frame = tk.Frame(self.window, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = ttk.Label(title_frame, text="TaskMaster", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)

        # 新增任務區域
        self.create_input_section()

        # 任務列表區域
        self.create_task_list_section()

        # 操作按鈕區域
        self.create_button_section()

    def create_input_section(self):
        """建立輸入區域"""
        input_frame = ctk.CTkFrame(self.window)
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        # 標題標籤
        title_label = ctk.CTkLabel(input_frame, text="新增任務", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(10, 5), padx=10)

        # 標題輸入
        ctk.CTkLabel(input_frame, text="任務標題:", font=('Arial', 12)).grid(row=1, column=0, sticky="w", pady=5, padx=(10, 5))
        self.title_entry = ctk.CTkEntry(input_frame, width=400, font=('Arial', 12))
        self.title_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5, padx=(5, 10))

        # 描述輸入
        ctk.CTkLabel(input_frame, text="描述:", font=('Arial', 12)).grid(row=2, column=0, sticky="nw", pady=5, padx=(10, 5))
        self.desc_text = ctk.CTkTextbox(input_frame, width=400, height=100, font=('Arial', 12))
        self.desc_text.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5, padx=(5, 10))

        # 優先級選擇
        ctk.CTkLabel(input_frame, text="優先級:", font=('Arial', 12)).grid(row=3, column=0, sticky="w", pady=5, padx=(10, 5))
        self.priority_var = tk.StringVar(value="low")
        priority_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        priority_frame.grid(row=3, column=1, sticky="w", pady=5, padx=(5, 0))

        for priority in ["low", "medium", "high"]:
            priority_text = {"low": "低", "medium": "中", "high": "高"}[priority]
            ctk.CTkRadioButton(priority_frame, text=priority_text, variable=self.priority_var,
                              value=priority, font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 15))

        # 新增按鈕
        add_button = ctk.CTkButton(input_frame, text="新增任務", command=self.add_task_gui,
                                   font=('Arial', 12), width=100)
        add_button.grid(row=3, column=2, pady=5, padx=(10, 10))

        # 設定列權重
        input_frame.columnconfigure(1, weight=1)

    def create_task_list_section(self):
        """建立任務列表區域"""
        # 使用 CTkFrame 作為容器
        list_frame = ctk.CTkFrame(self.window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 標題標籤
        title_label = ctk.CTkLabel(list_frame, text="任務列表", font=("Arial", 14, "bold"))
        title_label.pack(pady=(10, 5), padx=10, anchor="w")

        # 內部容器用於 Treeview
        tree_container = ctk.CTkFrame(list_frame)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # 建立 Treeview (保留原生元件,因為 CustomTkinter 沒有替代品)
        columns = ("title", "description", "priority", "status", "created_at")
        self.task_listbox = ttk.Treeview(tree_container, columns=columns, show="tree headings",
                                        style='Custom.Treeview')

        # 設定欄位標題和寬度
        self.task_listbox.heading("#0", text="ID")
        self.task_listbox.heading("title", text="標題")
        self.task_listbox.heading("description", text="描述")
        self.task_listbox.heading("priority", text="優先級")
        self.task_listbox.heading("status", text="狀態")
        self.task_listbox.heading("created_at", text="建立時間")

        self.task_listbox.column("#0", width=50, minwidth=50)
        self.task_listbox.column("title", width=200, minwidth=150)
        self.task_listbox.column("description", width=250, minwidth=200)
        self.task_listbox.column("priority", width=80, minwidth=80)
        self.task_listbox.column("status", width=100, minwidth=100)
        self.task_listbox.column("created_at", width=150, minwidth=150)

        # 滾動條
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.task_listbox.configure(yscrollcommand=scrollbar.set)

        # 打包
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_button_section(self):
        """建立操作按鈕區域"""
        button_frame = tk.Frame(self.window, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # 按鈕樣式
        button_config = {'font': ('Arial', 10), 'width': 12}

        ttk.Button(button_frame, text="標記完成", command=self.complete_task,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(button_frame, text="標記進行中", command=self.mark_in_progress,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(button_frame, text="刪除任務", command=self.delete_task_gui,
                   style='Custom.TButton').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(button_frame, text="重新整理", command=self.refresh_tasks,
                   style='Custom.TButton').pack(side=tk.RIGHT)

    def add_task_gui(self):
        """新增任務的 GUI 處理"""
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get()

        # 驗證輸入
        if not ValidationUtils.validate_task_title(title):
            messagebox.showerror("錯誤", "請輸入有效的任務標題（1-200字元）")
            return

        if not ValidationUtils.validate_priority(priority):
            messagebox.showerror("錯誤", "請選擇有效的優先級")
            return

        # 清理輸入
        title = ValidationUtils.sanitize_text(title)
        description = ValidationUtils.sanitize_text(description)

        # 新增到資料庫
        if self.db_manager.add_task(title, description, priority):
            self.clear_inputs()
            self.refresh_tasks()
            LogUtils.log_action(f"新增任務: {title}")
            messagebox.showinfo("成功", "任務已成功新增")
        else:
            messagebox.showerror("錯誤", "新增任務失敗")

    def clear_inputs(self):
        """清空輸入欄位"""
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.priority_var.set("low")

    def get_selected_task_id(self) -> Optional[int]:
        """取得選中任務的 ID"""
        selection = self.task_listbox.selection()
        if selection:
            item = self.task_listbox.item(selection[0])
            try:
                return int(item['text'])
            except (ValueError, KeyError):
                pass
        return None

    def complete_task(self):
        """標記任務為完成"""
        task_id = self.get_selected_task_id()
        if task_id is None:
            messagebox.showwarning("警告", "請選擇一個任務")
            return

        if self.db_manager.update_task_status(task_id, "completed"):
            self.refresh_tasks()
            LogUtils.log_action(f"任務 {task_id} 標記為完成")
        else:
            messagebox.showerror("錯誤", "更新任務狀態失敗")

    def mark_in_progress(self):
        """標記任務為進行中"""
        task_id = self.get_selected_task_id()
        if task_id is None:
            messagebox.showwarning("警告", "請選擇一個任務")
            return

        if self.db_manager.update_task_status(task_id, "in_progress"):
            self.refresh_tasks()
            LogUtils.log_action(f"任務 {task_id} 標記為進行中")
        else:
            messagebox.showerror("錯誤", "更新任務狀態失敗")

    def delete_task_gui(self):
        """刪除任務的 GUI 處理"""
        task_id = self.get_selected_task_id()
        if task_id is None:
            messagebox.showwarning("警告", "請選擇一個任務")
            return

        if messagebox.askyesno("確認", "確定要刪除這個任務嗎？"):
            if self.db_manager.delete_task(task_id):
                self.refresh_tasks()
                LogUtils.log_action(f"刪除任務 {task_id}")
                messagebox.showinfo("成功", "任務已刪除")
            else:
                messagebox.showerror("錯誤", "刪除任務失敗")

    def refresh_tasks(self):
        """重新整理任務列表"""
        # 清空現有項目
        for item in self.task_listbox.get_children():
            self.task_listbox.delete(item)

        # 載入任務
        tasks = self.db_manager.get_tasks()
        for task in tasks:
            task_id, title, description, priority, status, created_at = task

            # 格式化顯示文字
            priority_text = {"low": "低", "medium": "中", "high": "高"}.get(priority, priority)
            status_text = {"pending": "待辦", "in_progress": "進行中", "completed": "已完成"}.get(status, status)

            # 截短描述
            short_desc = description[:50] + "..." if len(description) > 50 else description

            # 插入項目
            self.task_listbox.insert("", tk.END, text=task_id,
                                   values=(title, short_desc, priority_text, status_text, created_at))

    def run(self):
        """啟動 GUI"""
        try:
            LogUtils.log_action("啟動 TaskGUI")
            self.window.mainloop()
        except Exception as e:
            LogUtils.log_action(f"GUI 錯誤: {e}")
            messagebox.showerror("錯誤", f"應用程式錯誤: {e}")


def main():
    """主函式"""
    try:
        gui = TaskGUI()
        gui.run()
    except Exception as e:
        print(f"啟動失敗: {e}")


if __name__ == "__main__":
    main()