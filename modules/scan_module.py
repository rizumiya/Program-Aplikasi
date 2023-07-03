import cv2
import numpy as np
from datetime import datetime

from modules import general_functions as func


class scan_module:
    def __init__(self, userp, passw):

        # ambil data setting dan subject
        self.funct = func.Functions()
        setting = self.funct.getSettingData(userp, passw)
        detailSub, jawaban = self.funct.ambilJawaban(setting[3])
        
        # Mengisi variable utama

        # variable setting
        self.idLogin = setting[1]
        self.selectedCamera = setting[2]
        self.selectedSub = setting[3]
        self.showAnswer = setting[4]
        self.autoSave = setting[5]

        # variable subject
        self.bykTanya = detailSub[2]
        self.bykJawab = detailSub[3]
        self.jawaban = jawaban

        self.webcam_on = True
        now = datetime.now()
        self.waktu = now.strftime("%Y-%m-%d %H:%M")
        self.widthImg = 800
        self.heightImg = 600
        self.kernel = np.ones((5, 5), np.uint8)

        # Inisialisasi video webcam
        self.cap = cv2.VideoCapture(self.selectedCamera)
        self.cap.set(10, 150)
        self.threshold_value = 140
        self.create_threshold()


    # Membuat fungsi untuk update threshold
    def update_threshold(self, value):
        self.threshold_value = value


    def create_threshold(self):
        # Membuat window baru
        cv2.namedWindow("OMRay | Scanning")

        # Membuat trackbar di window 
        cv2.createTrackbar("Threshold", "OMRay | Scanning", self.threshold_value, 255,
                           self.update_threshold)


    def preprocessing(self, frame):
        frame = cv2.resize(frame, (self.widthImg, self.heightImg))
        imgContourTerbesar = frame.copy()
        imgContours = frame.copy()
        imgFinal = frame.copy()
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, 10, 40)
        imgDilate = cv2.dilate(imgCanny, self.kernel, iterations=1)


    def start_scanning(self):
        # self.preprocessing(frame)

        while True:
            if self.webcam_on:
                _, frame = self.cap.read()
            
            cv2.imshow("OMRay | Scanning", frame)
            print(self.threshold_value)

            key = cv2.waitKey(1)

            # q untuk berhenti
            if key == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()



    
        