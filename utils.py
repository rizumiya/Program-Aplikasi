#========================================
# Nama  : Rizki Nur Rachmadi Y
# NIM   : 1900018014
# Univ  : Universitas Ahmad Dahlan
# APP   : Penilaian ujian harian dengan Lembar Jawab tidak berbasis komputer
#========================================

import cv2
import numpy as np


def stackImages(imgArray, scale, lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(
                    imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        hor_con = np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth = int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        # print(eachImgHeight)
        for d in range(0, rows):
            for c in range(0, cols):
                cv2.rectangle(ver, (c*eachImgWidth, eachImgHeight*d), (c*eachImgWidth+len(
                    lables[d][c])*13+27, 30+eachImgHeight*d), (255, 255, 255), cv2.FILLED)
                cv2.putText(ver, lables[d][c], (eachImgWidth*c+10, eachImgHeight *
                            d+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
    return ver


# Preprocessing #1
def preprocesing_lj(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_tresh = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
    img_canny = cv2.Canny(img_tresh, 100, 100, apertureSize=5)
    img_dilate = cv2.dilate(img_canny, np.ones((2, 2)), iterations=1)
    img_erode = cv2.erode(img_dilate, np.ones((2, 2)), iterations=1)
    return img_erode


# Preprocessing #2
def preprocesing_pg(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgThresh = cv2.threshold(img_gray, 135, 255, cv2.THRESH_BINARY)
    img_canny = cv2.Canny(imgThresh, 100, 100, apertureSize=7)
    kernel = np.ones((2, 2))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=1)
    img_erode = cv2.erode(img_dilate, kernel, iterations=1)
    return img_erode


# Cari kontur area terbesar
def kotakContour(contours):
    kotakCont = []
    for i in contours:
        area = cv2.contourArea(i)
        # print(area)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                kotakCont.append(i)
    kotakCont = sorted(kotakCont, key=cv2.contourArea, reverse=True)
    print("panjang kotakCont: ", len(kotakCont))
    return kotakCont


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))  # REMOVE EXTRA BRACKET
    # print(myPoints)
    # NEW MATRIX WITH ARRANGED POINTS
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    # print(add)
    # print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  # [0,0]
    myPointsNew[3] = myPoints[np.argmax(add)]  # [w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]  # [w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)]  # [h,0]

    return myPointsNew


def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)  # LENGTH OF CONTOUR
    # APPROXIMATE THE POLY TO GET CORNER POINTS
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
    return approx


# Cek semua kontur
def cekKontur(img, prepos):
    imgContours = img.copy()
    imgConTerbesar = img.copy()
    imgWarpWarna = img.copy()
    widthImg = 600
    heightImg = 800
    # cv2.imshow("test : ", prepos)
    try:
        # Mencari semua contour
        contours, hierarchy = cv2.findContours(prepos, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)
        # Mencari Kotak
        kotakCont = kotakContour(contours)
        ConTerbesar = getCornerPoints(kotakCont[0])
        # print(ConTerbesar)
        if ConTerbesar.size != 0:
            cv2.drawContours(imgConTerbesar, ConTerbesar, -1, (0, 255, 0), 20)
            ConTerbesar = reorder(ConTerbesar)
            pt1 = np.float32(ConTerbesar)
            pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg],
                              [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpWarna = cv2.warpPerspective(img, matrix,
                                               (widthImg, heightImg))
            # cv2.imshow("Warp", imgWarpWarna)
        else:
            cv2.putText(imgConTerbesar, "Tidak ada lembar jawab", (15, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 255, 100), 2)
    except:
        print("gak bisa")

    return imgWarpWarna


def crop_image(img):
    img = img[150:360, 45:565]
    img = cv2.resize(img, (1050, 420))
    # print(img.shape)
    return img


def cropPerPG(img):
    img = crop_image(img)
    imgKotak = []
    p = 20
    l = 275
    for i in range(4):  #jumlah kotakan pilihan ganda
        i = img[0:, p:l]
        imgKotak.append(i)
        p = l
        l += 255
    return imgKotak


def splitBoxes(img):
    rows = np.vsplit(img, 10)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 5)
        for box in cols:
            boxes.append(box)
            # cv2.imshow("split", box)
    return boxes


def potongPG(img):
    imgWarpGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgTresh = cv2.threshold(imgWarpGray, 130, 255, cv2.THRESH_BINARY_INV)
    boxes = splitBoxes(imgTresh)
    # cv2.imshow("tests", boxes[0])
    return boxes