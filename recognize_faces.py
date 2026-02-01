import cv2
import pickle
import numpy as np
from datetime import datetime
from attendance import mark_attendance

IMG_SIZE = (200, 200)
CONFIDENCE_THRESHOLD = 70  # هرچه کمتر = سختگیرانه‌تر

model = cv2.face.LBPHFaceRecognizer_create()
model.read("face_model.yml")

with open("label_map.pkl", "rb") as f:
    label_map = pickle.load(f)

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, IMG_SIZE)

        label_id, confidence = model.predict(face_img)

        if confidence < CONFIDENCE_THRESHOLD:
            name = label_map[label_id]
            status = "Marked"
            mark_attendance(name)
            color = (0, 255, 0)
        else:
            name = "Unknown"
            status = "Unregistered"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, f"{name} ({status})", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
