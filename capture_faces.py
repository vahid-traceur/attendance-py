import cv2
import os

# Get person name
person_names = input("Enter the person name: ").strip().lower()

# Store path
base_dir = 'known_faces'
person_dir = os.path.join(base_dir, person_names)

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

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(
        rgb, scaleFactor=1.3, minNeighbors=5
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Capture Faces", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_img = frame[y:y + h, x:x + w]
        img_path = os.path.join(person_dir, f"{count}.jpg")
        cv2.imwrite(img_path, face_img)
        count += 1
        print(f"Saved {count} faces in {img_path}")

        if count >= max_images:
            print("Face captured completed")
            break
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
