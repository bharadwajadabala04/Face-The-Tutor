# backend/notify_tutor.py

# In-memory list to store alerts (you could switch this to DB later if needed)
alerts = []

def notify_tutor(student_id):
    """
    Called when a student is inactive for too long.
    Adds an alert message to the tutor's alert list.
    """
    message = f"⚠️ Student '{student_id}' has been inactive for 10 minutes."
    if message not in alerts:  # Avoid duplicate alerts
        alerts.append(message)

def get_alerts():
    """
    Returns all stored alert messages.
    """
    return alerts

def clear_alerts():
    """
    Clears all current alert messages (can be used by tutor).
    """
    alerts.clear()
