#!/usr/bin/env python3
"""
TaskMaster 資料庫檢查工具
用於檢視、管理和維護 tasks.db 資料庫
"""

import sqlite3
import sys
import datetime
from typing import List, Dict, Any, Optional

class DatabaseChecker:
    """資料庫檢查和管理工具"""

    def __init__(self, db_path: str = 'tasks.db'):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """取得資料庫連線"""
        return sqlite3.connect(self.db_path)

    def check_connection(self) -> bool:
        """檢查資料庫連線是否正常"""
        try:
            conn = self.get_connection()
            conn.execute('SELECT 1')
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 資料庫連線失敗: {e}")
            return False

    def show_table_info(self) -> None:
        """顯示表格結構資訊"""
        print("\n" + "="*50)
        print("📋 表格結構資訊")
        print("="*50)

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 取得所有表格
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                print(f"\n📊 表格: {table_name}")
                print("-" * 30)

                # 取得表格結構
                cursor.execute(f'PRAGMA table_info({table_name})')
                columns = cursor.fetchall()

                for col in columns:
                    col_id, name, col_type, not_null, default, pk = col
                    pk_info = "🔑 PRIMARY KEY" if pk else ""
                    null_info = "NOT NULL" if not_null else "NULL"
                    default_info = f"DEFAULT: {default}" if default else ""

                    print(f"  {name:<15} {col_type:<10} {null_info:<8} {pk_info} {default_info}")

            conn.close()

        except Exception as e:
            print(f"❌ 無法取得表格資訊: {e}")

    def show_statistics(self) -> None:
        """顯示資料庫統計資訊"""
        print("\n" + "="*50)
        print("📊 資料庫統計")
        print("="*50)

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 總任務數
            cursor.execute("SELECT COUNT(*) FROM tasks")
            total_tasks = cursor.fetchone()[0]

            # 依狀態統計
            cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
            status_counts = cursor.fetchall()

            # 依優先級統計
            cursor.execute("SELECT priority, COUNT(*) FROM tasks GROUP BY priority")
            priority_counts = cursor.fetchall()

            # 最近建立的任務
            cursor.execute("SELECT created_at FROM tasks ORDER BY created_at DESC LIMIT 1")
            latest_task = cursor.fetchone()

            print(f"📈 總任務數: {total_tasks}")

            print("\n📋 狀態分布:")
            for status, count in status_counts:
                emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(status, "❓")
                print(f"  {emoji} {status:<12}: {count}")

            print("\n🎯 優先級分布:")
            for priority, count in priority_counts:
                emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                print(f"  {emoji} {priority:<8}: {count}")

            if latest_task:
                print(f"\n🕒 最近活動: {latest_task[0]}")

            conn.close()

        except Exception as e:
            print(f"❌ 無法取得統計資訊: {e}")

    def show_all_tasks(self, limit: int = 10) -> None:
        """顯示所有任務"""
        print("\n" + "="*80)
        print(f"📝 任務列表 (最近 {limit} 筆)")
        print("="*80)

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, title, description, priority, status, created_at
                FROM tasks
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

            tasks = cursor.fetchall()

            if not tasks:
                print("📭 無任務資料")
                return

            print(f"{'ID':<4} {'標題':<20} {'描述':<30} {'優先級':<8} {'狀態':<12} {'建立時間':<20}")
            print("-" * 80)

            for task in tasks:
                task_id, title, desc, priority, status, created_at = task

                # 截斷長文字
                title = (title[:17] + "...") if len(title) > 20 else title
                desc = (desc[:27] + "...") if desc and len(desc) > 30 else (desc or "-")

                # 狀態emoji
                status_emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(status, "❓")
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")

                print(f"{task_id:<4} {title:<20} {desc:<30} {priority_emoji}{priority:<7} {status_emoji}{status:<11} {created_at[:19]}")

            conn.close()

        except Exception as e:
            print(f"❌ 無法取得任務列表: {e}")

    def search_tasks(self, keyword: str) -> None:
        """搜尋任務"""
        print(f"\n🔍 搜尋結果: '{keyword}'")
        print("="*50)

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, title, description, priority, status
                FROM tasks
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
            """, (f'%{keyword}%', f'%{keyword}%'))

            tasks = cursor.fetchall()

            if not tasks:
                print("🚫 找不到相符的任務")
                return

            for task in tasks:
                task_id, title, desc, priority, status = task
                print(f"📌 ID {task_id}: {title}")
                print(f"   📄 {desc or '(無描述)'}")
                print(f"   🎯 優先級: {priority} | 狀態: {status}")
                print()

            conn.close()

        except Exception as e:
            print(f"❌ 搜尋失敗: {e}")

    def verify_data_integrity(self) -> None:
        """驗證資料完整性"""
        print("\n" + "="*50)
        print("🔍 資料完整性檢查")
        print("="*50)

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            issues = []

            # 檢查空標題
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE title IS NULL OR title = ''")
            empty_titles = cursor.fetchone()[0]
            if empty_titles > 0:
                issues.append(f"⚠️  {empty_titles} 個任務標題為空")

            # 檢查無效狀態
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status NOT IN ('pending', 'in_progress', 'completed')")
            invalid_status = cursor.fetchone()[0]
            if invalid_status > 0:
                issues.append(f"⚠️  {invalid_status} 個任務狀態無效")

            # 檢查無效優先級
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE priority NOT IN ('low', 'medium', 'high')")
            invalid_priority = cursor.fetchone()[0]
            if invalid_priority > 0:
                issues.append(f"⚠️  {invalid_priority} 個任務優先級無效")

            # 檢查日期格式
            cursor.execute("SELECT id, created_at FROM tasks")
            all_tasks = cursor.fetchall()
            invalid_dates = 0
            for task_id, created_at in all_tasks:
                try:
                    datetime.datetime.fromisoformat(created_at.replace(' ', 'T'))
                except:
                    invalid_dates += 1

            if invalid_dates > 0:
                issues.append(f"⚠️  {invalid_dates} 個任務日期格式無效")

            if issues:
                print("發現以下問題:")
                for issue in issues:
                    print(f"  {issue}")
            else:
                print("✅ 資料完整性良好，無發現問題")

            conn.close()

        except Exception as e:
            print(f"❌ 資料完整性檢查失敗: {e}")

    def cleanup_database(self) -> None:
        """清理資料庫（移除無效資料）"""
        print("\n" + "="*50)
        print("🧹 資料庫清理")
        print("="*50)

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 移除空標題的任務
            cursor.execute("DELETE FROM tasks WHERE title IS NULL OR title = ''")
            deleted_empty = cursor.rowcount

            # 修正無效狀態
            cursor.execute("UPDATE tasks SET status = 'pending' WHERE status NOT IN ('pending', 'in_progress', 'completed')")
            fixed_status = cursor.rowcount

            # 修正無效優先級
            cursor.execute("UPDATE tasks SET priority = 'medium' WHERE priority NOT IN ('low', 'medium', 'high')")
            fixed_priority = cursor.rowcount

            conn.commit()

            print(f"✅ 清理完成:")
            print(f"  📭 移除空標題任務: {deleted_empty}")
            print(f"  🔄 修正無效狀態: {fixed_status}")
            print(f"  🎯 修正無效優先級: {fixed_priority}")

            conn.close()

        except Exception as e:
            print(f"❌ 資料庫清理失敗: {e}")

def show_help():
    """顯示使用說明"""
    print("""
