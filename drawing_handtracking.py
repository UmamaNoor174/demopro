import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hands and Drawing Utilities
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Start Video Capture
cap = cv2.VideoCapture(0)

# Initialize Canvas for Drawing
canvas = None
prev_x, prev_y = 0, 0  # To track the previous position of the index finger

while True:
    # Read frame from webcam
    success, frame = cap.read()
    if not success:
        break

    # Flip frame horizontally for natural interaction
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB for Mediapipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Create a canvas for drawing (if not already created)
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

            # Get position of the index finger's tip
            landmarks = hand_landmark.landmark
            h, w, c = frame.shape
            index_x = int(landmarks[8].x * w)
            index_y = int(landmarks[8].y * h)

            # Detect if only the index finger is up (gesture detection)
            fingers_up = landmarks[8].y < landmarks[6].y  # Check if index finger is above its knuckle
            if fingers_up:
                # If this is the first point, initialize the previous position
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = index_x, index_y
                else:
                    # Draw a line on the canvas from the previous position to the current
                    canvas = cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), (255, 0, 0), 5)
                # Update the previous position
                prev_x, prev_y = index_x, index_y
            else:
                # Reset the previous position when the gesture is not active
                prev_x, prev_y = 0, 0

    # Blend the canvas and the webcam feed
    combined_frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Show the combined frame
    cv2.imshow("Drawing with Hand Gestures", combined_frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
