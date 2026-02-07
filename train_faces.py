import cv2
import os
import pickle
import numpy as np

DATASET_DIR = "known_faces"
IMG_SIZE = (200, 200)

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "face_model.yml")
LABEL_PATH = os.path.join(MODEL_DIR, "label_map.pkl")
os.makedirs(MODEL_DIR, exist_ok=True)

def train_model():
    faces = []
    labels = []
    label_map = {}
    current_label = 0

    for name in os.listdir(DATASET_DIR):
        person_dir = os.path.join(DATASET_DIR, name)
        if not os.path.isdir(person_dir):
            continue

        label_map[current_label] = name

        for filename in os.listdir(person_dir):
            img_path = os.path.join(person_dir, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            img = cv2.resize(img, IMG_SIZE)
            faces.append(img)
            labels.append(current_label)

        current_label += 1

    if len(faces) == 0:
        print("No faces found. Skipping training.")
        return

    labels = np.array(labels, dtype=np.int32)

    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(faces, labels)
    model.save(MODEL_PATH)

    with open(LABEL_PATH, "wb") as f:
        pickle.dump(label_map, f)

    print("✅ Model retrained successfully.")

if __name__ == "__main__":
    train_model()
