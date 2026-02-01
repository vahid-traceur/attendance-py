import cv2
import face_recognition
import os

KNOWN_FACES_DIR = "known_faces"
TOLERANCE = 0.5
FRAME_THICKNESS = 2
FONT_THICKNESS = 2

known_encodings = []
known_names = []

print("Loading known faces...")

for name in os.listdir(KNOWN_FACES_DIR):
    person_dir = os.path.join(KNOWN_FACES_DIR, name)
    if not os.path.isdir(person_dir):
        continue

    for filename in os.listdir(person_dir):
        image_path = os.path.join(person_dir, filename)

        # ✅ خواندن امن تصویر
        bgr_image = cv2.imread(image_path)
        if bgr_image is None:
            print(f"Skipping invalid image: {image_path}")
            continue

        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb_image)
        if len(encodings) == 0:
            print(f"No face found in {image_path}")
            continue

        known_encodings.append(encodings[0])
        known_names.append(name)

print("Known faces loaded.")

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, locations)

    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(
            known_encodings, face_encoding, TOLERANCE
        )
        name = "Unknown"

        if True in results:
            match_index = results.index(True)
            name = known_names[match_index]

        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), FRAME_THICKNESS)
        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
            FONT_THICKNESS,
        )

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
