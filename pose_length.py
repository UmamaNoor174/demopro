import cv2
import mediapipe as mp
import math

# Function to calculate the Euclidean distance between two landmarks
def calculate_distance(landmark1, landmark2, image_width, image_height):
    x1, y1 = int(landmark1.x * image_width), int(landmark1.y * image_height)
    x2, y2 = int(landmark2.x * image_width), int(landmark2.y * image_height)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Initialize Mediapipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Use Mediapipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Unable to access the webcam.")
            break

        # Get the frame dimensions
        image_height, image_width, _ = frame.shape

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame to detect poses
        results = pose.process(rgb_frame)

        # Draw pose landmarks on the original frame
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
            )

            # Access the landmarks
            landmarks = results.pose_landmarks.landmark

            # Define specific body parts
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            mouth_left = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT]
            mouth_right = landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT]
            left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE]
            right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE]

            # Calculate distances
            distance_between_wrists = calculate_distance(left_wrist, right_wrist, image_width, image_height)
            distance_between_eyes = calculate_distance(left_eye, right_eye, image_width, image_height)
            mouth_width = calculate_distance(mouth_left, mouth_right, image_width, image_height)

            # Display distances on the frame
            cv2.putText(frame, f"Wrists Distance: {int(distance_between_wrists)} px", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Eyes Distance: {int(distance_between_eyes)} px", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Mouth Width: {int(mouth_width)} px", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Display the frame
        cv2.imshow('Pose Estimation with Body Part Detection', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
