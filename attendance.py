import csv
import os
from datetime import datetime

FILE_NAME = "attendance.csv"

def mark_attendance(name):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    already_marked = False

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[0] == name and row[1] == today:
                    already_marked = True
                    break

    if not already_marked:
        with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([name, today, time_str])
        print(f"✅ Attendance marked for {name}")
    else:
        print(f"⚠️ {name} already marked today")
