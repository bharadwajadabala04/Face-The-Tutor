from flask import Flask, render_template, request, redirect, url_for, session, Response
import sqlite3
import uuid
import bcrypt
from models.camera import gen_frames
from database import init_db
from backend.notification import get_notifications_for_tutor, mark_notifications_seen

app = Flask(__name__)
app.secret_key = "your_secret_key"

init_db()

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT id, username, password, role FROM users WHERE username=? AND role=?", (username, role))
        user = cur.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode() if isinstance(user[2], str) else user[2]):
            session["user_id"] = user[0]
            session["user"] = username
            session["role"] = role
            return redirect(url_for("dashboard") if role == "tutor" else "student_dashboard")
        else:
            return render_template("login.html", error="Invalid credentials or role")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if session.get("role") != "tutor":
        return redirect(url_for("login"))
    tutor_id = session.get("user_id")
    tutor_username = session.get("user")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT session_code FROM sessions WHERE tutor_id=?", (tutor_id,))
    row = cur.fetchone()
    session_code = row[0] if row else str(uuid.uuid4())[:8]

    if not row:
        cur.execute("INSERT INTO sessions (tutor_id, session_code) VALUES (?, ?)", (tutor_id, session_code))
        conn.commit()
    conn.close()

    notifications = get_notifications_for_tutor(tutor_username)
    mark_notifications_seen(tutor_username)
    join_link = url_for("student_join", session_code=session_code, _external=True)

    return render_template("dashboard.html", join_link=join_link, tutor=tutor_username, notifications=notifications)

@app.route("/student_dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    student_username = session["user"]
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT message, timestamp, seen FROM notifications WHERE student_id=(SELECT id FROM users WHERE username=?) ORDER BY timestamp DESC", (student_username,))
    rows = cur.fetchall()
    conn.close()

    notifications = [{"message": r[0], "timestamp": r[1], "seen": bool(r[2])} for r in rows]

    return render_template("student_dashboard.html", username=student_username, notifications=notifications)

@app.route("/student_monitor")
def student_monitor():
    if session.get("role") != "student":
        return redirect(url_for("login"))
    return render_template("student_monitor.html", username=session["user"])

@app.route("/video_feed/<student_username>")
def video_feed(student_username):
    if "user" not in session:
        return redirect(url_for("login"))
    return Response(gen_frames(student_username), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/join/<session_code>")
def student_join(session_code):
    if session.get("role") != "student":
        return redirect(url_for("login"))

    student_id = session["user_id"]
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM sessions WHERE session_code=?", (session_code,))
    row = cur.fetchone()

    if not row:
        return "Invalid session link"
    session_id = row[0]
    cur.execute("SELECT * FROM session_participants WHERE session_id=? AND student_id=?", (session_id, student_id))
    if not cur.fetchone():
        cur.execute("INSERT INTO session_participants (session_id, student_id) VALUES (?, ?)", (session_id, student_id))
        conn.commit()
    conn.close()
    return redirect(url_for("student_dashboard"))

@app.route("/monitor")
def monitor():
    if session.get("role") != "tutor":
        return redirect(url_for("login"))
    return render_template("monitor.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
