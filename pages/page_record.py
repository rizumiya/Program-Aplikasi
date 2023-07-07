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

        self.subject_box = ctk.CTkOptionMenu(master=self.recBaruFrame,
                                    width=190, values='les go') # kurang values
        self.subject_box.place(x=20, y=20)


app = PageRecord()
app.mainloop()
