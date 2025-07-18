import sqlite3

def is_hashed(pw):
    return pw.startswith("$2b$")

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Get all users
cur.execute("SELECT id, password FROM users")
users = cur.fetchall()

# Identify invalid users
for user_id, password in users:
    if not isinstance(password, str) or not is_hashed(password):
        print(f"Deleting user with ID: {user_id}, invalid password: {password}")
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))

conn.commit()
conn.close()
print("✅ Invalid users removed.")
