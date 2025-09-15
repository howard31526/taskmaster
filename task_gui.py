import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Another GUI implementation (conflicting with main.py)
class TaskManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager v2")
        
        # Different implementation than main.py
        self.setup_widgets()
        
    def setup_widgets(self):
        # Frame for input
        input_frame = ttk.Frame(self.master)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Task Title:").grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.title_var, width=40).grid(row=0, column=1)
        
        ttk.Button(input_frame, text="Add", command=self.add_task).grid(row=0, column=2)
        
        # Task list
        self.tree = ttk.Treeview(self.master, columns=("title", "status"), show="tree headings")
        self.tree.heading("#0", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
    def add_task(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Please enter a task title")
            return
            
        # Direct database access (bad!)
        conn = sqlite3.connect("tasks.db")
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()
        
        self.title_var.set("")
        self.refresh_list()
        
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = sqlite3.connect("tasks.db")
        cursor = conn.execute("SELECT id, title, status FROM tasks")
        
        for row in cursor:
            self.tree.insert("", tk.END, text=row[0], values=(row[1], row[2]))
            
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()