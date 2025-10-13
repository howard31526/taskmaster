import customtkinter as ctk
from tkinter import messagebox
from typing import Optional

from database import DatabaseManager
from utils import TaskUtils, ValidationUtils, LogUtils
from config import Config


# 設定 CustomTkinter 外觀模式和顏色主題
ctk.set_appearance_mode("light")  # 可選: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # 可選: "blue", "green", "dark-blue"


class TaskGUI:
    """TaskMaster 桌面圖形介面 - CustomTkinter 版本"""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager(Config.get_database_path())
        self.logger = LogUtils.setup_logger("task_gui")

        # 主視窗設定
        self.window = ctk.CTk()
        self.window.title("TaskMaster - 任務管理系統")
        self.window.geometry("1200x800")

        # 設定視窗最小尺寸
        self.window.minsize(900, 600)

        # 建立主要佈局
        self.create_main_layout()
        self.refresh_tasks()

    def create_main_layout(self):
        """建立主要佈局結構"""
        # 設定網格權重
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # 建立側邊欄
        self.create_sidebar()

        # 建立主要內容區域
        self.create_main_content()

    def create_sidebar(self):
        """建立左側側邊欄"""
        self.sidebar = ctk.CTkFrame(self.window, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_rowconfigure(7, weight=1)  # 讓底部按鈕置底

        # 應用程式標題
        title_label = ctk.CTkLabel(
            self.sidebar,
            text="TaskMaster",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        # 導航按鈕
        self.nav_buttons = []
        nav_items = [
            ("📊 Dashboard", 1),
            ("✉️ Message", 2),
            ("✓ Tasks", 3),
            ("📅 Planning", 4),
            ("🌐 Global", 5),
            ("📈 Analytics", 6),
        ]

        for text, row in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                font=ctk.CTkFont(size=14),
                height=40,
                corner_radius=8,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w"
            )
            btn.grid(row=row, column=0, padx=20, pady=5, sticky="ew")
            self.nav_buttons.append(btn)

        # 外觀模式切換
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar,
            text="外觀模式:",
            font=ctk.CTkFont(size=12)
        )
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(20, 5))

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=(5, 20))

    def change_appearance_mode(self, new_mode: str):
        """切換外觀模式"""
        ctk.set_appearance_mode(new_mode.lower())

    def create_main_content(self):
        """建立主要內容區域"""
        # 主要內容容器
        self.main_container = ctk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # 設定網格權重
        self.main_container.grid_rowconfigure(2, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # 頁面標題
        self.create_header()

        # 新增任務區域
        self.create_input_section()

        # 任務列表區域（看板式佈局）
        self.create_task_board()

    def create_header(self):
        """建立頁面標題"""
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        title = ctk.CTkLabel(
            header_frame,
            text="Task Management",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="01 Division / 01 Department / A Team",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(side="left", padx=(15, 0))

    def create_input_section(self):
        """建立新增任務輸入區域"""
        input_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        input_frame.grid_columnconfigure(1, weight=1)

        # 標籤設定
        label_font = ctk.CTkFont(size=13, weight="bold")

        # 任務標題
        title_label = ctk.CTkLabel(input_frame, text="任務標題:", font=label_font)
        title_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="w")

        self.title_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="輸入任務標題...",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.title_entry.grid(row=0, column=1, padx=(0, 20), pady=(20, 10), sticky="ew")

        # 任務描述
        desc_label = ctk.CTkLabel(input_frame, text="描述:", font=label_font)
        desc_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nw")

        self.desc_text = ctk.CTkTextbox(
            input_frame,
            height=80,
            font=ctk.CTkFont(size=13)
        )
        self.desc_text.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")

        # 優先級和按鈕容器
        control_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        control_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")

        # 優先級選擇
        priority_label = ctk.CTkLabel(control_frame, text="優先級:", font=label_font)
        priority_label.pack(side="left", padx=(0, 10))

        self.priority_var = ctk.StringVar(value="low")

        priority_options = [
            ("低", "low"),
            ("中", "medium"),
            ("高", "high")
        ]

        for text, value in priority_options:
            radio = ctk.CTkRadioButton(
                control_frame,
                text=text,
                variable=self.priority_var,
                value=value,
                font=ctk.CTkFont(size=13)
            )
            radio.pack(side="left", padx=5)

        # 新增按鈕
        add_button = ctk.CTkButton(
            control_frame,
            text="➕ 新增任務",
            command=self.add_task_gui,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        add_button.pack(side="right", padx=5)

        # 清除按鈕
        clear_button = ctk.CTkButton(
            control_frame,
            text="🗑️ 清除",
            command=self.clear_inputs,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            fg_color="gray",
            hover_color="darkgray"
        )
        clear_button.pack(side="right", padx=5)

    def create_task_board(self):
        """建立任務看板（類似參考圖的佈局）"""
        # 看板容器
        board_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        board_frame.grid(row=2, column=0, sticky="nsew")

        # 設定網格權重
        for i in range(4):
            board_frame.grid_columnconfigure(i, weight=1, uniform="column")
        board_frame.grid_rowconfigure(1, weight=1)

        # 狀態列定義
        self.status_columns = {
            "pending": {"title": "待辦 (DRAFT)", "color": "#3498db", "frame": None, "tasks": []},
            "in_progress": {"title": "進行中 (IN PROGRESS)", "color": "#9b59b6", "frame": None, "tasks": []},
            "editing": {"title": "檢視中 (EDITING)", "color": "#e74c3c", "frame": None, "tasks": []},
            "completed": {"title": "已完成 (DONE)", "color": "#27ae60", "frame": None, "tasks": []}
        }

        # 建立各狀態列
        for col, (status, data) in enumerate(self.status_columns.items()):
            # 標題
            title_label = ctk.CTkLabel(
                board_frame,
                text=data["title"],
                font=ctk.CTkFont(size=14, weight="bold")
            )
            title_label.grid(row=0, column=col, padx=10, pady=(15, 10))

            # 任務卡片容器（可滾動）
            scrollable_frame = ctk.CTkScrollableFrame(
                board_frame,
                corner_radius=10,
                fg_color=("gray90", "gray20")
            )
            scrollable_frame.grid(row=1, column=col, padx=10, pady=(0, 15), sticky="nsew")

            data["frame"] = scrollable_frame

    def create_task_card(self, parent, task_data):
        """建立單個任務卡片"""
        task_id, title, description, priority, status, created_at = task_data

        # 顏色映射
        priority_colors = {
            "low": "#3498db",
            "medium": "#f39c12",
            "high": "#e74c3c"
        }

        # 卡片框架
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color=("white", "gray17"))
        card.pack(fill="x", padx=5, pady=8)

        # 卡片內容容器
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=12)

        # 任務標題
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 5))

        # 任務描述（截短）
        short_desc = description[:60] + "..." if len(description) > 60 else description
        if short_desc:
            desc_label = ctk.CTkLabel(
                content_frame,
                text=short_desc,
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w",
                wraplength=200
            )
            desc_label.pack(fill="x", pady=(0, 8))

        # 底部資訊列
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(fill="x")

        # 優先級標籤
        priority_text = {"low": "低", "medium": "中", "high": "高"}[priority]
        priority_badge = ctk.CTkLabel(
            info_frame,
            text=f"🎯 {priority_text}",
            font=ctk.CTkFont(size=11),
            text_color=priority_colors[priority]
        )
        priority_badge.pack(side="left")

        # 任務ID
        id_label = ctk.CTkLabel(
            info_frame,
            text=f"#{task_id}",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        id_label.pack(side="right")

        # 按鈕容器
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(8, 0))

        # 編輯狀態按鈕
        if status != "completed":
            complete_btn = ctk.CTkButton(
                button_frame,
                text="✓",
                width=30,
                height=28,
                command=lambda: self.complete_task_by_id(task_id),
                corner_radius=6,
                fg_color="green",
                hover_color="darkgreen"
            )
            complete_btn.pack(side="left", padx=(0, 5))

        if status == "pending":
            progress_btn = ctk.CTkButton(
                button_frame,
                text="▶",
                width=30,
                height=28,
                command=lambda: self.mark_in_progress_by_id(task_id),
                corner_radius=6,
                fg_color="orange",
                hover_color="darkorange"
            )
            progress_btn.pack(side="left", padx=(0, 5))

        # 刪除按鈕
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑",
            width=30,
            height=28,
            command=lambda: self.delete_task_by_id(task_id),
            corner_radius=6,
            fg_color="red",
            hover_color="darkred"
        )
        delete_btn.pack(side="left")

        # 建立時間
        time_label = ctk.CTkLabel(
            button_frame,
            text=created_at[:16] if created_at else "",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        time_label.pack(side="right")

    def add_task_gui(self):
        """新增任務的 GUI 處理"""
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", "end").strip()
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
        self.title_entry.delete(0, "end")
        self.desc_text.delete("1.0", "end")
        self.priority_var.set("low")

    def complete_task_by_id(self, task_id: int):
        """標記任務為完成"""
        if self.db_manager.update_task_status(task_id, "completed"):
            self.refresh_tasks()
            LogUtils.log_action(f"任務 {task_id} 標記為完成")
        else:
            messagebox.showerror("錯誤", "更新任務狀態失敗")

    def mark_in_progress_by_id(self, task_id: int):
        """標記任務為進行中"""
        if self.db_manager.update_task_status(task_id, "in_progress"):
            self.refresh_tasks()
            LogUtils.log_action(f"任務 {task_id} 標記為進行中")
        else:
            messagebox.showerror("錯誤", "更新任務狀態失敗")

    def delete_task_by_id(self, task_id: int):
        """刪除任務"""
        if messagebox.askyesno("確認", "確定要刪除這個任務嗎？"):
            if self.db_manager.delete_task(task_id):
                self.refresh_tasks()
                LogUtils.log_action(f"刪除任務 {task_id}")
                messagebox.showinfo("成功", "任務已刪除")
            else:
                messagebox.showerror("錯誤", "刪除任務失敗")

    def refresh_tasks(self):
        """重新整理任務列表"""
        # 清空所有狀態列的任務
        for status_data in self.status_columns.values():
            if status_data["frame"]:
                for widget in status_data["frame"].winfo_children():
                    widget.destroy()

        # 載入任務
        tasks = self.db_manager.get_tasks()

        for task in tasks:
            task_id, title, description, priority, status, created_at = task

            # 根據狀態分配到對應的列
            # 注意：資料庫中沒有 'editing' 狀態，我們將其視為一種展示需求
            # 實際應用中可以新增此狀態，或將某些任務映射到此狀態
            if status in self.status_columns:
                frame = self.status_columns[status]["frame"]
                if frame:
                    self.create_task_card(frame, task)

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
