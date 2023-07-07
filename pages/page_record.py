import tkinter as tk
import customtkinter as ctk

class PageRecord(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OMRay | Add New Record")
        self.geometry('700x380+300+90')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        self.heading = ctk.CTkLabel(self, text='New Record', text_color='#fff', 
                                    font=('Fugaz One', 36, 'bold'))
        self.heading.place(x=20, y=10)

        # Pilih subject
        self.pilihSublbl = ctk.CTkLabel(self.master, text="Select Subject")
        self.pilihSublbl.place(x=20, y=70)

        self.recBaruFrame = ctk.CTkFrame(self.master, width=250, height=220)
        self.recBaruFrame.place(x=20, y=100)

        self.subject_box = ctk.CTkOptionMenu(master=self.recBaruFrame, width=210, values='les go')  # Kurang values
        self.subject_box.place(x=20, y=20)

        self.clsrmEnt = ctk.CTkEntry(self.recBaruFrame, height=32, width=210, text_color='white', placeholder_text='Classroom', bg_color='transparent', font=('Fresca', 16))
        self.clsrmEnt.place(x=20, y=60)

        self.student_id = tk.IntVar()
        self.cb_use_sid = ctk.CTkCheckBox(self.recBaruFrame, text="Use student id", variable=self.student_id, command=self.show_order_options)
        self.cb_use_sid.place(x=20, y=105)

        self.ordersidlbl = ctk.CTkLabel(self.recBaruFrame, text="Order student id by", state='disabled')
        self.ordersidlbl.place(x=20, y=140)

        self.order_student_id = ['Ascending', 'Descending']
        self.order_sid_opt = ctk.CTkOptionMenu(master=self.recBaruFrame, width=210, values=self.order_student_id, state='disabled')  # Kurang values
        self.order_sid_opt.place(x=20, y=170)

    def show_order_options(self):
        if self.student_id.get() == 1:
            self.ordersidlbl.configure(state="normal")
            self.order_sid_opt.configure(state="normal")
        else:
            self.ordersidlbl.configure(state="disabled")
            self.order_sid_opt.configure(state="disabled")

app = PageRecord()
app.mainloop()
