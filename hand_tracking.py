# Import the libraries
import cv2
import mediapipe as mp

# Initialize MediaPipe Hands and Drawing Utils
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

# Open webcam
cap = cv2.VideoCapture(0)
hands = mphands.Hands()

while True:
    ret, image = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # Flip the image and convert it to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process the image
    results = hands.process(image)

    # Convert back to BGR for rendering
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw hand landmarks if any are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mphands.HAND_CONNECTIONS)

    # Show the image
    cv2.imshow('Handtracker', image)

    # Exit the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()