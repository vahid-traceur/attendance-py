from flask import Flask, render_template, send_file
import csv
from datetime import datetime
import os

app = Flask(__name__)
FILE_NAME = "attendance.csv"

def read_attendance():
    records = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    records.append(row)
    return records

@app.route("/")
def dashboard():
    records = read_attendance()
    today = datetime.now().strftime("%Y-%m-%d")
    today_records = [r for r in records if r[1] == today]
    return render_template("dashboard.html",
                           today_records=today_records,
                           all_records=records)

@app.route("/download")
def download():
    return send_file(FILE_NAME, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
