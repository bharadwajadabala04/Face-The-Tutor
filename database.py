# database.py

import sqlite3

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # --- Users Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # --- Sessions Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_id INTEGER NOT NULL,
            session_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(tutor_id) REFERENCES users(id)
        )
    """)

    # --- Session Participants Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS session_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id),
            FOREIGN KEY(student_id) REFERENCES users(id)
        )
    """)

    # --- Notifications Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            message TEXT,
            timestamp TEXT,
            seen INTEGER DEFAULT 0,
            FOREIGN KEY(student_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
