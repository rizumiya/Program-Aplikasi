from tkinter import messagebox
import customtkinter as ctk
from tkinter import *
from typing import List

from modules import db_helper as dbh, general_functions as func
import config as cfg


class page_subject(ctk.CTk):
    def __init__(self, id_login):
        super().__init__()
        self.title("OMRay | Subject")
        self.geometry('700x380+300+90')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        # Inisialisasi variable
        self.id_login = id_login
        self.bykSoal: int = 0
        self.namaSub: str = "No Subject"
        self.bykPilgan: int = 0
        self.subjectName = []
        self.toplevel_window = None

        # Header

        self.heading = ctk.CTkLabel(self, text='Subject', text_color='#fff', 
                                    font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)

        # Bagian kiri

        self.listSubjectlbl = ctk.CTkLabel(self.master, text="Current Subjects")
        self.listSubjectlbl.place(x=20, y=70)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.master, width=110, height=40)
        self.scrollable_frame.place(x=20, y=100)

        self.backBtn = ctk.CTkButton(self.master, text="Back", height=35, command=self.onclosing)
        self.backBtn.place(x=20, y=335)

        # Bagian kanan

        self.buatBarulbl = ctk.CTkLabel(self.master, text="Add new Subject")
        self.buatBarulbl.place(x=165, y=70)

        self.subBaruFrame = ctk.CTkFrame(self.master, width=250, height=220)
        self.subBaruFrame.place(x=165, y=100)

        self.namaSubject = ctk.CTkEntry(self.subBaruFrame, height=32, width=210, 
                                    text_color='white', placeholder_text='Subject name', 
                                    bg_color='transparent', font=('Fresca', 16))
        self.namaSubject.place(x=20, y=20)

        self.banyakSoal = ctk.CTkEntry(self.subBaruFrame, height=32, width=210, 
                                       text_color='white', placeholder_text='Number of questions', 
                                       bg_color='transparent', font=('Fresca', 16))
        self.banyakSoal.place(x=20, y=70)
        
        self.banyakPilgan = ctk.CTkEntry(self.subBaruFrame, height=32, width=210, 
                                         text_color='white', placeholder_text='Number of choices', 
                                         bg_color='transparent', font=('Fresca', 16))
        self.banyakPilgan.place(x=20, y=120)
        
        self.confirmNew = ctk.CTkButton(self.subBaruFrame, text="Confirm", 
                                        height=35, command=self.show_checkbox_window)
        self.confirmNew.place(relx=0.5, y=185, anchor=CENTER)

        # Bagian edit subject

        self.editSub = ctk.CTkLabel(self.master, text="Update existed subject")
        self.editSub.place(x=430, y=70)

        self.subEditFrame = ctk.CTkFrame(self.master, width=250, height=220)
        self.subEditFrame.place(x=430, y=100)

        self.subject_label = ctk.CTkLabel(self.subEditFrame, text="Subject : ")
        self.subject_label.place(x=20, y=10)

        self.action_label = ctk.CTkLabel(self.subEditFrame, text="Action : ")
        self.action_label.place(x=20, y=80)
        
        self.editSubBtn = ctk.CTkButton(self.subEditFrame, text="Edit Subject", height=35)
        self.editSubBtn.place(relx=0.5, y=135, anchor=CENTER)

        self.deleteSubBtn = ctk.CTkButton(self.subEditFrame, text="Delete Subject", 
                                          height=35, fg_color="#a13535", hover_color="#a61717")
        self.deleteSubBtn.place(relx=0.5, y=185, anchor=CENTER)

        self.focused = False

        self.protocol("WM_DELETE_WINDOW", self.onclosing)
        
        self.bind("<FocusIn>", self.on_focus_in)

    # Function

    def updateListSubject(self):
        # Ambil daftar subject
        db_sub = dbh.DB_Subject()
        self.dataSubject = db_sub.getSubjectASC(self.id_login)

        if self.dataSubject is not None:
            self.subject_names = ['No Subject'] if len(self.dataSubject) == 0 else [row[1] for row in self.dataSubject]
        else:
            self.subject_names = ['No Subject']
        self.subjectName = self.subject_names

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.subject_box.destroy()
        self.buatUlangWidget()

        for i, row in enumerate(self.subject_names):
            label = ctk.CTkLabel(self.scrollable_frame, text=row)
            label.grid(row=i, column=0, sticky="w")

    def buatUlangWidget(self):
        self.subject_box = ctk.CTkOptionMenu(master=self.subEditFrame,
                                    width=190,
                                    values=self.subjectName)
        self.subject_box.place(x=20, y=40)

    def on_focus_in(self, _):
        if not self.focused:
            self.focused = True
            self.buatUlangWidget()
            self.updateListSubject()
            self.focused = False
        
    def cleanEntry(self):
        self.banyakSoal.delete(0, 'end')
        self.namaSubject.delete(0, 'end')
        self.banyakPilgan.delete(0, 'end')
        self.namaSubject.focus()
    
    def show_checkbox_window(self):
        if not self.banyakSoal.get().isdigit():
            messagebox.showerror("Error", "Input must be a number")
            return
        else:
            db_sub = dbh.DB_Subject()
            if db_sub.checkSubjectExists(self.id_login, self.namaSub):
                messagebox.showwarning("Duplicate", "Subject already existed")
            else:
                self.bykPilgan = int(self.banyakPilgan.get())
                self.bykSoal = int(self.banyakSoal.get())
                self.namaSub = self.namaSubject.get()
                self.open_toplevel()
                self.cleanEntry()
    
    def open_toplevel(self):
        if self.bykSoal == 0:
            messagebox.showerror("Error", "Number of questions not set")
            return
        elif self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = checkBoxWindow(self.id_login, self.bykPilgan, self.bykSoal, self.namaSub)
        else:
            self.toplevel_window.focus()

    def onclosing(self):
        # Mengembalikan ke pengecekan awal
        self.destroy()
        main_app = cfg.config()
        main_app

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class checkBoxWindow(ctk.CTkToplevel):
    def __init__(self, id_login, bykPilgan, bykSoal, namaSub):
        super().__init__()
        self.title("OMRay | Subject")
        self.geometry('500x280+1200+90')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        # Insialisasi variable utama

        self.checkbox_values = []
        self.id_login: int = id_login
        self.jawaban: str = ""
        self.namaSub: str = namaSub
        self.banyakPilihan: int = bykPilgan
        self.banyakSoal: int = bykSoal

        # Iterasi nomor
        self.nomorKe: int = 0
        self.nomorKe += 1

        # Atur widget 

        ctk.CTkLabel(self, text="", width=500, height=120).grid(row=0, column=0, columnspan=self.banyakPilihan)

        self.heading = ctk.CTkLabel(self, text='Add Answer Key', text_color='#fff', font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)
        
        ctk.CTkLabel(self, text="Question number " + str(self.nomorKe)).place(relx=0.5, y=90, anchor=CENTER)

        # Perulangan untuk membuat widget checkbox

        self.checkbox_vars = [ctk.IntVar() for i in range(self.banyakPilihan)]
        for i, var in enumerate(self.checkbox_vars):
            ctk.CTkCheckBox(self, text=chr(i+97), variable=var, width=10).grid(row=1, column=i)

        self.checkbox_submit_button = ctk.CTkButton(self, text="Submit", height=35, command=self.save_checkbox_values)
        self.checkbox_submit_button.place(relx=0.5, y=200, anchor=CENTER)

    # Function

    def save_checkbox_values(self):
        self.nomorKe += 1
        ctk.CTkLabel(self, text="Question number " + str(self.nomorKe)).place(relx=0.5, y=90, anchor=CENTER)

        if all(var.get() == 0 for var in self.checkbox_vars):
            messagebox.showerror("Invalid", "Please select at least one answer")
            self.nomorKe -= 1
            return
        else:
            # Process the selected checkboxes
            for i, var in enumerate(self.checkbox_vars):
                if var.get() == 1:
                    self.checkbox_values.append(i)

        for var in self.checkbox_vars:
            var.set(0)

        if len(self.checkbox_values) == int(self.banyakSoal):
            self.grab_release()
            self.saveToDatabase()
            self.destroy()


    def saveToDatabase(self):
        self.myfunc = func.Functions()
        self.jawaban = self.myfunc.convertArraykeString(self.checkbox_values)
        self.checkbox_values.clear()

        db_sub = dbh.DB_Subject()
        insertNewSubject = db_sub.addSubject(
            self.id_login, 
            self.namaSub, 
            self.banyakSoal, 
            self.banyakPilihan, 
            self.jawaban
        )

        if insertNewSubject:
            messagebox.showinfo("Success", "Subject "+ self.namaSub +" added!")
            self.destroy()
        else:
            messagebox.showwarning("Invalid", "Double check before submit")