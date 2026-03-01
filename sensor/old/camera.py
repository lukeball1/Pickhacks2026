import cv2

# 1. Initialize the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(4)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# 2. Capture a single frame
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame from webcam.")
    cap.release()
    exit()

# 3. Display the captured frame
cv2.imshow("Captured Image", frame)

# Wait until a key is pressed
cv2.waitKey(0)

# 4. Clean up
cap.release()
cv2.destroyAllWindows()
