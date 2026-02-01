import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from train_faces import train_model

WATCH_DIR = "known_faces"

class FaceFolderHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        print("📁 Change detected. Retraining model...")
        train_model()

if __name__ == "__main__":
    event_handler = FaceFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()

    print("👀 Watching for face dataset changes... Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
