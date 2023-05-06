from tkinter import messagebox
import customtkinter as ctk
from tkinter import *
import tkinter as tk
import sqlite3
import os
import sys

banyakSoal = 0
namaSub = str
banyakPilihan = 0
subjectName = []

class checkboxWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("OMRay | Subject")
        self.geometry('500x280+1200+90')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        # variable
        
        self.checkbox_values = []
        self.jawaban = str
        global banyakPilihan
        self.nomorKe = 0
        self.nomorKe += 1

        # widget

        ctk.CTkLabel(self, text="", width=500, height=120).grid(row=0, column=0, columnspan=banyakPilihan)

        self.heading = ctk.CTkLabel(self, text='Add Answer Key', text_color='#fff', font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)
        
        ctk.CTkLabel(self, text="Question number " + str(self.nomorKe)).place(relx=0.5, y=90, anchor=CENTER)

        # perulangan untuk membuat widget checkbox

        self.checkbox_vars = [ctk.IntVar() for i in range(banyakPilihan)]
        for i, var in enumerate(self.checkbox_vars):
            ctk.CTkCheckBox(self, text=chr(i+97), variable=var, width=10).grid(row=1, column=i)

        self.checkbox_submit_button = ctk.CTkButton(self, text="Submit", height=35, command=self.save_checkbox_values)
        self.checkbox_submit_button.place(relx=0.5, y=200, anchor=CENTER)

    # function

    def save_checkbox_values(self):
        self.nomorKe += 1
        ctk.CTkLabel(self, text="Question number " + str(self.nomorKe)).place(relx=0.5, y=90, anchor=CENTER)

        for i, var in enumerate(self.checkbox_vars):
            if var.get() == 1:
                self.checkbox_values.append(i)
        
        for var in self.checkbox_vars:
            var.set(0)

        if len(self.checkbox_values) == int(banyakSoal):
            self.grab_release()
            self.saveToDatabase()
            self.destroy()
        

    def saveToDatabase(self):
        from assets.libs.Database import Database
        from assets.libs.Module import Module

        global banyakSoal, namaSub, banyakPilihan
        
        self.database = Database()
        self.module = Module()

        self.jawaban = self.module.convertArraykeString(self.checkbox_values)
        self.checkbox_values.clear()

        self.id_login = self.database.selectActive()
        print(namaSub, banyakSoal, banyakPilihan, self.jawaban, self.id_login)
        if self.database.insert_subject(namaSub, banyakSoal, banyakPilihan, str(self.jawaban), self.id_login):
            messagebox.showinfo("Success", "Subject "+ namaSub +" added!")
            self.destroy()
        else:
            messagebox.showwarning("Invalid", "Double check before submit")



