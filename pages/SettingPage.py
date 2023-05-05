import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
import sqlite3
import os

from assets.libs.Database import Database
from assets.libs.Module import Module

class SettingPage(ctk.CTkToplevel):
    def __init__(self, parent, title, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title(title)
        self.geometry('700x380+1000+70')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        #variable
        
        self.database = Database()
        self.my_module = Module()

        # ambil data dari database ================================================================

        self.SQLPATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'temps', 'omr.db')
        global conn
        self.conn = sqlite3.connect(self.SQLPATH)
        self.cur = self.conn.cursor()

        # contoh kode ambil jawaban dari subject tertentu
        self.cur.execute('SELECT sub_answer FROM subjects WHERE sub_id = "1"')
        self.kunci_jwb = self.cur.fetchall()
        if self.kunci_jwb:
            self.jawaban_string = self.kunci_jwb[0][0]
            self.jawaban_array = self.jawaban_string.split(",")
            # kode lainnya di sini
        else:
            print("Data kunci jawaban tidak ditemukan")
        # print(jawaban_array)

        # ambil daftar subject
        self.cur.execute("SELECT sub_name FROM subjects")
        # simpan hasil query ke dalam array
        self.data = self.cur.fetchall()
        self.subject_names = ['No Subject'] if len(self.data) == 0 else [row[0] for row in self.data]


        self.id_login = self.database.selectActive()
        self.dataSetting = self.database.selectAttributes('*', 'settings', 'id_login=' + str(self.id_login))
        self.selectedCamera = self.dataSetting[0][2]
        self.selectedSub = self.dataSetting[0][3]
        self.showAnswer = self.dataSetting[0][4]
        self.autoSave = self.dataSetting[0][5]
        
        # ===========================================================================================
    

        # Menambahkan judul
        self.heading = ctk.CTkLabel(self, text='Setting', text_color='#fff', font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)

        # bagian kiri
        self.defaultScn_label = ctk.CTkLabel(self, text="Default Scanning")
        self.defaultScn_label.place(x=20, y=70)

        self.defaultScanScrollableFrame = ctk.CTkScrollableFrame(self, width=300, height=80)
        self.defaultScanScrollableFrame.place(x=20, y=100)

        self.aturtampilan = ctk.CTkLabel(self.defaultScanScrollableFrame, text="")
        self.aturtampilan.grid(row=0, column=0, padx=0, pady=80, sticky="n")

        self.camera_label = ctk.CTkLabel(self.defaultScanScrollableFrame, text="Camera : ")
        self.camera_label.place(x=10, y=10)

        self.options = {
            0: "Default webcam",
            1: "External source"
        }

        self.caption = self.options[self.selectedCamera]
        self.defaultCam = ctk.StringVar(value=self.caption)

        self.camera_box = ctk.CTkOptionMenu(master=self.defaultScanScrollableFrame,
                                    width=190,
                                    values=list(self.options.values()),
                                    variable=self.defaultCam)
        self.camera_box.place(x=100, y=10)


        self.subject_label = ctk.CTkLabel(self.defaultScanScrollableFrame, text="Subject : ")
        self.subject_label.place(x=10, y=60)

        self.subject_box = ctk.CTkOptionMenu(master=self.defaultScanScrollableFrame,
                                    width=190,
                                    values=self.subject_names)
        self.subject_box.place(x=100, y=60)


        self.show_answer_var = ctk.BooleanVar()

        if self.showAnswer == 1:
            self.show_answer_var.set(True) 
        elif self.showAnswer == 0:
            self.show_answer_var.set(False) 

        self.show_answer_checkbox = ctk.CTkCheckBox(self.defaultScanScrollableFrame, text='Show Answer', variable=self.show_answer_var)

        self.show_answer_checkbox.place(x=10, y=110)


        self.auto_save_var = ctk.BooleanVar()

        if self.autoSave == 1:
            self.auto_save_var.set(True) 
        elif self.autoSave == 0:
            self.auto_save_var.set(False) 

        self.auto_save_checkbox = ctk.CTkCheckBox(self.defaultScanScrollableFrame, text='Auto Save', variable=self.auto_save_var)
        self.auto_save_checkbox.place(x=160, y=110)


        # bagian kanan =============================================================================

        self.defaultScn_label = ctk.CTkLabel(self, text="Account Setting")
        self.defaultScn_label.place(x=360, y=70)

        self.accountScanScrollableFrame = ctk.CTkScrollableFrame(self, width=300, height=80)
        self.accountScanScrollableFrame.place(x=360, y=100)

        self.aturtampilan = ctk.CTkLabel(self.accountScanScrollableFrame, text="")
        self.aturtampilan.grid(row=0, column=0, padx=0, pady=80, sticky="n")

        self.password_label = ctk.CTkLabel(self.accountScanScrollableFrame, text="Change password")
        self.password_label.place(x=10, y=10)

        self.oldPass_entry = ctk.CTkEntry(self.accountScanScrollableFrame, height=40, width=260, text_color='white',placeholder_text='Old Password',
                        bg_color='transparent', font=('Fresca', 14))
        self.oldPass_entry.place(x=10, y=40)

        self.newPass_entry = ctk.CTkEntry(self.accountScanScrollableFrame, height=40, width=260, text_color='white',placeholder_text='New Password',
                        bg_color='transparent', font=('Fresca', 14))
        self.newPass_entry.place(x=10, y=90)

        self.reset_button = ctk.CTkButton(self.accountScanScrollableFrame, text="Reset account", width=130, height=35, fg_color="#a13535", hover_color="#a61717")
        self.reset_button.place(x=10, y=150)

        self.delete_button = ctk.CTkButton(self.accountScanScrollableFrame, text="Delete account", width=130, height=35, fg_color="#a13535", hover_color="#a61717")
        self.delete_button.place(x=150, y=150)

        # Menambahkan tombol untuk menyimpan pengaturan
        self.save_button = ctk.CTkButton(self, text="Save", height=35, command=lambda:
        self.simpan_pengaturan(self.id_login,self.ambilCam(),self.subject_box.get(),self.show_answer_checkbox.get(),self.auto_save_checkbox.get()))
        self.save_button.place(x=540, y=330)
    
        # self.dumpSQL()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # function ======================================================================================================


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Unsaved changes will be discarded, continue?"): 
            self.conn.close()
            self.destroy()


    def cek(self, boolCek):
        if boolCek:
            return 1
        else:
            return 0
        

    def simpan_pengaturan(self, login, camera, subject, showAns, autoSV):
        self.conn.execute("UPDATE settings SET cameraNo=?, def_subject=?, showAnswer=?, autoSave=? WHERE id_login=?", (camera, subject, self.cek(showAns), self.cek(autoSV), login))
        self.conn.commit()
        self.mesg = self.updatePass()

        messagebox.showinfo('Setting', self.mesg)
        self.conn.close()
        self.destroy()


    def dumpSQL(self):
        with open('database.txt', 'w') as f:
            for line in self.conn.iterdump():
                f.write('%s\n' % line)


    def ambilCam(self):
        if self.camera_box.get() == "Default webcam":
            return 0
        else : 
            return 1


    def updatePass(self):
        self.newPass = self.newPass_entry.get()
        self.oldPass = self.oldPass_entry.get()

        self.cur.execute("SELECT password FROM logins WHERE login_id=?",(self.id_login,))
        self.passW = self.cur.fetchone()[0]
    
        if not all([self.newPass, self.oldPass]):
            return "Settings updated!"
        elif self.oldPass != self.passW:
            messagebox.showerror("Invalid", "Old password and current password doesn't match!")
            return "Settings updated!"
        else: 
            self.conn.execute("UPDATE logins SET password=? WHERE login_id=?", (self.newPass,self.id_login))
            self.conn.commit()
            return "Settings and password updated!"




