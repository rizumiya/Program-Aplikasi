from assets.libs.utils import kotakContour, getCornerPoints, reorder, splitBoxes, showAnswers, stackImages
import cv2
import numpy as np
import datetime
import openpyxl

imgPath = "../papers/paper.jpg"
xlPath = "assets/temps/omray.xlsx"

widthImg = 800
heightImg = 600
kernel = np.ones((5, 5), np.uint8)

questions = 0 # 10
choices = 0 # 5

ansid = 0
ans = [[2, 3, 1, 2, 3, 2, 2, 3, 1, 3],
       [1, 2, 2, 2, 3, 2, 1, 1, 1, 4]]

webcamOn = True
cameraNo = 0
checking = True

now = datetime.datetime.now()
waktu = now.strftime("%Y-%m-%d %H:%M")

# Initialize the video capture object
cap = cv2.VideoCapture(cameraNo)
cap.set(10, 150)

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

def newScanning(webcamOn, cameraNo, questions, choices, ans, ansid):
    # deklarasi variable
    grade = 0
    score = 0
    salah = []
    NoW = []

    cap = cv2.VideoCapture(cameraNo)
    cap.set(10, 150)

    while True:
        if webcamOn:
            # Capture a frame from the video stream
            ret, frame = cap.read()
        else:
            frame = cv2.imread(imgPath)

        # preprocessing 
        frame = cv2.resize(frame, (widthImg, heightImg))
        imgContourTerbesar = frame.copy()
        imgContours = frame.copy()
        imgFinal = frame.copy()
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, 10, 40)
        imgDilate = cv2.dilate(imgCanny, kernel, iterations=1)

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply the threshold value from the slider to create a binary image
        _, thresh = cv2.threshold(imgGray, threshold_value, 255, cv2.THRESH_BINARY_INV)

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
            # cv2.putText(frame, f"{i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            key = cv2.waitKey(1)
            
            # Create a separate window for each of the four largest rectangles
            if i < 4:
                roi = frame[y:y+h, x:x+w]
                roi = cv2.resize(roi, (widthImg, heightImg))
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                roi = cv2.threshold(roi, threshold_value, 255, cv2.THRESH_BINARY_INV)[1]
                cv2.imshow(f"Rectangle {i+1}", roi)
                kotakan = splitBoxes(roi)

            # If Enter key is pressed, take a screenshot
                try:
                    # Find non-zero pixel value for each answer
                    jawabanPixelVal = np.zeros((questions, choices))
                    hitC = 0
                    hitR = 0

                    for gambar in kotakan:
                        if hitC == 0:
                            jawabanPixelVal[hitR][hitC] = 0
                            hitC += 1
                            continue
                            
                        totalPixels = cv2.countNonZero(gambar)
                        jawabanPixelVal[hitR][hitC] = totalPixels
                        
                        hitC += 1
                        if (hitC == choices):
                            hitR += 1
                            hitC = 0

                    # Find the index value for each answer
                    jawabanIndex = []
                    for x in range(0, questions):
                        arr = jawabanPixelVal[x]
                        nilaiJawabanIndex = np.where(arr == np.amax(arr))
                        jawabanIndex.append(nilaiJawabanIndex[0][0])

                    # Evaluate the answers
                    penilaian = []
                    salah = []
                    for x in range(0, questions):
                        if ans[ansid][x] == jawabanIndex[x]:
                            penilaian.append(1)
                        else:
                            penilaian.append(0)
                            salah.append(x + 1)
                    
                    score = (sum(penilaian)/questions) * 20 # 1 nilai
                    roiCopy = frame.copy()
                    showAnswers(roiCopy, jawabanIndex, penilaian, ans,
                                  questions, choices, ansid)
                    cv2.imshow(f"tyutyu {i+1}", roiCopy)
                except:
                    print("error : " + i)
            cv2.putText(frame, str(round(score, 2)), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


        # Display the frame
        cv2.imshow("Detected Rectangles", frame)

        # Check for key press
        key = cv2.waitKey(1)

        # If Enter key is pressed, take a screenshot
        # if key == 13:
        #     cv2.imwrite('screenshot.png', frame)
        #     print('Screenshot saved!')

        # If q key is pressed, exit
        if key == ord("q"):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

# newScanning(True, 1, 10, 5, ans, ansid)