import os
import customtkinter as ctk
import openpyxl as xl
from tkinter import messagebox, font, ttk


class PageSeeRecord(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('OMRay | See Record')
        self.geometry('900x495+635+230')
        self.resizable(False, False)
        self.iconbitmap(default='assets/images/OMRay.ico')

        self.xlPath = "assets/datas/omray.xlsx"
        self.sheet_name = 'Scanning result'
        self.search_filter_applied = False
        
        # Heading
        
        self.heading = ctk.CTkLabel(self, text='Record History', text_color='#fff', 
                                    font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)

        # Entry untuk Classroom
        
        self.classroom_label = ctk.CTkLabel(self, text="Classroom")
        self.classroom_label.place(x=20, y=70)
        self.classroom_entry = ctk.CTkEntry(self, width=120, font=('Fresca', 16))
        self.classroom_entry.place(x=20, y=100)

        # Entry untuk Student ID
        self.classroom_label = ctk.CTkLabel(self, text="Student ID")
        self.classroom_label.place(x=150, y=70)
        self.student_id_entry = ctk.CTkEntry(self, width=120, font=('Fresca', 16))
        self.student_id_entry.place(x=150, y=100)

        # Entry untuk Subject
        self.classroom_label = ctk.CTkLabel(self, text="Subject")
        self.classroom_label.place(x=280, y=70)
        self.subject_entry = ctk.CTkEntry(self, width=120, font=('Fresca', 16))
        self.subject_entry.place(x=280, y=100)

        # Tombol Cari
        self.search_btn = ctk.CTkButton(self, text="Search", command=self.search_records)
        self.search_btn.place(x=410, y=100)

        # Tombol Reset
        self.reset_btn = ctk.CTkButton(self, text="\u27F2", width=80, command=self.reset_filter)
        self.reset_btn.place(x=800, y=100)

        # scrollable frame

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=840, height=340)
        self.scrollable_frame.place(x=20, y=150)

        self.tree = self.loadExcel()
        self.update_treeview()

        self.after(300, self.lift)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    # Function

    def on_closing(self):
        self.destroy()

    def search_records(self):
        classroom = self.classroom_entry.get()
        student_id = self.student_id_entry.get()
        subject = self.subject_entry.get()

        self.filtered_data = []
        if classroom == "" and student_id == "" and subject == "":
            messagebox.showwarning("Invalid", "Fill atleast one field")
            self.after(100, self.lift)
            return
        else:
            self.tree.delete(*self.tree.get_children()) 

            self.tree.config(columns=self.cols)
            for col_name in self.cols:
                self.tree.heading(col_name, text=col_name)
                self.tree.column(col_name, width=font.Font().measure(col_name))

            for value_data in self.list_data[1:]:
                if (
                    (classroom == "" or classroom in value_data) and
                    (student_id == "" or int(student_id) in value_data) and
                    (subject == "" or subject in value_data)
                ):
                    self.tree.insert("", 'end', values=value_data)
                    self.filtered_data.append(value_data)

            self.classroom_entry.delete(0, 'end')
            self.student_id_entry.delete(0, 'end')
            self.subject_entry.delete(0, 'end')
            self.reset_btn.focus()

            self.search_filter_applied = True

    def loadExcel(self):
        self.workbook = xl.load_workbook(self.xlPath)
        self.sheet = self.workbook[self.sheet_name]
        self.list_data = list(self.sheet.values)
        self.cols = self.list_data[0]

        self.tree = ttk.Treeview(self.scrollable_frame, columns=self.cols, show="headings", height=19)
        for self.col_name in self.cols:
            self.tree.heading(self.col_name, text=self.col_name)
            self.tree.column(self.col_name, width=font.Font().measure(self.col_name))
        self.tree.pack(expand=True, fill="both")

        for self.value_data in self.list_data[1:]:
            self.tree.insert('', 'end', values=self.value_data)
        return self.tree

    def reset_filter(self):
        self.search_filter_applied = False
        self.tree.delete(*self.tree.get_children())
        self.tree.config(columns=self.cols)

        for value_data in self.list_data[1:]:
            self.tree.insert("", 'end', values=value_data)

    def update_treeview(self):
        if self.search_filter_applied:
            # Gunakan data yang telah difilter saat pencarian
            self.tree.delete(*self.tree.get_children())
            self.tree.config(columns=self.cols)

            for col_name in self.cols:
                self.tree.heading(col_name, text=col_name)
                self.tree.column(col_name, width=font.Font().measure(col_name))

            for value_data in self.filtered_data:
                self.tree.insert("", 'end', values=value_data)
        else:
            # Gunakan semua data
            self.workbook = xl.load_workbook(self.xlPath)
            self.sheet = self.workbook[self.sheet_name]
            self.list_data = list(self.sheet.values)
            self.cols = self.list_data[0]
            self.tree.delete(*self.tree.get_children())
            self.tree.config(columns=self.cols)

            for col_name in self.cols:
                self.tree.heading(col_name, text=col_name)
                self.tree.column(col_name, width=font.Font().measure(col_name))

            for value_data in self.list_data[1:]:
                self.tree.insert("", 'end', values=value_data)

        self.after(100, self.update_treeview)
