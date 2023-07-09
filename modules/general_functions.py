from tkinter import messagebox, font
from modules import db_helper as dbh
from PIL import ImageFont

class Functions:
    
    def on_closing(self, root):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    # ambil jawaban dari subject tertentu
    def ambilJawaban(self, sub_name, queperbox):
        db_subb = dbh.DB_Subject()
        sub_data = db_subb.getDataFromSubName(sub_name)
        self.jawaban = sub_data[4]

        if self.jawaban:
            # Menguraikan string menjadi list yang valid
            jawaban_list = self.jawaban.split(', ')
            jawaban_list = [int(elem) for elem in jawaban_list]
            jawaban_sublist = [jawaban_list[i:i+queperbox] for i in range(0, len(jawaban_list), queperbox)]
            return sub_data, jawaban_sublist
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

    def get_subject(self, idlogin):
        db_sub = dbh.DB_Subject()
        self.dataSubject = db_sub.getSubjectASC(idlogin)
        
        if self.dataSubject is not None:
            self.subject_names = ['No Subject'] if len(self.dataSubject) == 0 else [row[1] for row in self.dataSubject]
        else:
            self.subject_names = ['No Subject']
        
        return self.subject_names
