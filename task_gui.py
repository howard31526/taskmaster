import customtkinter as ctk
from tkinter import messagebox
from typing import Optional

from database import DatabaseManager
from utils import TaskUtils, ValidationUtils, LogUtils
from config import Config


class TaskGUI:
    """TaskMaster 桌面圖形介面 - CustomTkinter 版本"""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager(Config.get_database_path())
        self.logger = LogUtils.setup_logger("task_gui")

        # 設定 CustomTkinter 主題
        ctk.set_appearance_mode("dark")  # 深色模式
        ctk.set_default_color_theme("blue")  # 藍色主題

        self.window = ctk.CTk()
        self.window.title("TaskMaster - 任務管理系統")
        self.window.geometry("1000x750")

        # 定義配色方案
        self.colors = {
            'primary': '#1f6aa5',
            'secondary': '#144870',
            'success': '#2fa572',
            'warning': '#ff9800',
            'danger': '#e53935',
            'bg_dark': '#1a1a1a',
            'bg_card': '#2b2b2b',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'high': '#ff5252',
            'medium': '#ffa726',
            'low': '#66bb6a'
        }

        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self):
        """建立 UI 元件"""
        # 主容器
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # 標題區域
        title_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))

        title_label = ctk.CTkLabel(
            title_frame,
            text="📋 TaskMaster",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(side="left")

        # 新增任務區域
        self.create_input_section(main_container)

        # 任務列表區域
        self.create_task_list_section(main_container)

        # 操作按鈕區域
        self.create_button_section(main_container)

    def create_input_section(self, parent):
        """建立輸入區域"""
        input_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_card'], corner_radius=15)
        input_frame.pack(fill="x", pady=(0, 20))

        # 內部容器
        inner_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        inner_frame.pack(fill="x", padx=20, pady=20)

        # 標題
        section_title = ctk.CTkLabel(
            inner_frame,
            text="✨ 新增任務",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        section_title.pack(fill="x", pady=(0, 15))

        # 任務標題輸入
        title_label = ctk.CTkLabel(
            inner_frame,
            text="任務標題",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 5))

        self.title_entry = ctk.CTkEntry(
            inner_frame,
            height=40,
            font=ctk.CTkFont(size=13),
            placeholder_text="輸入任務標題..."
        )
        self.title_entry.pack(fill="x", pady=(0, 15))

        # 描述輸入
        desc_label = ctk.CTkLabel(
            inner_frame,
            text="描述",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        desc_label.pack(fill="x", pady=(0, 5))

        self.desc_text = ctk.CTkTextbox(
            inner_frame,
            height=100,
            font=ctk.CTkFont(size=13)
        )
        self.desc_text.pack(fill="x", pady=(0, 15))

        # 優先級與新增按鈕區域
        bottom_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        bottom_frame.pack(fill="x")

        # 優先級選擇
        priority_label = ctk.CTkLabel(
            bottom_frame,
            text="優先級",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        priority_label.pack(side="left", padx=(0, 15))

        self.priority_var = ctk.StringVar(value="low")
        priority_container = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        priority_container.pack(side="left", fill="x", expand=True)

        priorities = [
            ("高", "high", self.colors['high']),
            ("中", "medium", self.colors['medium']),
            ("低", "low", self.colors['low'])
        ]

        for text, value, color in priorities:
            radio = ctk.CTkRadioButton(
                priority_container,
                text=text,
                variable=self.priority_var,
                value=value,
                font=ctk.CTkFont(size=12),
                fg_color=color,
                hover_color=color
            )
            radio.pack(side="left", padx=(0, 15))

        # 新增按鈕
        add_button = ctk.CTkButton(
            bottom_frame,
            text="➕ 新增任務",
            command=self.add_task_gui,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['secondary'],
            corner_radius=10
        )
        add_button.pack(side="right")

    def create_task_list_section(self, parent):
        """建立任務列表區域（卡片式設計）"""
        list_container = ctk.CTkFrame(parent, fg_color=self.colors['bg_card'], corner_radius=15)
        list_container.pack(fill="both", expand=True, pady=(0, 20))

        # 標題
        header_frame = ctk.CTkFrame(list_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        list_title = ctk.CTkLabel(
            header_frame,
            text="📝 任務列表",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        list_title.pack(side="left")

        # 可滾動框架
        self.task_scroll = ctk.CTkScrollableFrame(
            list_container,
            fg_color="transparent",
            corner_radius=10
        )
        self.task_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def create_button_section(self, parent):
        """建立操作按鈕區域"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x")

        buttons = [
            ("✓ 標記完成", self.complete_task, self.colors['success']),
            ("⟳ 進行中", self.mark_in_progress, self.colors['warning']),
            ("🗑 刪除任務", self.delete_task_gui, self.colors['danger']),
        ]

        for text, command, color in buttons:
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=13),
                fg_color=color,
                hover_color=self._darken_color(color),
                corner_radius=10,
                width=140
            )
            btn.pack(side="left", padx=(0, 10))

        # 重新整理按鈕（靠右）
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 重新整理",
            command=self.refresh_tasks,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color=self.colors['primary'],
            hover_color=self.colors['secondary'],
            corner_radius=10,
            width=140
        )
        refresh_btn.pack(side="right")

    def _darken_color(self, hex_color: str) -> str:
        """將顏色變暗"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
        return f'#{r:02x}{g:02x}{b:02x}'

    def create_task_card(self, task):
        """建立單一任務卡片"""
        task_id, title, description, priority, status, created_at = task

        # 卡片容器
        card = ctk.CTkFrame(
            self.task_scroll,
            fg_color="#3a3a3a",
            corner_radius=12,
            border_width=2,
            border_color="transparent"
        )
        card.pack(fill="x", pady=8)

        # 使卡片可點擊
        card.bind("<Button-1>", lambda e: self.select_task(task_id, card))

        # 儲存任務 ID 到卡片
        card.task_id = task_id
        card.is_selected = False

        # 內容容器
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=12)

        # 頂部：標題與狀態
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 8))

        # 優先級指示器
        priority_colors = {
            'high': self.colors['high'],
            'medium': self.colors['medium'],
            'low': self.colors['low']
        }
        priority_indicator = ctk.CTkFrame(
            top_frame,
            width=4,
            height=20,
            fg_color=priority_colors.get(priority, self.colors['low']),
            corner_radius=2
        )
        priority_indicator.pack(side="left", padx=(0, 10))

        # 標題
        title_label = ctk.CTkLabel(
            top_frame,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True)

        # 狀態標籤
        status_text = {"pending": "待辦", "in_progress": "進行中", "completed": "已完成"}
        status_colors = {
            "pending": "#616161",
            "in_progress": "#fb8c00",
            "completed": "#43a047"
        }
        status_label = ctk.CTkLabel(
            top_frame,
            text=status_text.get(status, status),
            font=ctk.CTkFont(size=11),
            fg_color=status_colors.get(status, "#616161"),
            corner_radius=8,
            padx=12,
            pady=4
        )
        status_label.pack(side="right")

        # 描述
        if description:
            desc_label = ctk.CTkLabel(
                content_frame,
                text=description[:150] + "..." if len(description) > 150 else description,
                font=ctk.CTkFont(size=12),
                text_color=self.colors['text_secondary'],
                anchor="w",
                justify="left",
                wraplength=850
            )
            desc_label.pack(fill="x", pady=(0, 8))

        # 底部：優先級與時間
        bottom_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_frame.pack(fill="x")

        priority_text = {"low": "低", "medium": "中", "high": "高"}
        info_label = ctk.CTkLabel(
            bottom_frame,
            text=f"🔖 {priority_text.get(priority, priority)} | 📅 {created_at}",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        info_label.pack(side="left")

        task_id_label = ctk.CTkLabel(
            bottom_frame,
            text=f"ID: {task_id}",
            font=ctk.CTkFont(size=10),
            text_color=self.colors['text_secondary'],
            anchor="e"
        )
        task_id_label.pack(side="right")

        return card

    def select_task(self, task_id: int, card_widget):
        """選擇任務卡片"""
        # 取消所有其他卡片的選中狀態
        for widget in self.task_scroll.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and hasattr(widget, 'is_selected'):
                widget.configure(border_color="transparent")
                widget.is_selected = False

        # 選中當前卡片
        card_widget.configure(border_color=self.colors['primary'])
        card_widget.is_selected = True
        self.selected_task_id = task_id

    def add_task_gui(self):
        """新增任務的 GUI 處理"""
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", "end-1c").strip()
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

    def get_selected_task_id(self) -> Optional[int]:
        """取得選中任務的 ID"""
        return getattr(self, 'selected_task_id', None)

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
        # 清空現有卡片
        for widget in self.task_scroll.winfo_children():
            widget.destroy()

        # 重置選中狀態
        self.selected_task_id = None

        # 載入任務並建立卡片
        tasks = self.db_manager.get_tasks()
        if not tasks:
            # 顯示空狀態
            empty_label = ctk.CTkLabel(
                self.task_scroll,
                text="📭 目前沒有任務\n\n點擊上方「新增任務」開始管理你的工作！",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_secondary'],
                justify="center"
            )
            empty_label.pack(expand=True, pady=50)
        else:
            for task in tasks:
                self.create_task_card(task)

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
