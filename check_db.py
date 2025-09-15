import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

print('=== 表格結構 ===')
cursor.execute('PRAGMA table_info(tasks)')
columns = cursor.fetchall()
for col in columns:
    pk = 'PRIMARY KEY' if col[5] else ''
    print(f'{col[1]:15} {col[2]:10} {pk}')

conn.close()