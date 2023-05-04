# import cv2
# import numpy as np

# # Initialize the video capture object
# cap = cv2.VideoCapture(0)

# # Initialize the threshold value
# threshold_value = 140

# # Create a window to display the output frame
# cv2.namedWindow("Detected Rectangles")

# # Create a function to update the threshold value based on the slider position
# def update_threshold(value):
#     global threshold_value
#     threshold_value = value

# # Create a trackbar to adjust the threshold value
# cv2.createTrackbar("Threshold", "Detected Rectangles", threshold_value, 255, update_threshold)

# def newScanning():
#     while True:
#         # Capture a frame from the video stream
#         ret, frame = cap.read()

#         # Convert the frame to grayscale
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Apply the threshold value from the slider to create a binary image
#         _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

#         # Find contours in the binary image
#         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#         # Sort the contours by area in descending order
#         contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]

#         # Sort the contours from right to left
#         bounding_boxes = [cv2.boundingRect(c) for c in contours]
#         bounding_boxes = sorted(bounding_boxes, key=lambda x: x[0])

#         # Draw an outline on each of the four largest rectangles
#         for i, box in enumerate(bounding_boxes):
#             x, y, w, h = box
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.putText(frame, f"{i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

#         # Display the frame
#         cv2.imshow("Detected Rectangles", frame)

#         # Check for key press
#         key = cv2.waitKey(1)

#         # If Enter key is pressed, take a screenshot
#         if key == 13:
#             cv2.imwrite('screenshot.png', frame)
#             print('Screenshot saved!')

#         # If q key is pressed, exit
#         if key == ord("q"):
#             break

#     # Release the video capture object and close all windows
#     cap.release()
#     cv2.destroyAllWindows()

# newScanning()






import cv2
import numpy as np

# Initialize the video capture object
cap = cv2.VideoCapture(1)

# Initialize the threshold value
threshold_value = 140

# Create a window to display the output frame
cv2.namedWindow("Detected Rectangles")

# Create a function to update the threshold value based on the slider position
def update_threshold(value):
    global threshold_value
    threshold_value = value

# Create a trackbar to adjust the threshold value
cv2.createTrackbar("Threshold", "Detected Rectangles", threshold_value, 255, update_threshold)

def newScanning():
    while True:
        # Capture a frame from the video stream
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply the threshold value from the slider to create a binary image
        _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the binary image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sort the contours by area in descending order
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]

        # Sort the contours from right to left
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        bounding_boxes = sorted(bounding_boxes, key=lambda x: x[0])

        # Draw an outline on each of the four largest rectangles
        for i, box in enumerate(bounding_boxes):
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Create a separate window for each of the four largest rectangles
            if i < 4:
                roi = frame[y:y+h, x:x+w]
                cv2.imshow(f"Rectangle {i+1}", roi)

        # Display the frame
        cv2.imshow("Detected Rectangles", frame)

        # Check for key press
        key = cv2.waitKey(1)

        # If Enter key is pressed, take a screenshot
        if key == 13:
            cv2.imwrite('screenshot.png', frame)
            print('Screenshot saved!')

        # If q key is pressed, exit
        if key == ord("q"):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

newScanning()
