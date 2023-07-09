import tkinter as tk
import customtkinter as ctk
import config as cfg

from tkinter import messagebox
from modules import adv_scan_module as asm, general_functions as func

class PageRecord(ctk.CTk):
    def __init__(self, idlogin):
        super().__init__()
        self.title("OMRay | Add New Record")
        self.geometry('800x450+60+65')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        self.funct = func.Functions()
        self.id_login = idlogin
        
        # Ambil subject
        self.subject_names = self.funct.get_subject(self.id_login)

        # Heading

        self.heading = ctk.CTkLabel(self, text='New Record', text_color='#fff', 
                                    font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)

        # Left section

        self.pilihSublbl = ctk.CTkLabel(self.master, 
                                        text="Subject and Questions",
                                        font=('Fresca', 18))
        self.pilihSublbl.place(x=20, y=70)

        # Left frame
        self.recBaruFrame = ctk.CTkFrame(self.master, width=250, height=220)
        self.recBaruFrame.place(x=20, y=100)

        # Subject to use
        self.subject_box = ctk.CTkOptionMenu(master=self.recBaruFrame, width=210, 
                                             values=self.subject_names) 
        self.subject_box.place(x=20, y=20)

        self.scdsubjlbl = ctk.CTkLabel(self.recBaruFrame, text="Question Behaviour",
                                       font=('Fresca', 16))
        self.scdsubjlbl.place(x=20, y=60)

        # question behaviour
        self.multichoice = ['regular multiple choice', 'complex multiple choice']
        self.selected_option = tk.StringVar()
        self.selected_option.set(self.multichoice[0])
        self.multichoice_box = ctk.CTkOptionMenu(master=self.recBaruFrame, width=210,
                                                 values=self.multichoice,
                                                 variable=self.selected_option)
        self.multichoice_box.place(x=20, y=90)
        
        self.show_answer_var = ctk.BooleanVar()
        self.show_answer_checkbox = ctk.CTkCheckBox(self.recBaruFrame, text='Show Answer', 
                                                    border_width=2, variable=self.show_answer_var)
        self.show_answer_checkbox.place(x=20, y=140)

        # Midle section

        self.behavpaperlbl = ctk.CTkLabel(self.master, 
                                          text="Save Results Options", 
                                          font=('Fresca', 18))
        self.behavpaperlbl.place(x=290, y=70)

        # frame tengah
        self.resultFrame = ctk.CTkFrame(self.master, width=260, height=220)
        self.resultFrame.place(x=290, y=100)

        # check box save result
        self.saveresult_val = tk.IntVar()
        self.cb_save_result = ctk.CTkCheckBox(self.resultFrame, border_width=2,
                                              text="Save result", 
                                              variable=self.saveresult_val, 
                                              command=self.result_opt)
        self.cb_save_result.place(x=20, y=20)
        
        # check box student id
        self.student_id = tk.IntVar()
        self.cb_use_sid = ctk.CTkCheckBox(self.resultFrame, border_width=2,
                                          text="Use Student Id", 
                                          variable=self.student_id, 
                                          state='disabled',
                                          command=self.order_options)
        self.cb_use_sid.place(x=125, y=20)

        # entry classroom
        self.classroom_lbl = ctk.CTkLabel(self.resultFrame, text="Classroom", 
                                          state='disabled', font=('Fresca', 16))
        self.classroom_lbl.place(x=20, y=60)

        self.clsrmEnt = ctk.CTkEntry(self.resultFrame, height=32, width=110, 
                                     text_color='white', state='disabled',
                                     bg_color='transparent', font=('Fresca', 16))
        self.clsrmEnt.place(x=20, y=90)

        # max student in classroom
        self.totstudent_lbl = ctk.CTkLabel(self.resultFrame, text="Total students", 
                                           state='disabled', font=('Fresca', 16))
        self.totstudent_lbl.place(x=140, y=60)

        self.totstudEntry = ctk.CTkEntry(self.resultFrame, height=32, width=100, 
                                     text_color='white', state='disabled',
                                     bg_color='transparent', font=('Fresca', 16))
        self.totstudEntry.place(x=140, y=90)

        self.ordersidlbl = ctk.CTkLabel(self.resultFrame, 
                                        text="Order student id by", 
                                        state='disabled', font=('Fresca', 16))
        self.ordersidlbl.place(x=20, y=140)

        # urutan sid
        self.order_student_id = ['Ascending', 'Descending']
        self.order_sid_opt = ctk.CTkOptionMenu(master=self.resultFrame, 
                                               width=210, 
                                               values=self.order_student_id, 
                                               state='disabled')  # Kurang variables
        self.order_sid_opt.place(x=20, y=170)

        # Right section

        self.help_lbl = ctk.CTkLabel(self.master, text="Usage",
                                      font=('Fresca', 18))
        self.help_lbl.place(x=570, y=70)

        # right frame
        self.howtoFrame = ctk.CTkFrame(self.master, width=250, height=220)
        self.howtoFrame.place(x=570, y=100)

        # how to : keyboard
        self.help1_lbl = ctk.CTkLabel(self.howtoFrame, text="Shorcut keys",
                                      font=('Fresca', 18))
        self.help1_lbl.place(x=20, y=20)

        self.help2_lbl = ctk.CTkLabel(self.howtoFrame, text="[r] to rotate camera",
                                      font=('Fresca', 17))
        self.help2_lbl.place(x=20, y=50)
        
        self.help2_lbl = ctk.CTkLabel(self.howtoFrame, text="[s] to skip student",
                                      font=('Fresca', 17))
        self.help2_lbl.place(x=20, y=80)
        
        self.help3_lbl = ctk.CTkLabel(self.howtoFrame, text="[q] to quit scanning",
                                      font=('Fresca', 17))
        self.help3_lbl.place(x=20, y=110)
        
        self.help4_lbl = ctk.CTkLabel(self.howtoFrame, text="[enter] to save result and\ngo to the next student",
                                      font=('Fresca', 17))
        self.help4_lbl.place(x=20, y=145)

        # Bottom section

        self.bottomframe = ctk.CTkFrame(self.master, width=800, height= 52)
        self.bottomframe.place(x=20, y=340)

        self.camera_label = ctk.CTkLabel(self.bottomframe, text="Camera : ", font=('Fresca', 16))
        self.camera_label.place(x=20, y=10)

        self.options = {
            0: "Default webcam",
            1: "External source"
        }

        self.caption = self.options[0]
        self.defaultCam = ctk.StringVar(value=self.caption)

        self.camera_box = ctk.CTkOptionMenu(master=self.bottomframe,
                                    width=150,
                                    values=list(self.options.values()),
                                    variable=self.defaultCam)
        self.camera_box.place(x=80, y=10)

        self.queperbox_lbl = ctk.CTkLabel(self.bottomframe, text="Many rows in one table : ", 
                                           font=('Fresca', 16))
        self.queperbox_lbl.place(x=270, y=10)

        self.queperbox_entry = ctk.CTkEntry(self.bottomframe, height=32, width=100, 
                                     text_color='white', bg_color='transparent', placeholder_text="Empty = 10", 
                                     font=('Fresca', 16))
        self.queperbox_entry.place(x=430, y=10)

        # Button

        self.backBtn = ctk.CTkButton(self.master, text="Back", height=35, command=self.onclosing)
        self.backBtn.place(x=20, y=405)

        self.startScan = ctk.CTkButton(self.master, text="Start Scanning", height=35,
                                       command=self.start_scanning_btn)
        self.startScan.place(x=640, y=405)

        self.protocol("WM_DELETE_WINDOW", self.onclosing)


    # Function
    
    def ambilCam(self):
        if self.camera_box.get() == "Default webcam":
            return 0
        else : 
            return 1
        

    def get_all_value(self):
        if self.queperbox_entry.get() != "" and not self.queperbox_entry.get().isdigit():
            messagebox.showerror("Error", "Input number of rows must be a number")
            return
        
        if self.totstudEntry.get() != "" and not self.totstudEntry.get().isdigit():
            messagebox.showerror("Error", "Input total students must be a number")
            return
        
        # ambil data subject
        self.subject_1 = self.subject_box.get()
        self.behaviour = self.multichoice_box.get()
        self.cam_no = self.ambilCam()
        self.show_answer = self.show_answer_checkbox.get()
        self.queperbox = int(self.queperbox_entry.get()) if self.queperbox_entry.get() != "" else 10
        # print(self.subject_1, self.behaviour, self.cam_no, self.queperbox, self.show_answer)

        # ambil data save result
        self.autosave = 1 if self.saveresult_val.get() == 1 else 0
        self.use_sid = self.student_id.get()
        self.order_sid = self.order_sid_opt.get() if self.student_id.get() == 1 else None
        self.classroom_name = self.clsrmEnt.get() if self.clsrmEnt.get() != "" else None
        self.total_student = int(self.totstudEntry.get()) if self.totstudEntry.get() != "" else None
        # print(self.autosave, self.order_sid, self.classroom_name, self.total_student)

    
    def start_scanning_btn(self):
        self.get_all_value()
        adv_scan = asm.AdvanceScanModule(self.subject_1, self.behaviour, self.cam_no, self.queperbox)
        adv_scan.autosave = self.autosave
        adv_scan.use_sid = self.use_sid
        adv_scan.order_sid = self.order_sid
        adv_scan.classroom_name = self.classroom_name
        adv_scan.total_student = self.total_student
        adv_scan.show_answer = self.show_answer
        adv_scan.start_scanning()


    def result_opt(self):
        if self.saveresult_val.get() == 1:
            self.cb_use_sid.configure(state="normal")
            self.classroom_lbl.configure(state="normal")
            self.clsrmEnt.configure(state="normal")
            self.totstudent_lbl.configure(state="normal")
            self.totstudEntry.configure(state="normal")
        else:
            self.student_id.set(0)
            self.cb_use_sid.configure(state="disabled")
            self.classroom_lbl.configure(state="disabled")
            self.clsrmEnt.configure(state="disabled")
            self.totstudent_lbl.configure(state="disabled")
            self.totstudEntry.configure(state="disabled")
            self.order_sid_opt.configure(state="disabled")
            self.ordersidlbl.configure(state="disabled")


    def order_options(self):
        if self.student_id.get() == 1:
            self.ordersidlbl.configure(state="normal")
            self.order_sid_opt.configure(state="normal")
        else:
            self.ordersidlbl.configure(state="disabled")
            self.order_sid_opt.configure(state="disabled")


    def onclosing(self):
        # Mengembalikan ke pengecekan awal
        self.destroy()
        main_app = cfg.config()
        main_app
