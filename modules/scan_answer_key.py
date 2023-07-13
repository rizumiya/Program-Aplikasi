import cv2
import time
import numpy as np
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk

from . import db_helper as dbh 

class ScanModule:
    def __init__(self, idLogin, subname, queperbox, question, choice, camera):

        # Mengisi variable utama
        self.idLogin = idLogin
        self.name_sub = subname
        self.camera_number = camera
        self.webcam_on = True
        self.queperbox = queperbox # numbers per box

        # variable subject
        self.question = question
        self.choice = choice
        self.ansid = 0
        self.box_pilgan = self.question // self.queperbox + (self.question % self.queperbox > 0)
        self.classroom = None

        self.widthImg = 600
        self.heightImg = 800
        self.kernel = np.ones((5, 5), np.uint8)

        self.rotate = 0
        self.is_pressed = False
        self.previous = False
        self.current  = False

        # Inisialisasi video webcam
        self.cap = cv2.VideoCapture(self.camera_number)
        self.threshold_value = 95
        self.create_threshold()


    def rotate_img(self, frame):
        self.current = self.is_pressed
        if (self.previous is False) and (self.current is True): 
            self.rotate = (self.rotate + 90) % 360
            # print(self.rotate)
        self.previous = self.current

        if self.rotate == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif self.rotate == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif self.rotate == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        self.is_pressed = False
        return frame


    # Membuat fungsi untuk update threshold
    def update_threshold(self, value):
        self.threshold_value = value


    def create_threshold(self):
        # Membuat window baru
        cv2.namedWindow("OMRay | Scanning")

        # Membuat trackbar di window 
        cv2.createTrackbar("Threshold", "OMRay | Scanning", self.threshold_value, 255,
                           self.update_threshold)


    def on_threshold_changed(self, value):
        self.threshold_value = value
    

    def splitBoxes(self, frame, min_width=20, min_height=20):
        height, width = frame.shape
        cell_width = max(width // self.choice, min_width)
        cell_height = max(height // self.queperbox, min_height)

        boxes = []
        for r in range(self.queperbox):
            for c in range(self.choice):
                try:
                    x = c * cell_width
                    y = r * cell_height
                    cell = frame[y:y+cell_height, x:x+cell_width]
                    boxes.append(cell)
                except:
                    # Mengatasi error jika ukuran tidak sama rata
                    cell = frame[r*cell_height:(r+1)*cell_height, c*cell_width:(c+1)*cell_width]
                    boxes.append(cell)

        return boxes


    def check_exam_paper(self, valid_contours):
        if len(valid_contours) == 0:
            self.nopaper = True
            cv2.putText(self.imgFinal, "No Exam Paper Detected!", (85, 400),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 3)
        else:
            self.nopaper = False



    def kotak_contour(self, dilated_edges):
        contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_contours = []
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4 and cv2.contourArea(approx) > 20000:
                valid_contours.append(approx)
        
        valid_contours = valid_contours[:4]

        valid_contours = sorted(valid_contours, key=lambda x: cv2.boundingRect(x)[0])

        self.check_exam_paper(valid_contours)

        return valid_contours[:self.box_pilgan]
    

    def preprocessing(self, frame):
        frame = cv2.resize(frame, (self.widthImg, self.heightImg))
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imgGray = cv2.bilateralFilter(imgGray, 11, 17, 17)

        # Menggunakan dilasi untuk memperbesar ketebalan garis tepi
        kernel = np.ones((2, 2), np.uint8)
        dilated_edges = cv2.Canny(imgGray, self.threshold_value, self.threshold_value * 2)
        dilated_edges = cv2.dilate(dilated_edges, kernel, iterations=1)

        self.imgFinal = frame.copy()
        valid_contours = self.kotak_contour(dilated_edges)

        return frame, valid_contours
    

    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect
    

    def warp_prespective(self, image, pts):
        rect = self.order_points(pts)

        dst = np.array([
            [0, 0], 
            [self.widthImg, 0], 
            [self.widthImg, self.heightImg], 
            [0, self.heightImg]], dtype="float32")
        
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (self.widthImg, self.heightImg))

        self.ttk1 = rect
        self.ttk2 = dst

        return warped


    def get_student_answer(self, boxes):
        jawabanPixelVal = np.zeros((self.queperbox, self.choice))
        hitC = 0
        hitR = 0

        for pilgan in boxes:
            if hitC == 0:
                jawabanPixelVal[hitR][hitC] = 0
                hitC += 1
                continue

            totalPixels = cv2.countNonZero(pilgan)
            jawabanPixelVal[hitR][hitC] = totalPixels

            hitC += 1
            if (hitC == self.choice):
                hitR += 1
                hitC = 0

        return jawabanPixelVal


    def array_to_string(self, data):
        result = []
        for sublist in data:
            sublist_str = ", ".join(str(item) for item in sublist)
            result.append(sublist_str)
        
        final_string = ", ".join(result)
        jawaban_list = final_string.split(', ')

        for i, _ in enumerate(jawaban_list):
            if i >= self.question:
                jawaban_list[i] = "0"

        final_string = ", ".join(jawaban_list)

        return final_string

    
    def check_answer(self, boxes):
        jawabanPixelVal = self.get_student_answer(boxes)

        jawabanIndex = []
        for x in range(0, self.queperbox):
            arr = jawabanPixelVal[x]
            nilaiJawabanIndex = np.where(arr == np.amax(arr))
            jawabanIndex.append(nilaiJawabanIndex[0][0])

        return jawabanIndex
    

    def save_to_database(self, answer):
        db_sub = dbh.DB_Subject()
        insertNewSubject = db_sub.addSubject(
            self.idLogin, 
            self.name_sub, 
            self.question,
            self.choice, 
            answer
        )

        if insertNewSubject:
            messagebox.showinfo("Success", "Subject "+ self.name_sub +" added!")
            return
        else:
            messagebox.showwarning("Invalid", "Double check before submit")
    
    
    def show_answers(self, img, ans, questions, choices, ansid):
        secW = int(img.shape[1]/choices)
        secH = int(img.shape[0]/questions)

        for x in range(0, questions):
            # Menampilkan jawaban benar dengan lingkaran
            myColor = (0, 255, 0)
            correctAns = ans[ansid][x]
            cv2.circle(img, ((correctAns * secW)+secW//2, (x * secH) + secH // 2),
                    20, myColor, cv2.FILLED)


    def start_scanning(self):
        while True:
            if self.webcam_on:
                _, frame = self.cap.read()
            else:
                frame = cv2.imread(self.imgPath)

            frame = self.rotate_img(frame)
            
            frame, valid_contours = self.preprocessing(frame)

            imgCopy = frame.copy()
            kuncijawaban = []

            # Menggambar kotak untuk setiap kontur
            for i, boxpilgan in enumerate(valid_contours):
                # Ambil titik sudut
                x, y, w, h = cv2.boundingRect(boxpilgan)

                cv2.drawContours(self.imgFinal, [boxpilgan], -1, (0, 255, 0), 2)

                warped = self.warp_prespective(frame, boxpilgan.reshape(4, 2))

                imgWrapGray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                imgTresh = cv2.threshold(imgWrapGray, 140, 255,
                                         cv2.THRESH_BINARY_INV)[1]

                # Bagi tiap kotak menjadi perkotak
                boxes = self.splitBoxes(imgTresh)
                self.ansid = i

                kunci_jawaban = self.check_answer(boxes)
                kuncijawaban.append(kunci_jawaban)

                imgWarpMentah = np.zeros_like(warped)

                self.show_answers(imgWarpMentah, kuncijawaban, self.queperbox, self.choice, self.ansid)
                
                invMatrix = cv2.getPerspectiveTransform(self.ttk2, self.ttk1)
                imgInWarp = cv2.warpPerspective(imgWarpMentah, invMatrix,
                                                (self.widthImg, self.heightImg))
            
                self.imgFinal = cv2.addWeighted(self.imgFinal, 1, imgInWarp, 1, 0)

            
            cv2.putText(self.imgFinal, "Press [q] to quit", (20, 720),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            cv2.putText(self.imgFinal, "Press [r] to rotate", (20, 750),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            cv2.putText(self.imgFinal, "Press [enter] to confirm", (20, 780),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            cv2.imshow("OMRay | Scanning", self.imgFinal)
            kunci_jawaban = self.array_to_string(kuncijawaban)

            # Menghentikan program jika tombol 'q' ditekan
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.is_pressed = True
            elif key == 13:
                if not self.nopaper:
                    self.save_to_database(kunci_jawaban)
                    break

        self.cap.release()
        cv2.destroyAllWindows()


class ScanWindow(ctk.CTkToplevel):
    def __init__(self, idLogin, bykPilgan, bykSoal, namaSub):
        super().__init__()
        self.title("OMRay | Subject")
        self.geometry('360x200+1200+90')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        self.question = bykSoal
        self.choice = bykPilgan
        self.nameSub = namaSub
        self.idLogin = idLogin

        # Header

        self.heading = ctk.CTkLabel(self, text='Scan Answer Key', text_color='#fff', 
                                    font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)

        # Widget

        self.camera_label = ctk.CTkLabel(self, text="Camera : ", 
                                         font=('Fresca', 16))
        self.camera_label.place(x=20, y=70)

        self.options = {
            0: "Default webcam",
            1: "External source"
        }

        self.caption = self.options[0]
        self.defaultCam = ctk.StringVar(value=self.caption)

        self.camera_box = ctk.CTkOptionMenu(master=self,
                                    width=140,
                                    values=list(self.options.values()),
                                    variable=self.defaultCam)
        self.camera_box.place(x=20, y=105)

        self.queperboxlbl = ctk.CTkLabel(self, text="Many rows in one table : ", 
                                        font=('Fresca', 16))
        self.queperboxlbl.place(x=180, y=70)

        self.queperbox_entry = ctk.CTkEntry(self, height=32, width=100, 
                                    text_color='white', 
                                    bg_color='transparent', font=('Fresca', 16))
        self.queperbox_entry.place(x=180, y=100)

        self.confirmNew = ctk.CTkButton(self, text="Start", 
                                        height=35, width=100, command=self.start_scanning_answer)
        self.confirmNew.place(relx=0.5, y=170, anchor=CENTER)

        self.after(200, self.lift)
    
    
    def ambilCam(self):
        if self.camera_box.get() == "Default webcam":
            return 0
        else : 
            return 1

    def get_queperbox(self):
        if not self.queperbox_entry.get().isdigit():
            messagebox.showerror("Error", "Input must be a number")
            return False
        else:
            self.queperbox = self.queperbox_entry.get()
            return True

    def start_scanning_answer(self):
        checkqueperbox = self.get_queperbox()
        if checkqueperbox:
            scan = ScanModule(self.idLogin, self.nameSub, int(self.queperbox), self.question, int(self.choice + 1), self.ambilCam())
            scan.start_scanning()
            self.destroy()
        else:
            return