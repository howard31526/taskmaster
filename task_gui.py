import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, List
from datetime import datetime

from database import DatabaseManager
from utils import TaskUtils, ValidationUtils, LogUtils
from config import Config


class TaskGUI:
    """TaskMaster 現代化圖形介面 - 使用 CustomTkinter"""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager(Config.get_database_path())
        self.logger = LogUtils.setup_logger("task_gui")

        # 設定 CustomTkinter 主題
        ctk.set_appearance_mode("dark")  # 預設為深色模式
        ctk.set_default_color_theme("blue")

        # 建立主視窗
        self.window = ctk.CTk()
        self.window.title("TaskMaster - 任務管理系統")
        self.window.geometry("1400x800")

        # 儲存任務卡片參考
        self.task_cards: Dict[str, List] = {
            "pending": [],
            "in_progress": [],
            "editing": [],
            "completed": []
        }

        # 建立 UI
        self.create_main_layout()
        self.refresh_tasks()

    def create_main_layout(self):
        """建立主要版面配置"""
        # 主容器 - 水平分割
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        # 左側導航欄
        self.create_sidebar()

        # 主要內容區
        self.create_main_content()

    def create_sidebar(self):
        """建立左側導航側邊欄"""
        sidebar = ctk.CTkFrame(self.window, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(8, weight=1)  # 讓最後一個元素推到底部

        # 標題
        title_label = ctk.CTkLabel(
            sidebar,
            text="TaskMaster",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # 導航選項
        nav_options = [
            ("📊", "Dashboard"),
            ("💬", "Message"),
            ("✓", "Tasks"),
            ("📅", "Planning"),
            ("🌐", "Global"),
            ("📈", "Analytics"),
        ]

        for idx, (icon, label) in enumerate(nav_options, start=1):
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icon}  {label}",
                font=ctk.CTkFont(size=14),
                anchor="w",
                fg_color="transparent",
                hover_color=("#3B8ED0", "#1F6AA5"),
                height=40,
                command=lambda l=label: self.on_nav_click(l)
            )
            btn.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")

        # 外觀模式選擇器（底部）
        appearance_label = ctk.CTkLabel(
            sidebar,
            text="外觀模式:",
            font=ctk.CTkFont(size=12)
        )
        appearance_label.grid(row=9, column=0, padx=20, pady=(10, 5))

        self.appearance_mode = ctk.CTkSegmentedButton(
            sidebar,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode.set("Dark")
        self.appearance_mode.grid(row=10, column=0, padx=20, pady=(0, 20))

    def create_main_content(self):
        """建立主要內容區域"""
        # 主容器
        main_frame = ctk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # 標題列
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        title = ctk.CTkLabel(
            header,
            text="Task Management",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(side="left")

        # 新增任務區域
        self.create_add_task_section(main_frame)

        # 看板式任務區域
        self.create_kanban_board(main_frame)

    def create_add_task_section(self, parent):
        """建立新增任務區域"""
        add_frame = ctk.CTkFrame(parent)
        add_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        add_frame.grid_columnconfigure(0, weight=1)

        # 任務標題輸入
        self.title_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="輸入任務標題...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.title_entry.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # 任務描述輸入
        self.desc_textbox = ctk.CTkTextbox(
            add_frame,
            height=80,
            font=ctk.CTkFont(size=13)
        )
        self.desc_textbox.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 10))

        # 優先級選擇
        priority_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        priority_frame.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 10))

        ctk.CTkLabel(
            priority_frame,
            text="優先級:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 10))

        self.priority_var = ctk.StringVar(value="low")

        priorities = [("低", "low"), ("中", "medium"), ("高", "high")]
        for text, value in priorities:
            radio = ctk.CTkRadioButton(
                priority_frame,
                text=text,
                variable=self.priority_var,
                value=value,
                font=ctk.CTkFont(size=13)
            )
            radio.pack(side="left", padx=5)

        # 按鈕區域
        button_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        button_frame.grid(row=2, column=1, columnspan=2, sticky="e", padx=10, pady=(0, 10))

        ctk.CTkButton(
            button_frame,
            text="清除",
            width=100,
            command=self.clear_inputs,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="新增任務",
            width=120,
            command=self.add_task_gui
        ).pack(side="left", padx=5)

    def create_kanban_board(self, parent):
        """建立看板式任務佈局"""
        kanban_frame = ctk.CTkFrame(parent, fg_color="transparent")
        kanban_frame.grid(row=2, column=0, sticky="nsew")

        # 配置四欄
        for i in range(4):
            kanban_frame.grid_columnconfigure(i, weight=1, uniform="column")
        kanban_frame.grid_rowconfigure(1, weight=1)

        # 定義看板欄位
        columns = [
            ("DRAFT", "待辦", "pending", "#FF6B9D"),
            ("IN PROGRESS", "進行中", "in_progress", "#4A90E2"),
            ("EDITING", "檢視中", "editing", "#9B59B6"),
            ("DONE", "已完成", "completed", "#2ECC71")
        ]

        # 建立每一欄
        for idx, (title, subtitle, status_key, color) in enumerate(columns):
            self.create_kanban_column(kanban_frame, idx, title, subtitle, status_key, color)

    def create_kanban_column(self, parent, col_idx, title, subtitle, status_key, color):
        """建立單一看板欄位"""
        column_frame = ctk.CTkFrame(parent)
        column_frame.grid(row=0, column=col_idx, rowspan=2, sticky="nsew", padx=5)
        column_frame.grid_rowconfigure(1, weight=1)
        column_frame.grid_columnconfigure(0, weight=1)

        # 欄位標題
        header = ctk.CTkFrame(column_frame, fg_color=color, corner_radius=10)
        header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(pady=10)

        ctk.CTkLabel(
            header,
            text=subtitle,
            font=ctk.CTkFont(size=11),
            text_color="white"
        ).pack(pady=(0, 10))

        # 可滾動的任務卡片區域
        scrollable = ctk.CTkScrollableFrame(column_frame, fg_color="transparent")
        scrollable.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        scrollable.grid_columnconfigure(0, weight=1)

        # 儲存滾動框架參考
        setattr(self, f"{status_key}_frame", scrollable)

    def create_task_card(self, parent, task_data, row_idx):
        """建立任務卡片"""
        task_id, title, description, priority, status, created_at = task_data

        # 卡片主框架
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=row_idx, column=0, sticky="ew", pady=5)
        card.grid_columnconfigure(0, weight=1)

        # 標題
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))

        # 描述
        if description:
            short_desc = description[:50] + "..." if len(description) > 50 else description
            desc_label = ctk.CTkLabel(
                card,
                text=short_desc,
                font=ctk.CTkFont(size=11),
                anchor="w",
                text_color="gray"
            )
            desc_label.grid(row=1, column=0, sticky="ew", padx=15, pady=5)

        # 優先級標籤
        priority_colors = {
            "low": ("#95E1D3", "#2D6A5D"),
            "medium": ("#FFC93C", "#8B6914"),
            "high": ("#FF6B9D", "#8B3A5A")
        }
        priority_text = {"low": "低", "medium": "中", "high": "高"}

        bg_color, text_color = priority_colors.get(priority, ("#95E1D3", "#2D6A5D"))

        priority_label = ctk.CTkLabel(
            card,
            text=f"優先級: {priority_text.get(priority, priority)}",
            font=ctk.CTkFont(size=10),
            fg_color=bg_color,
            text_color=text_color,
            corner_radius=5,
            padx=10,
            pady=3
        )
        priority_label.grid(row=2, column=0, sticky="w", padx=15, pady=5)

        # 操作按鈕區域
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 10))

        # 根據狀態顯示不同按鈕
        if status == "pending":
            ctk.CTkButton(
                button_frame,
                text="▶ 開始",
                width=70,
                height=25,
                font=ctk.CTkFont(size=11),
                command=lambda: self.mark_in_progress(task_id)
            ).pack(side="left", padx=5)
        elif status == "in_progress":
            ctk.CTkButton(
                button_frame,
                text="✓ 完成",
                width=70,
                height=25,
                font=ctk.CTkFont(size=11),
                fg_color="green",
                hover_color="darkgreen",
                command=lambda: self.complete_task(task_id)
            ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="🗑 刪除",
            width=70,
            height=25,
            font=ctk.CTkFont(size=11),
            fg_color="red",
            hover_color="darkred",
            command=lambda: self.delete_task_gui(task_id)
        ).pack(side="left", padx=5)

        # 任務資訊
        info_label = ctk.CTkLabel(
            card,
            text=f"ID: {task_id} | 建立於: {created_at[:16]}",
            font=ctk.CTkFont(size=9),
            text_color="gray",
            anchor="w"
        )
        info_label.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 10))

        return card

    def add_task_gui(self):
        """新增任務的 GUI 處理"""
        title = self.title_entry.get().strip()
        description = self.desc_textbox.get("1.0", "end-1c").strip()
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
        self.desc_textbox.delete("1.0", "end")
        self.priority_var.set("low")

    def complete_task(self, task_id: int):
        """標記任務為完成"""
        if self.db_manager.update_task_status(task_id, "completed"):
            self.refresh_tasks()
            LogUtils.log_action(f"任務 {task_id} 標記為完成")
            messagebox.showinfo("成功", "任務已標記為完成")
        else:
            messagebox.showerror("錯誤", "更新任務狀態失敗")

    def mark_in_progress(self, task_id: int):
        """標記任務為進行中"""
        if self.db_manager.update_task_status(task_id, "in_progress"):
            self.refresh_tasks()
            LogUtils.log_action(f"任務 {task_id} 標記為進行中")
            messagebox.showinfo("成功", "任務已標記為進行中")
        else:
            messagebox.showerror("錯誤", "更新任務狀態失敗")

    def delete_task_gui(self, task_id: int):
        """刪除任務的 GUI 處理"""
        if messagebox.askyesno("確認", "確定要刪除這個任務嗎？"):
            if self.db_manager.delete_task(task_id):
                self.refresh_tasks()
                LogUtils.log_action(f"刪除任務 {task_id}")
                messagebox.showinfo("成功", "任務已刪除")
            else:
                messagebox.showerror("錯誤", "刪除任務失敗")

    def refresh_tasks(self):
        """重新整理任務列表"""
        # 清空現有卡片
        for status_key in ["pending", "in_progress", "editing", "completed"]:
            frame = getattr(self, f"{status_key}_frame", None)
            if frame:
                for widget in frame.winfo_children():
                    widget.destroy()

        # 載入任務並分類顯示
        tasks = self.db_manager.get_tasks()
        task_counts = {"pending": 0, "in_progress": 0, "editing": 0, "completed": 0}

        for task in tasks:
            task_id, title, description, priority, status, created_at = task

            # 映射狀態到看板欄位
            status_key = status if status in task_counts else "pending"
            frame = getattr(self, f"{status_key}_frame", None)

            if frame:
                self.create_task_card(frame, task, task_counts[status_key])
                task_counts[status_key] += 1

    def on_nav_click(self, nav_label: str):
        """處理導航點擊事件"""
        LogUtils.log_action(f"導航到: {nav_label}")
        # 這裡可以實作不同頁面的切換
        if nav_label == "Tasks":
            self.refresh_tasks()

    def change_appearance_mode(self, mode: str):
        """切換外觀模式"""
        ctk.set_appearance_mode(mode.lower())
        LogUtils.log_action(f"切換外觀模式: {mode}")

    def run(self):
        """啟動 GUI"""
        try:
            LogUtils.log_action("啟動 TaskGUI (CustomTkinter)")
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
