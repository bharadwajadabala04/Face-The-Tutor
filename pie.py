import sqlite3
conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute("SELECT username, role FROM users")
print(cur.fetchall())
conn.close()