class SubjectPage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("OMRay | Subject")
        self.geometry('700x380+300+90')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        # membuat database

        self.SQLPATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'temps', 'omr.db')
        self.conn = sqlite3.connect(self.SQLPATH)
        self.cur = self.conn.cursor()

        # variable
        
        from assets.libs.Database import Database
        self.toplevel_window = None
        self.database = Database()

        # widget

        self.heading = ctk.CTkLabel(self, text='Subject', text_color='#fff', font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)

        # bagian kiri

        self.listSubjectlbl = ctk.CTkLabel(self.master, text="List of Subjects")
        self.listSubjectlbl.place(x=20, y=70)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.master, width=110, height=40)
        self.scrollable_frame.place(x=20, y=100)

        self.backBtn = ctk.CTkButton(self.master, text="Back", height=35, command=self.kembaliKeMenu)
        self.backBtn.place(x=20, y=335)

        # bagian kanan

        self.buatBarulbl = ctk.CTkLabel(self.master, text="Add new Subject")
        self.buatBarulbl.place(x=165, y=70)

        self.subBaruFrame = ctk.CTkFrame(self.master, width=250, height=220)
        self.subBaruFrame.place(x=165, y=100)

        self.namaSub = ctk.CTkEntry(self.subBaruFrame, height=32, width=210, text_color='white', 
                                       placeholder_text='Subject name', bg_color='transparent', font=('Fresca', 16))
        self.namaSub.place(x=20, y=20)

        self.banyakSoal = ctk.CTkEntry(self.subBaruFrame, height=32, width=210, text_color='white', 
                                       placeholder_text='Number of questions', bg_color='transparent', font=('Fresca', 16))
        self.banyakSoal.place(x=20, y=70)
        
        self.banyakPilgan = ctk.CTkEntry(self.subBaruFrame, height=32, width=210, text_color='white', 
                                       placeholder_text='Number of choices', bg_color='transparent', font=('Fresca', 16))
        self.banyakPilgan.place(x=20, y=120)
        
        self.confirmNew = ctk.CTkButton(self.subBaruFrame, text="Confirm", height=35 ,command=self.show_checkbox_window)
        self.confirmNew.place(relx=0.5, y=185, anchor=CENTER)

        # bagian edit subject

        self.editSub = ctk.CTkLabel(self.master, text="Update existed subject")
        self.editSub.place(x=430, y=70)

        self.subEditFrame = ctk.CTkFrame(self.master, width=250, height=220)
        self.subEditFrame.place(x=430, y=100)

        self.subject_label = ctk.CTkLabel(self.subEditFrame, text="Subject : ")
        self.subject_label.place(x=20, y=10)

        self.action_label = ctk.CTkLabel(self.subEditFrame, text="Action : ")
        self.action_label.place(x=20, y=80)
        
        self.editSubBtn = ctk.CTkButton(self.subEditFrame, text="Edit Subject", height=35 ,command=self.updateSubCmd)
        self.editSubBtn.place(relx=0.5, y=135, anchor=CENTER)

        self.deleteSubBtn = ctk.CTkButton(self.subEditFrame, text="Delete Subject", height=35 ,command=self.deleteSubCmd, fg_color="#a13535", hover_color="#a61717")
        self.deleteSubBtn.place(relx=0.5, y=185, anchor=CENTER)

        self.focused = False
        self.protocol("WM_DELETE_WINDOW", self.kembaliKeMenu)
        self.bind("<FocusIn>", self.on_focus_in)
    

    def deleteSubCmd(self):
        from assets.libs.Database import Database

        self.database = Database()
        if self.subject_box.get() is not "No Subject":
            if messagebox.askokcancel("Subject deletion", "Are you sure want to delete subject " + self.subject_box.get() + "?"):
                self.idSub = self.database.getAnyID('sub_id', 'subjects', 'sub_name="' + str(self.subject_box.get()) + '"' )
                self.row = self.database.selectAttributes('*', 'settings', 'id_login=' + str(self.database.selectActive()))
                self.database.update_setting(self.row[0][0],self.row[0][1],self.row[0][2],"No Subject",self.row[0][4],self.row[0][5])
                if self.database.delete_subject(self.idSub):
                    messagebox.showinfo("Success", "Subject successfully deleted!")
        else: 
            messagebox.showwarning("Error", "No subject selected")


    def updateSubCmd(self):
        messagebox.showwarning("Not available", "This feature is currently unavailable")


    def buatUlangWidget(self):
        global subjectName
        self.subject_box = ctk.CTkOptionMenu(master=self.subEditFrame,
                                    width=190,
                                    values=subjectName)
        self.subject_box.place(x=20, y=40)


    def on_focus_in(self, event):
        if not self.focused:
            self.focused = True
            self.buatUlangWidget()
            self.updateListSubject()
            self.focused = False
    

    def updateListSubject(self):
        global subjectName
        self.dataSubject = self.database.selectAttributes('sub_name', 'subjects', order='sub_name asc')
        if self.dataSubject is not None:
            self.subject_names = ['No Subject'] if len(self.dataSubject) == 0 else [row[0] for row in self.dataSubject]
        else:
            self.subject_names = ['No Subject']
        subjectName = self.subject_names

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.subject_box.destroy()
        self.buatUlangWidget()

        for i, row in enumerate(self.subject_names):
            label = ctk.CTkLabel(self.scrollable_frame, text=row)
            label.grid(row=i, column=0, sticky="w")


    def kembaliKeMenu(self):
        self.destroy()
        from MainMenu import MainMenu
        mainMenu = MainMenu()
        mainMenu.mainloop()

    
    def clearNewSubEntry(self):
        self.namaSub.delete(0, END)
        self.banyakSoal.delete(0, END)
        self.banyakPilgan.delete(0, END)


    def show_checkbox_window(self):
        global banyakSoal, namaSub, banyakPilihan
        if not self.banyakSoal.get().isdigit():
            messagebox.showerror("Error", "Input must be a number")
            return
        else:
            self.cekKembar = self.database.checkExist('sub_name', 'subjects', 'sub_name="' + str(self.namaSub.get()) + '"')
            if self.cekKembar:
                messagebox.showwarning("Duplicate", "Subject already existed")
            else:
                banyakSoal = int(self.banyakSoal.get())
                namaSub = self.namaSub.get()
                banyakPilihan = int(self.banyakPilgan.get())
                self.open_toplevel()
                self.clearNewSubEntry()
    

    def open_toplevel(self):
        if banyakSoal == 0:
            messagebox.showerror("Error", "Number of questions not set")
            return
        elif self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = checkboxWindow(self)
        else:
            self.toplevel_window.focus()



if __name__ == "__main__":
    app = SubjectPage()
    app.mainloop()
