import os
import pandas as pd
from datetime import datetime, timedelta

FILE_PATH = "data/attendance.xlsx"
COOLDOWN_SECONDS = 30  # جلوگیری از ثبت تکراری

os.makedirs("data", exist_ok=True)


def _init_file():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["Name", "Date", "Time", "State"])
        df.to_excel(FILE_PATH, index=False)


def get_last_state(name):
    _init_file()
    df = pd.read_excel(FILE_PATH)
    user_rows = df[df["Name"] == name]
    if user_rows.empty:
        return None, None
    last_row = user_rows.iloc[-1]
    last_time = datetime.strptime(
        f"{last_row['Date']} {last_row['Time']}", "%Y-%m-%d %H:%M:%S"
    )
    return last_row["State"], last_time


def log_attendance(name):
    _init_file()
    now = datetime.now()

    last_state, last_time = get_last_state(name)

    if last_time and (now - last_time).total_seconds() < COOLDOWN_SECONDS:
        print(f"⏳ Skipped duplicate log for {name}")
        return None

    new_state = "IN" if last_state != "IN" else "OUT"

    new_row = {
        "Name": name,
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
        "State": new_state,
    }

    df = pd.read_excel(FILE_PATH)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(FILE_PATH, index=False)

    print(f"✅ {name} → {new_state}")
    return new_state
