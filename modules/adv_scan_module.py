import cv2
import numpy as np
import openpyxl
from tkinter import messagebox
from datetime import datetime

from . import general_functions as func


class AdvanceScanModule:
    def __init__(self, subject_1, cam_no, queperbox, order_sid, ttl_stud):
        # Inisialisasi variable awal
        self.autosave = 0
        self.use_sid = 0
        self.order_sid = order_sid
        self.classroom_name = None
        self.total_student = ttl_stud if ttl_stud != None else 999
        self.subject_1 = subject_1
        self.camera_number = cam_no
        self.queperbox = queperbox
        self.show_answer = False
        self.student_id = 1 if order_sid == "Ascending" and order_sid != None else self.total_student

        # Ambil data Subject dari database
        self.funct = func.Functions()
        detailSub, jawaban = self.funct.ambilJawaban(self.subject_1, self.queperbox)

        self.subject_name = detailSub[1]
        self.question = detailSub[2]
        self.choice = detailSub[3]
        self.ansid = 0
        self.ans = jawaban
        self.box_pilgan = self.question // self.queperbox + (self.question % self.queperbox > 0)

        self.all_done = False
        self.webcam_on = True
        self.imgPath = "p1.jpg"
        now = datetime.now()
        self.waktu = now.strftime("%Y-%m-%d %H:%M")
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


    def show_answers(self, img, myIndex, grading, ans, questions, choices, ansid):
        secW = int(img.shape[1]/choices)
        secH = int(img.shape[0]/questions)

        for x in range(0, questions):
            myAns = myIndex[x]
            cX = (myAns * secW) + secW // 2
            cY = (x * secH) + secH // 2
            if grading[x] == 1:
                myColor = (0, 255, 0)
                cv2.rectangle(img, (myAns*secW, x*secH), ((myAns*secW) +
                            secW, (x*secH)+secH), myColor, cv2.FILLED)
                cv2.circle(img, (cX, cY), 35, myColor, cv2.FILLED)
            else:
                myColor = (0, 0, 255)
                cv2.rectangle(img, (myAns * secW, x * secH), ((myAns *
                            secW) + secW, (x * secH) + secH), myColor, cv2.FILLED)
                cv2.circle(img, (cX, cY), 35, myColor, cv2.FILLED)

                # Menampilkan jawaban benar dengan lingkaran
                myColor = (0, 255, 0)
                correctAns = ans[ansid][x]
                cv2.circle(img, ((correctAns * secW)+secW//2, (x * secH) + secH // 2),
                        20, myColor, cv2.FILLED)


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

    
    def check_answer(self, boxes, i):
        jawabanPixelVal = self.get_student_answer(boxes)

        self.jawabanIndex = []
        for x in range(0, self.queperbox):
            arr = jawabanPixelVal[x]
            nilaiJawabanIndex = np.where(arr == np.amax(arr))
            self.jawabanIndex.append(nilaiJawabanIndex[0][0])

        # Evaluate the answers
        penilaian = []
        salah = []
        for x in range(0, self.queperbox):
            try:
                if self.ans[self.ansid][x] == 0:
                    self.jawabanIndex[x] = 0
                if self.ans[self.ansid][x] != 0 and self.ans[self.ansid][x] == self.jawabanIndex[x]:
                    penilaian.append(1)
                else:
                    i = self.ansid * 10
                    penilaian.append(0)
                    salah.append(x + 1 + i)
            except:
                messagebox.showerror("Error", "Please check how many rows in the table")
                self.cap.release()
                cv2.destroyAllWindows()
                break

        jawab_benar = sum(penilaian)  # 1 nilai

        return jawab_benar, penilaian, salah


    def save_to_excel(self, sheet_index, **kwargs):
        xlPath = "assets/datas/omray.xlsx"
        classroom = "Regular" if not self.classroom_name else self.classroom_name

        workbook = openpyxl.load_workbook(xlPath)
        sheet = workbook.worksheets[sheet_index]

        if sheet_index == 0:
            sheet.append([self.waktu, self.subject_name, classroom])
        else:
            sheet.append([self.waktu, self.subject_name, classroom, self.student_id, kwargs["total_score"], str(kwargs["NoW"])])
        
        workbook.save(xlPath)


    def next_student(self, NoW, total_score):
        NoW = NoW if len(NoW) != 0 else "No wrong answer"

        if self.order_sid == "Ascending" and self.student_id <= self.total_student:
            self.save_to_excel(1, NoW=NoW, total_score=total_score)
            self.student_id += 1
        if self.order_sid == "Descending" and self.student_id >= 1:
            self.save_to_excel(1, NoW=NoW, total_score=total_score)
            self.student_id -= 1

        if self.order_sid == "Ascending" and self.student_id > self.total_student:
            self.all_done = True
        elif self.order_sid == "Descending" and self.student_id == 0:
            self.all_done = True
    

    def skip_student(self):
        if self.order_sid == "Ascending" and self.order_sid != None:
            self.student_id += 1
        elif self.order_sid == "Descending" and self.order_sid != None:
            self.student_id -= 1
            
        if self.order_sid == "Ascending" and self.student_id > self.total_student:
            self.all_done = True
        elif self.order_sid == "Descending" and self.student_id == 0:
            self.all_done = True


    def start_scanning(self):
        while True:
            if self.webcam_on:
                _, frame = self.cap.read()
            else:
                frame = cv2.imread(self.imgPath)

            frame = self.rotate_img(frame)
            
            frame, valid_contours = self.preprocessing(frame)

            imgCopy = frame.copy()

            total_score = 0
            jwb_benar = 0
            get_salah = True
            NoW = []

            # Menggambar kotak untuk setiap kontur
            for i, boxpilgan in enumerate(valid_contours):
                # Ambil titik sudut
                x, y, w, h = cv2.boundingRect(boxpilgan)

                cv2.drawContours(imgCopy, [boxpilgan], -1, (0, 255, 0), 2)

                warped = self.warp_prespective(frame, boxpilgan.reshape(4, 2))

                imgWrapGray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                imgTresh = cv2.threshold(imgWrapGray, 140, 255,
                                         cv2.THRESH_BINARY_INV)[1]

                # Bagi tiap kotak menjadi perkotak
                boxes = self.splitBoxes(imgTresh)
                self.ansid = i

                jawaban_benar, penilaian, salah = self.check_answer(boxes, i)

                for wrong_ans in salah:
                    if i < len(valid_contours) and get_salah:
                        NoW.append(wrong_ans)

                
                jwb_benar += jawaban_benar

                imgWarpMentah = np.zeros_like(warped)

                self.show_answers(imgWarpMentah, self.jawabanIndex, penilaian, self.ans, self.queperbox, self.choice, self.ansid)

                if self.show_answer:
                    cv2.putText(self.imgFinal, str(jawaban_benar), (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    invMatrix = cv2.getPerspectiveTransform(self.ttk2, self.ttk1)
                    imgInWarp = cv2.warpPerspective(imgWarpMentah, invMatrix,
                                                    (self.widthImg, self.heightImg))

                    self.imgFinal = cv2.addWeighted(self.imgFinal, 1, imgInWarp, 1, 0)

            if self.order_sid != None: 
                cv2.putText(self.imgFinal, str(self.student_id), (500, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

            # Perhitungan total score
            total_score = (jwb_benar / self.question) * 100

            cv2.putText(self.imgFinal, str(int(total_score)), (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
            
            cv2.imshow("OMRay | Scanning", self.imgFinal)

            # Menghentikan program jika tombol 'q' ditekan
            key = cv2.waitKey(10)
            if key == ord('q'):
                if self.autosave:
                    self.save_to_excel(0)
                break
            elif key == ord('r'):
                self.is_pressed = True
            elif key == 13:
                if not self.nopaper:
                    self.next_student(NoW, total_score)
                    self.get_salah = False
            elif key == ord('s'):
                self.skip_student()
            
            if self.all_done:
                self.save_to_excel(0)
                break

        self.cap.release()
        cv2.destroyAllWindows()
        



        