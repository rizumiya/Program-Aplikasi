from tkinter import messagebox
import customtkinter as ctk
from tkinter import *

import config as cfg
from modules import db_helper as dbh, general_functions as func


class PageSetting(ctk.CTkToplevel):
    def __init__(self, parent, title, user, passw):
        super().__init__(parent)
        self.title(title)
        self.geometry('700x380+1000+70')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        # Inisialisasi variable utama
        self.funct = func.Functions()
        setting = self.funct.getSettingData(user, passw)

        # Mengisi variable utama
        self.idLogin = setting[1]
        self.selectedCamera = setting[2]
        self.selectedSub = setting[3]
        self.showAnswer = setting[4]
        self.autoSave = setting[5]

        # Ambil daftar subject
        self.subject_names = self.funct.get_subject(self.idLogin)

        # Menambahkan judul

        self.heading = ctk.CTkLabel(self, text='Setting', text_color='#fff', font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)

        # Bagian kiri

        self.defaultScn_label = ctk.CTkLabel(self, text="Default Scanning", font=('Fresca', 16))
        self.defaultScn_label.place(x=20, y=70)

        self.defaultScanScrollableFrame = ctk.CTkScrollableFrame(self, width=300, height=85)
        self.defaultScanScrollableFrame.place(x=20, y=100)

        self.aturtampilan = ctk.CTkLabel(self.defaultScanScrollableFrame, text="", 
                                         font=('Fresca', 16))
        self.aturtampilan.grid(row=0, column=0, padx=0, pady=80, sticky="n")

        self.camera_label = ctk.CTkLabel(self.defaultScanScrollableFrame, text="Camera : ", 
                                         font=('Fresca', 16))
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


        self.subject_label = ctk.CTkLabel(self.defaultScanScrollableFrame, text="Subject : ", 
                                          font=('Fresca', 16))
        self.subject_label.place(x=10, y=50)

        self.subject_box = ctk.CTkOptionMenu(master=self.defaultScanScrollableFrame,
                                    width=190, values=self.subject_names)
        self.subject_box.set(self.selectedSub)
        self.subject_box.place(x=100, y=50)


        self.show_answer_var = ctk.BooleanVar()

        if self.showAnswer == 1:
            self.show_answer_var.set(True) 
        elif self.showAnswer == 0:
            self.show_answer_var.set(False) 

        self.show_answer_checkbox = ctk.CTkCheckBox(self.defaultScanScrollableFrame, 
                                                    text='Show Answer', variable=self.show_answer_var)

        self.show_answer_checkbox.place(x=10, y=90)

        self.auto_save_var = ctk.BooleanVar()

        if self.autoSave == 1:
            self.auto_save_var.set(True) 
        elif self.autoSave == 0:
            self.auto_save_var.set(False) 

        self.auto_save_checkbox = ctk.CTkCheckBox(self.defaultScanScrollableFrame, 
                                                  text='Auto Save', variable=self.auto_save_var)
        self.auto_save_checkbox.place(x=160, y=90)

        self.queperbox_lbl = ctk.CTkLabel(self.defaultScanScrollableFrame, text="Many rows in one table : ",
                                           font=('Fresca', 16))
        self.queperbox_lbl.place(x=10, y=130)

        self.queperbox_entry = ctk.CTkEntry(self.defaultScanScrollableFrame, height=32, width=100, 
                                     text_color='white', bg_color='transparent',placeholder_text="Empty = 10",
                                     font=('Fresca', 16))
        self.queperbox_entry.place(x=190, y=130)

        # Bagian kanan =============================================================================

        self.defaultScn_label = ctk.CTkLabel(self, text="Account Setting", 
                                             font=('Fresca', 16))
        self.defaultScn_label.place(x=360, y=70)

        self.accountScanScrollableFrame = ctk.CTkScrollableFrame(self, width=300, height=80)
        self.accountScanScrollableFrame.place(x=360, y=100)

        self.aturtampilan = ctk.CTkLabel(self.accountScanScrollableFrame, text="", 
                                         font=('Fresca', 16))
        self.aturtampilan.grid(row=0, column=0, padx=0, pady=80, sticky="n")

        self.password_label = ctk.CTkLabel(self.accountScanScrollableFrame, text="Change password", 
                                           font=('Fresca', 16))
        self.password_label.place(x=10, y=10)

        self.oldPass_entry = ctk.CTkEntry(self.accountScanScrollableFrame, height=40, 
                                          width=260, text_color='white',
                                          placeholder_text='Old Password',
                                          bg_color='transparent', font=('Fresca', 14))
        self.oldPass_entry.place(x=10, y=40)

        self.newPass_entry = ctk.CTkEntry(self.accountScanScrollableFrame, height=40, 
                                          width=260, text_color='white',
                                          placeholder_text='New Password',
                                          bg_color='transparent', font=('Fresca', 14))
        self.newPass_entry.place(x=10, y=90)

        self.reset_button = ctk.CTkButton(self.accountScanScrollableFrame, text="Reset account", 
                                          width=130, height=35, fg_color="#a13535", 
                                          hover_color="#a61717")
        self.reset_button.place(x=10, y=150)

        self.delete_button = ctk.CTkButton(self.accountScanScrollableFrame, text="Delete account", 
                                           width=130, height=35, fg_color="#a13535", 
                                           hover_color="#a61717", command=self.deleteAccount)
        self.delete_button.place(x=150, y=150)

        # Menambahkan tombol untuk menyimpan pengaturan
        
        self.save_button = ctk.CTkButton(self, text="Save", height=35, command=self.save_setting_btn)
        self.save_button.place(x=540, y=330)

        self.after(100, self.lift)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Function

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Unsaved changes will be discarded, continue?"): 
            self.destroy()
    
    def ambilCam(self):
        if self.camera_box.get() == "Default webcam":
            return 0
        else : 
            return 1

    def save_setting_btn(self):
        db_sett = dbh.DB_Setting()
        db_sett.cameraNo = self.ambilCam()
        db_sett.def_sub = self.subject_box.get()
        db_sett.showAnswer = self.show_answer_checkbox.get()
        db_sett.autoSave = self.auto_save_checkbox.get()
        db_sett.quePerBox = self.queperbox_entry.get() if self.queperbox_entry.get() != "" else 10
        db_sett.updateSetting(self.idLogin)
        newpas, mesg = self.updatePass()
        messagebox.showinfo('Setting', mesg)
        if newpas:
            self.destroy()
            self.master.destroy()
            cfg.config()
        self.destroy()

    def deleteAccount(self):
        db_user = dbh.DB_User()
        db_subb = dbh.DB_Subject()
        db_sett = dbh.DB_Setting()

        _, data_user = db_user.checkActiveUser()
        if messagebox.askokcancel("Delete account", "Are you sure want to delete your account?"):
            subjects = db_subb.getSubjectASC(data_user[0][0])
            for sub in subjects:
                db_subb.deleteSubName(sub[1])
            db_sett.deleteSetting(data_user[0][0])
            db_user.deleteUser()

            messagebox.showinfo("Success","Account has been deleted")
            self.master.destroy()
            cfg.config()

    def updatePass(self):
        self.newPass = self.newPass_entry.get()
        self.oldPass = self.oldPass_entry.get()

        db_user = dbh.DB_User()
        _, data_user = db_user.checkActiveUser()

        if not all([self.newPass, self.oldPass]):
            return None, "Settings updated!"
        elif self.oldPass != data_user[0][2]:
            messagebox.showerror("Invalid", "Old password doesn't match!")
            return None, "Settings updated!"
        else: 
            db_user.editLoginPass(self.newPass, 'on')
            return 1, "Settings and password updated!"
