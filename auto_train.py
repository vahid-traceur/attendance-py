import os
import hashlib
import subprocess
import sys

DATASET_DIR = "known_faces"
HASH_FILE = "dataset.hash"


def hash_dataset():
    h = hashlib.md5()
    for root, _, files in os.walk(DATASET_DIR):
        for f in sorted(files):
            path = os.path.join(root, f)
            h.update(path.encode())
            h.update(str(os.path.getmtime(path)).encode())
    return h.hexdigest()


def dataset_changed():
    new_hash = hash_dataset()
    if not os.path.exists(HASH_FILE):
        open(HASH_FILE, "w").write(new_hash)
        return True

    old_hash = open(HASH_FILE).read()
    if old_hash != new_hash:
        open(HASH_FILE, "w").write(new_hash)
        return True

    return False


def run_training():
    if dataset_changed():
        print("📸 Dataset changed — retraining model...")
        subprocess.call([sys.executable, "train_faces.py"])
    else:
        print("✅ Dataset unchanged — skipping training")
