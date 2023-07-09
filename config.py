import openpyxl as xl
import os

from modules import db_helper as dbh, database
from pages import page_signup as signup, page_signin as signin
import main as main


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
            # Mengirim data user dan settingnya ke main
            mainmenu = main.MainMenu(userData[0])
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
            sign_in_form = signin.PageSignIn()
            sign_in_form.mainloop()
        else:
            sign_up_form = signup.PageSignUp()
            sign_up_form.mainloop()

