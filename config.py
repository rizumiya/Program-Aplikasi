from PIL import Image, ImageTk
import openpyxl as xl
import tkinter as tk
import os

from modules import db_helper as dbh, scan_module as scan, database
from pages import page_signup as signup, page_signin as signin
import main as main


class WebCam:
    def __init__(self, root):
        self.root = root
        self.camera_no: int = 0
        self.camera_width: int = 0
        self.camera_height: int = 0
        self.current_angle: int = 0
    
    def image_rotate(self):
        # Merotasi gambar
        self.current_angle += 90
        rotated_image = self.image.rotate(self.current_angle)

        # Membuat objek Tkinter dari gambar yang telah dirotasi
        rotated_tk_image = ImageTk.PhotoImage(rotated_image)

        # Memperbarui gambar pada label
        self.label.configure(image=rotated_tk_image)
        self.label.image = rotated_tk_image


class PY_XL:
    def __init__(self, xlPath):
        self.xlPath = xlPath
        self.workbook = None
        self.sheet0 = None
        self.sheet1 = None

    def create_workbook(self):
        self.workbook = xl.Workbook()

    def create_scanning_history_sheet(self):
        self.sheet0 = self.workbook.active
        self.sheet0.title = "Scanning history"
        self.heading0 = [
            "Date/time", 
            "Subject", 
            "Classroom"
            ]
        self.sheet0.append(self.heading0)

    def create_scanning_result_sheet(self):
        self.workbook.create_sheet("Sheet_A")
        self.sheet1 = self.workbook["Sheet_A"]
        self.sheet1.title = "Scanning result"
        self.heading1 = [
            "Date/time", 
            "Subject", 
            "Classroom", 
            "Student ID", 
            "Grade", 
            "Wrong Answer"
            ]
        self.sheet1.append(self.heading1)

    def save_workbook(self):
        self.workbook.save(self.xlPath)

    def create_excel_file(self):
        if not os.path.exists(self.xlPath):
            self.create_workbook()
            self.create_scanning_history_sheet()
            self.create_scanning_result_sheet()
            self.save_workbook()


class config:
    def __init__(self):
        # Membuat database dan tabel
        db_manager = database.Database()
        db_manager.create_tables()

        # Membuat file excel
        excel_manager = PY_XL("assets/datas/omray.xlsx")
        excel_manager.create_excel_file()

        # Mengecek jika ada user aktif, jika tidak jalankan checkDataUser
        db_user = dbh.DB_User()
        db_user.table_name = "logins"
        userActive, userData= db_user.checkActiveUser()
        # Ambil data setting
        if userActive:
            # db_sett = dbh.DB_Setting()
            # db_sett.username = userData[0][1]
            # db_sett.password = userData[0][2]
            # settData = db_sett.getDataSetting()

            # Mengirim data user dan settingnya ke main
            mainmenu = main.Main_Menu(userData[0])
            mainmenu.mainloop()
        else:
            self.checkDataUser()

    def checkDataUser(self):
        # Mengecek database tabel user, jika belum ada buka sign up page
        db_helper = dbh.db_helper()
        db_helper.table_name = "logins"
        db_helper.fields = ["COUNT(*)"]
        dataExists = db_helper.checkIfdataExists()
        
        if dataExists:
            print("Buka Sign In")
            sign_in_form = signin.page_signin()
            sign_in_form.mainloop()
        else:
            print("Buka Sign Up")
            sign_up_form = signup.page_signup()
            sign_up_form.mainloop()













# import cv2
# import numpy as np

# # Fungsi untuk mengubah nilai threshold
# def change_threshold(value):
#     global threshold_value
#     threshold_value = value

# # Inisialisasi webcam
# cap = cv2.VideoCapture(0)

# # Inisialisasi nilai threshold awal
# threshold_value = 128

# # Inisialisasi flag rotasi video
# rotate = 0

# is_pressed = False

# previous = False
# current  = False

# # Membuat jendela GUI
# cv2.namedWindow("Webcam")
# cv2.createTrackbar("Threshold", "Webcam", threshold_value, 255, change_threshold)

# while True:
#     # Membaca frame dari webcam
#     ret, frame = cap.read()

#     # Mengubah frame menjadi grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Menerapkan thresholding
#     _, threshold = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

#     # Jika flag rotasi aktif, memutar frame
#     current = is_pressed
#     if (previous is False) and (current is True): 
#         rotate = (rotate + 90) % 360
#         print(rotate)
#     previous = current

#     if rotate == 90:
#         threshold = cv2.rotate(threshold, cv2.ROTATE_90_CLOCKWISE)
#     elif rotate == 180:
#         threshold = cv2.rotate(threshold, cv2.ROTATE_180)
#     elif rotate == 270:
#         threshold = cv2.rotate(threshold, cv2.ROTATE_90_COUNTERCLOCKWISE)

#     # Menampilkan frame hasil
#     cv2.imshow("Webcam", threshold)

#     # Mengecek tombol keyboard yang ditekan
#     key = cv2.waitKey(1)
#     if key == ord('q'):  # Tombol 'q' untuk keluar
#         break

#     is_pressed = (key == ord('r'))

# # Melepaskan sumber daya
# cap.release()
# cv2.destroyAllWindows()