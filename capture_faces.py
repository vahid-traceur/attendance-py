import cv2
import os

person_name = input("Enter person name: ").strip().lower()

base_dir = "known_faces"
person_dir = os.path.join(base_dir, person_name)
os.makedirs(person_dir, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

count = 0
max_images = 5

print("Press 's' to save face, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Capture Faces", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_img = frame[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(person_dir, f"{count}.jpg"), face_img)
        count += 1
        print(f"Saved image {count}")

        if count >= max_images:
            print("Done")
            break

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
