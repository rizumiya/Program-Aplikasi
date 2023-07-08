import tkinter as tk
import customtkinter as ctk
import config as cfg

class PageRecord(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OMRay | Add New Record")
        self.geometry('800x385+60+65')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

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
        self.subject_box = ctk.CTkOptionMenu(master=self.recBaruFrame, width=210, values='les go')  # Kurang values
        self.subject_box.place(x=20, y=20)

        self.scdsubjlbl = ctk.CTkLabel(self.recBaruFrame, text="Question Behaviour")
        self.scdsubjlbl.place(x=20, y=60)

        # question behaviour
        self.multichoice = ['regular multiple choice', 'complex multiple choice', 'combined']
        self.selected_option = tk.StringVar()
        self.selected_option.set(self.multichoice[0])
        self.multichoice_box = ctk.CTkOptionMenu(master=self.recBaruFrame, width=210,
                                                 values=self.multichoice,
                                                 variable=self.selected_option,
                                                 command=self.que_behav_opt)
        self.multichoice_box.place(x=20, y=90)

        # subject ke 2 jika combined terpilih
        self.scdsubjlbl = ctk.CTkLabel(self.recBaruFrame, text="Second Subject", state='disabled')
        self.scdsubjlbl.place(x=20, y=130)

        self.second_subject = ctk.CTkOptionMenu(master=self.recBaruFrame, width=210, state='disabled')
        self.second_subject.place(x=20, y=160)

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
        self.cd_save_result = ctk.CTkCheckBox(self.resultFrame, border_width=2,
                                              text="Save result", 
                                              variable=self.saveresult_val, 
                                              command=self.result_opt)
        self.cd_save_result.place(x=20, y=20)
        
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
                                           state='disabled')
        self.totstudent_lbl.place(x=140, y=60)

        self.totstudEntry = ctk.CTkEntry(self.resultFrame, height=32, width=100, 
                                     text_color='white', state='disabled',
                                     bg_color='transparent')
        self.totstudEntry.place(x=140, y=90)

        self.ordersidlbl = ctk.CTkLabel(self.resultFrame, 
                                        text="Order student id by", 
                                        state='disabled')
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

        self.backBtn = ctk.CTkButton(self.master, text="Back", height=35, command=self.onclosing)
        self.backBtn.place(x=20, y=335)

        self.startScan = ctk.CTkButton(self.master, text="Start Scanning", height=35)
        self.startScan.place(x=640, y=335)

        self.protocol("WM_DELETE_WINDOW", self.onclosing)


    # Function
    

    def onclosing(self):
        # Mengembalikan ke pengecekan awal
        self.destroy()
        main_app = cfg.config()
        main_app


    def que_behav_opt(self, selected_option):
        if selected_option == "combined":
            self.second_subject.configure(state="normal")
            self.scdsubjlbl.configure(state="normal")
        else:
            self.second_subject.configure(state="disabled")
            self.scdsubjlbl.configure(state="disabled")


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
