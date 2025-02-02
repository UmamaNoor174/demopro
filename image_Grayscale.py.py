import cv2
import numpy as np

# Path to the image
image_path = r"d:\downlods\istockphoto-1888768110-1024x1024.jpg"

# Load the image
image = cv2.imread(image_path)

# Check if the image is loaded successfully
if image is None:
    print(f"Error: Could not load the image. Please check the path: {image_path}")
else:
    print("Image loaded successfully.")

    # Display the original image
    cv2.imshow("Original Image", image)
    cv2.waitKey(1000)  # Wait for 1 second to ensure the image is visible

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Display the grayscale image
    cv2.imshow("Grayscale Image", gray_image)

    # Save the grayscale image (optional)
    output_path = r"c:\Users\Admin\Pictures\Grayscale_Image.jpg"
    cv2.imwrite(output_path, gray_image)
    print(f"Grayscale image saved to: {output_path}")

    # Wait for a key press and close all OpenCV windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
