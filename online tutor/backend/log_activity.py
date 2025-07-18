import csv
from datetime import datetime
import os

LOG_PATH = "backend/logs/activity_log.csv"

# Ensure folder exists
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log_event(face_id, event_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([face_id, timestamp, event_type])