TaskMaster 資料庫檢查工具

用法: python check_db.py [選項]

選項:
  info          顯示表格結構資訊
  stats         顯示統計資訊
  list [N]      顯示任務列表 (預設10筆)
  search <關鍵字> 搜尋任務
  check         驗證資料完整性
  cleanup       清理無效資料
  all           執行完整檢查 (預設)
  help          顯示此說明

範例:
  python check_db.py
  python check_db.py stats
  python check_db.py list 20
  python check_db.py search "重要"
    """)

def main():
    """主程式"""
    checker = DatabaseChecker()

    # 檢查連線
    if not checker.check_connection():
        sys.exit(1)

    print("🗃️  TaskMaster 資料庫檢查工具")
    print(f"📁 資料庫路徑: {checker.db_path}")

    if len(sys.argv) == 1:
        # 預設執行完整檢查
        checker.show_table_info()
        checker.show_statistics()
        checker.show_all_tasks()
        checker.verify_data_integrity()
    else:
        command = sys.argv[1].lower()

        if command == "help":
            show_help()
        elif command == "info":
            checker.show_table_info()
        elif command == "stats":
            checker.show_statistics()
        elif command == "list":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            checker.show_all_tasks(limit)
        elif command == "search":
            if len(sys.argv) < 3:
                print("❌ 請提供搜尋關鍵字")
                sys.exit(1)
            keyword = sys.argv[2]
            checker.search_tasks(keyword)
        elif command == "check":
            checker.verify_data_integrity()
        elif command == "cleanup":
            checker.cleanup_database()
        elif command == "all":
            checker.show_table_info()
            checker.show_statistics()
            checker.show_all_tasks()
            checker.verify_data_integrity()
        else:
            print(f"❌ 未知命令: {command}")
            show_help()
            sys.exit(1)

if __name__ == "__main__":
    main()