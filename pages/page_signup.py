import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from PIL import Image

from modules import general_functions as func, db_helper as dbhlp
from . import page_signin as signin


class page_signup(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OMRay | Sign Up")
        self.geometry('925x500+400+200')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        # Buat Background

        self.imgbg = ctk.CTkImage(light_image=Image.open("assets/images/bg_wall.png"), size=(1000, 650))
        self.l1=ctk.CTkLabel(master=self, image=self.imgbg, text=None)
        self.l1.place(x=0, y=0)

        # Atur tampilan

        self.frame = ctk.CTkFrame(self, corner_radius=25, width=350, height=390, bg_color='transparent')
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.heading = ctk.CTkLabel(self.frame, text='SIGN UP', text_color='#FFF', bg_color='transparent',
                        font=('Fugaz One', 28, 'bold'))
        self.heading.place(relx=0.5, y=40, anchor=CENTER)

        # Entry (Input text)

        # username --------------------------------------

        self.user = ctk.CTkEntry(self.frame, width=260, height=40, text_color='white', 
                            placeholder_text='Username', bg_color='transparent', font=('Fresca', 18))
        self.user.place(relx=0.5, y=100, anchor=CENTER)

        # password --------------------------------------

        self.code = ctk.CTkEntry(self.frame, width=260, height=40, text_color='white', 
                            placeholder_text='Password', bg_color='transparent', font=('Fresca', 18))
        self.code.place(relx=0.5, y=160, anchor=CENTER)

        # confirm password --------------------------------------

        self.confirm_code = ctk.CTkEntry(self.frame, height=40, width=260, text_color='white', 
                                    placeholder_text='Confirm Password', bg_color='transparent', 
                                    font=('Fresca', 18))
        self.confirm_code.place(relx=0.5, y=220, anchor=CENTER)

        # button --------------------------------------

        self.sign_up = ctk.CTkButton(self.frame, width=260, height=40, text='Sign Up',
                        bg_color='transparent', corner_radius=6, text_color='white', 
                        cursor='hand2', font=('Fugaz One', 24), command=self.signUp_account)
        self.sign_up.pack()
        self.sign_up.place(relx=0.5, y=290, anchor=CENTER)

        self.label = ctk.CTkLabel(self.frame, text="Already have account?", text_color='#fff',
                    bg_color='transparent', font=('Fresca', 16))
        self.label.place(x=74, y=320)

        self.sign_in = ctk.CTkButton(self.frame, width=6, text='Sign In', border_width=0,
                        bg_color='transparent', fg_color="transparent", cursor='hand2', 
                        text_color='#3B92EA', font=('Fresca', 16, 'bold'), command=self.signIn_btn)
        self.sign_in.place(x=220, y=320)

        self.protocol("WM_DELETE_WINDOW", self.onclosing)

    def onclosing(self):
        funct = func.Functions()
        funct.on_closing(self)

    def checkEntryValidity(self, username, password, confirm_password):
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror('Invalid', "All fields required!")
            return False
        elif password != confirm_password:
            messagebox.showerror('Invalid', "Password doesn't match")
            return False
        return True
    
    def cleanEntry(self):
        self.user.delete(0, 'end')
        self.code.delete(0, 'end')
        self.confirm_code.delete(0, 'end')
        self.user.focus()

    def signUp_account(self):
        db_user = dbhlp.DB_User()
        username = self.user.get()
        password = self.code.get()
        confirm_password = self.confirm_code.get()
        if self.checkEntryValidity(username, password, confirm_password):
            if db_user.addUser(username, password):
                # Menambahkan default setting untuk user
                db_setting = dbhlp.DB_Setting()
                db_setting.username = username
                db_setting.password = password
                db_setting.addSetting()
                print("# Success | New user added")
                self.cleanEntry()
                messagebox.showinfo('Sign Up', 'Account created successfully')
            else:
                print("# Error | Username already exists")
                messagebox.showinfo('Sign Up', 'Username already exists')

    def signIn_btn(self):
        self.destroy()
        sign_in_form = signin.page_signin()
        sign_in_form.mainloop()

