import sqlite3

# Connect to your database
conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Delete all users
cur.execute("DELETE FROM users")
conn.commit()
conn.close()

print("All users deleted.")
