import cv2
import numpy as np
import time
import assets.libs.utils as utils

path = "jwb1-10.png"
widthImg = 600
HeighImg = 800
start_time = time.time()
end_time = time.time()

webcamFeed = False
cameraNo = 0
cap = cv2.VideoCapture(cameraNo)
cap.set(600, 800)


# Prepocessing
def preprocessing(img):
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, im_thresh = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
    im_canny = cv2.Canny(im_gray, 100, 200)
    im_dilate = cv2.dilate(im_canny, np.ones((2, 2)), iterations=1)
    im_erode = cv2.erode(im_dilate, np.ones((2, 2)), iterations=1)
    return im_gray, im_canny, im_dilate, im_erode

def preprocessing2(img):
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, im_thresh = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
    im_canny = cv2.Canny(im_thresh, 100, 200, apertureSize=5)
    im_dilate = cv2.dilate(im_canny, np.ones((2, 3)), iterations=1)
    im_erode = cv2.erode(im_dilate, np.ones((2, 3)), iterations=1)
    return im_gray, im_canny, im_dilate, im_erode


while True:
    if webcamFeed:
        success, img = cap.read()
    else:
        img = cv2.imread(path)
        img = cv2.resize(img, (widthImg, HeighImg))

    imgBlank = np.zeros_like(img)

    ## ============================================================

    preprocessed_img = preprocessing(img)
    img_warp_warna = utils.getBiggestContour(img, preprocessed_img[3])
    imgConTerbesar = img_warp_warna[1]

    cv2.imshow("Warp", img_warp_warna[0])

    ## ============================================================

    kotakPG = utils.cropPerPG(img_warp_warna[0])
    preprocessed_img2 = preprocessing2(kotakPG[0])

    ## ============================================================

    imgArray = ([img, preprocessed_img[0], preprocessed_img[1],
                 preprocessed_img[2]], [preprocessed_img[3], imgConTerbesar, imgBlank, imgBlank])
    imgStacked = utils.stackImages(imgArray, 0.5)
    cv2.imshow("Stacked Images", imgStacked)

    imgArray2 = ([kotakPG[0], kotakPG[1], kotakPG[2], kotakPG[3]],
                 [preprocessed_img2[0], preprocessed_img2[1], preprocessed_img2[2], preprocessed_img2[3]])
    imgStacked2 = utils.stackImages(imgArray2, 0.5)
    cv2.imshow("Stacked Images 2", imgStacked2)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == 27:
        break

    # time.sleep(1 - (end_time - start_time))

cv2.waitKey(0)
