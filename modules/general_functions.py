from tkinter import messagebox
from modules import db_helper as dbh

class Functions:
    
    def on_closing(self, root):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    # ambil jawaban dari subject tertentu
    def ambilJawaban(self, sub_name):
        db_subb = dbh.DB_Subject()
        sub_data = db_subb.getDataFromSubName(sub_name)
        self.jawaban = sub_data[4]

        if self.jawaban:
            self.jawaban_array = self.jawaban.split(",")
            return sub_data, self.jawaban_array
        else:
            print("Data kunci jawaban tidak ditemukan")
            return None, None


    def pisah_karakter(text):
        karakter = ', '.join(text)
        return karakter
    
    
    def convertArraykeString(self, text):
        string = ", ".join(str(x) for x in text)
        return string
    
    def getSettingData(self, user, passw):
        db_sett = dbh.DB_Setting()
        db_sett.username = user
        db_sett.password = passw
        settData = db_sett.getDataSetting()
        return settData[0]
    