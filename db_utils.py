import sqlite3
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(username, password, role):
    try:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        hashed_pw = hash_password(password)
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, hashed_pw, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_user(username, password, role):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ? AND role = ?", (username, role))
    row = cur.fetchone()
    conn.close()
    if row and check_password(password, row[0]):
        return True
    return False
