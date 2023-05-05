from tkinter import messagebox
import customtkinter as ctk
from tkinter import *
import tkinter as tk

banyakSoal = 0

class checkboxWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("OMRay | Subject")
        self.geometry('300x380+1000+70')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        # variable

        self.checkbox_values = []
        print(banyakSoal)

        # perulangan untuk membuat widget checkbox

        self.checkbox_vars = [ctk.IntVar() for i in range(4)]
        for i, var in enumerate(self.checkbox_vars):
            checkbox = ctk.CTkCheckBox(self, text=chr(i+97), variable=var)
            checkbox.grid(row=0, column=i)

        self.checkbox_submit_button = ctk.CTkButton(self, text="Submit", command=self.save_checkbox_values)
        self.checkbox_submit_button.grid(row=1, column=2)

    # function

    def save_checkbox_values(self):
        for i, var in enumerate(self.checkbox_vars):
            if var.get() == 1:
                self.checkbox_values.append(i)
        
        for var in self.checkbox_vars:
            var.set(0)

        if len(self.checkbox_values) == int(banyakSoal):
            self.grab_release()
            self.destroy()
            print(self.checkbox_values)
            self.checkbox_values.clear()


class CustomTkinterApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("OMRay | Subject")
        self.geometry('700x380+500+70')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        self.toplevel_window = None

        self.banyakSoal = ctk.CTkEntry(self.master)
        self.banyakSoal.pack()

        self.submit_button = ctk.CTkButton(self.master, text="Submit", command=self.show_checkbox_window)
        self.submit_button.pack()


    def show_checkbox_window(self):
        global banyakSoal   
        if not self.banyakSoal.get().isdigit():
            messagebox.showerror("Error", "Input must be a number")
            return
        else:
            banyakSoal = int(self.banyakSoal.get())
            self.open_toplevel()
    

    def open_toplevel(self):
        if banyakSoal == 0:
            messagebox.showerror("Error", "banyakSoal value not set")
            return
        elif self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = checkboxWindow(self)
        else:
            self.toplevel_window.focus()



if __name__ == "__main__":
    app = CustomTkinterApp()
    app.mainloop()
