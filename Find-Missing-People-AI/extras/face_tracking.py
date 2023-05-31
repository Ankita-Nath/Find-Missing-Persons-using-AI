import cv2

# Create a new object tracker
tracker = cv2.legacy.MultiTracker_create()
face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

# Open a video capture object
cap = cv2.VideoCapture(0)

# Read the first frame of the video
success, frame = cap.read()

# Get the initial bounding boxes of the faces in the frame
faces = face_cascade.detectMultiScale(
    frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
)

# Add the faces to the tracker
for (x, y, w, h) in faces:
    tracker.add(cv2.TrackerMOSSE_create(), frame, (x, y, w, h))

# Create a set to store the IDs of the tracked faces
tracked_faces = set()

while True:
    # Read the next frame of the video
    success, frame = cap.read()

    # Update the tracker with the new frame
    success, boxes = tracker.update(frame)

    # Draw the bounding boxes around the tracked faces
    for box in boxes:
        (x, y, w, h) = [int(i) for i in box]
        face_id = (x, y, w, h)

        # Check if the face is new
        if face_id not in tracked_faces:
            print("New face detected!")
            tracked_faces.add(face_id)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Tracked Faces", frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object
cap.release()

# Close all windows
cv2.destroyAllWindows()
