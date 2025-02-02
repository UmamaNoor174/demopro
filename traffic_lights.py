import cv2
import numpy as np
from tkinter import Tk, filedialog

# Function to choose an image file
def get_image_path():
    # Create a hidden Tkinter root window
    Tk().withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    return file_path

# Function to handle mouse click events
def mouse_click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # On left mouse click
        # If clicked on the traffic light region, check for its color
        hsv_value = hsv_image[y, x]  # Get HSV value at the clicked pixel
        hue, sat, val = hsv_value

        # Check for the traffic light color based on the HSV value
        if (0 <= hue <= 10 or 160 <= hue <= 180) and sat > 100 and val > 100:
            text = "Red for STOP"
        elif 20 <= hue <= 30 and sat > 100 and val > 100:
            text = "Yellow for READY"
        elif 40 <= hue <= 90 and sat > 50 and val > 50:
            text = "Green for GO"
        else:
            text = "No specific signal detected."

        print(f"Traffic light color detected: {text}")
        show_text(text)

# Function to display text on the image
def show_text(text):
    temp_image = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(temp_image, text, (20, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)  # Text in White color
    cv2.imshow("Traffic Signal Detection", temp_image)

# Ask user to select an image
image_path = get_image_path()
if not image_path:
    print("No image selected. Exiting...")
    exit()

# Load the selected image
image = cv2.imread(image_path)

# Check if the image is loaded successfully
if image is None:
    print(f"Error: Could not load the image. Please check the path: {image_path}")
    exit()

# Resize the image for better visualization (optional)
image = cv2.resize(image, (400, 400))

# Convert the image to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Display the image and set the mouse callback
cv2.imshow("Traffic Signal Detection", image)
cv2.setMouseCallback("Traffic Signal Detection", mouse_click_event)

# Wait for a key press and close all OpenCV windows
cv2.waitKey(0)
cv2.destroyAllWindows() 