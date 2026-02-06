import threading
import time
import webbrowser
import auto_train
import app
import recognize_faces

def start_dashboard():
    app.run_dashboard()

def start_recognition():
    recognize_faces.run_recognition()

if __name__ == "__main__":
    print("🚀 Starting Attendance System...")

    auto_train.run_training()
    time.sleep(2)

    t1 = threading.Thread(target=start_dashboard, daemon=True)
    t1.start()

    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000")

    start_recognition()