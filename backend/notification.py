import sqlite3
from datetime import datetime

DB_NAME = "database.db"

# ✅ Send a notification to a student (from tutor)
def send_notification_to_student(student_username, message):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username=? AND role='student'", (student_username,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False

    student_id = row[0]
    cur.execute("""
        INSERT INTO notifications (student_id, message, timestamp, seen)
        VALUES (?, ?, ?, 0)
    """, (student_id, message, datetime.now()))

    conn.commit()
    conn.close()
    return True

# ✅ Get all notifications for a tutor (via their session's students)
def get_notifications_for_tutor(tutor_username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get tutor ID
    cur.execute("SELECT id FROM users WHERE username=? AND role='tutor'", (tutor_username,))
    tutor_row = cur.fetchone()
    if not tutor_row:
        conn.close()
        return []

    tutor_id = tutor_row[0]

    # Get sessions created by tutor
    cur.execute("SELECT id FROM sessions WHERE tutor_id=?", (tutor_id,))
    session_ids = [row[0] for row in cur.fetchall()]

    # Get students in those sessions
    student_ids = []
    for sid in session_ids:
        cur.execute("SELECT student_id FROM session_participants WHERE session_id=?", (sid,))
        student_ids.extend([row[0] for row in cur.fetchall()])

    if not student_ids:
        conn.close()
        return []

    # Fetch notifications for those students
    format_ids = ','.join('?' * len(student_ids))
    cur.execute(f"""
        SELECT users.username, notifications.message, notifications.timestamp, notifications.seen
        FROM notifications
        JOIN users ON users.id = notifications.student_id
        WHERE notifications.student_id IN ({format_ids})
        ORDER BY notifications.timestamp DESC
    """, student_ids)

    notifications = cur.fetchall()
    conn.close()

    return [
        {
            "student": row[0],
            "message": row[1],
            "timestamp": row[2],
            "seen": bool(row[3])
        }
        for row in notifications
    ]

# ✅ Mark all tutor-related notifications as seen
def mark_notifications_seen(tutor_username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username=? AND role='tutor'", (tutor_username,))
    tutor_row = cur.fetchone()
    if not tutor_row:
        conn.close()
        return

    tutor_id = tutor_row[0]

    # Get student IDs in tutor’s sessions
    cur.execute("SELECT id FROM sessions WHERE tutor_id=?", (tutor_id,))
    session_ids = [row[0] for row in cur.fetchall()]

    student_ids = []
    for sid in session_ids:
        cur.execute("SELECT student_id FROM session_participants WHERE session_id=?", (sid,))
        student_ids.extend([row[0] for row in cur.fetchall()])

    if student_ids:
        format_ids = ','.join('?' * len(student_ids))
        cur.execute(f"""
            UPDATE notifications
            SET seen=1
            WHERE student_id IN ({format_ids})
        """, student_ids)

    conn.commit()
    conn.close()

# ✅ Get notifications for a student
def get_notifications_for_student(student_username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username=? AND role='student'", (student_username,))
    student_row = cur.fetchone()
    if not student_row:
        conn.close()
        return []

    student_id = student_row[0]

    cur.execute("""
        SELECT message, timestamp FROM notifications
        WHERE student_id=?
        ORDER BY timestamp DESC
    """, (student_id,))

    notifications = cur.fetchall()
    conn.close()

    return [
        {
            "message": row[0],
            "timestamp": row[1]
        }
        for row in notifications
    ]
