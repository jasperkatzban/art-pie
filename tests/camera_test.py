import cv2

# create video capture object
cap = cv2.VideoCapture(0)
windowName = 'Laser Finder'

# run a continuous loop
while True:
    # Capture each frame
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow(windowName, frame)

    # quit by pressing CTRL/CMD + Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()