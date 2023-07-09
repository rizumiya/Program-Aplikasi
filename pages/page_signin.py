import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from PIL import Image

from modules import general_functions as func, db_helper as dbhlp
from . import page_signup as signup
import config as cfg

class PageSignIn(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OMRay | Sign In")
        self.geometry('925x500+400+200')
        self.resizable(False, False)
        self.iconbitmap('assets/images/OMRay.ico')

        # Buat Background

        self.imgbg = ctk.CTkImage(light_image=Image.open("assets/images/bg_wall.png"), size=(1000, 650))
        self.l1=ctk.CTkLabel(master=self, image=self.imgbg, text=None)
        self.l1.place(x=0, y=0)

        # Atur tampilan

        self.imgSi = ctk.CTkImage(light_image=Image.open("./assets/images/wp.png"), size=(298, 298))
        ctk.CTkLabel(self, image=self.imgSi, bg_color='transparent', text=None).place(x=60, rely=0.2)

        self.frameSignIn = ctk.CTkFrame(self, corner_radius=25, width=350, height=350, bg_color="transparent")
        self.frameSignIn.place(relx=0.5, y=70)

        self.heading = ctk.CTkLabel(self.frameSignIn, text='SIGN IN', text_color='#FFF', bg_color='transparent',
                        font=('Fugaz One', 28, 'bold'))
        self.heading.place(relx=0.5, y=40, anchor=CENTER)

        # Entry

        # username --------------------------------------

        self.user = ctk.CTkEntry(self.frameSignIn, height=40, width=260, text_color='white', placeholder_text='Username',
                    bg_color='transparent', font=('Fresca', 18))
        self.user.place(relx=0.5, y=100, anchor=CENTER)

        # password --------------------------------------

        self.code = ctk.CTkEntry(self.frameSignIn, height=40, width=260, text_color='white', placeholder_text='Password',
                            bg_color='transparent', font=('Fresca', 18))
        self.code.place(relx=0.5, y=160, anchor=CENTER)

        # button ------------------------------------------

        self.sign_in = ctk.CTkButton(self.frameSignIn, width=260, height=40, text='Sign In',
                                bg_color='transparent', corner_radius=6, text_color='white', 
                                cursor='hand2',font=('Fugaz One', 24), command=self.signIn_account)
        self.sign_in.pack()
        self.sign_in.place(relx=0.5, y=230, anchor=CENTER)

        self.label = ctk.CTkLabel(self.frameSignIn, text="Don't have an account?", text_color='#fff',
                    bg_color='transparent', font=('Fresca', 16))
        self.label.place(x=72, y=260)

        self.sign_up = ctk.CTkButton(self.frameSignIn, width=6, text='Sign Up', border_width=0, 
                                bg_color='transparent', fg_color="transparent", cursor='hand2', 
                                text_color='#3B92EA', font=('Fresca', 16, 'bold'), command=self.signUp_btn)
        self.sign_up.place(x=221, y=260)

        self.protocol("WM_DELETE_WINDOW", self.onclosing)

    # Function

    def checkEntryValidity(self, username, password):
        if len(username) == 0 or len(password) == 0:
            messagebox.showerror('Invalid', "All fields required!")
            return False
        return True
    
    def signUp_btn(self):
        self.destroy()
        sign_up_form = signup.PageSignUp()
        sign_up_form.mainloop()

    def signIn_account(self):
        username = self.user.get()
        password = self.code.get()
        if self.checkEntryValidity(username, password):
            db_helper = dbhlp.db_helper()
            db_helper.table_name = "logins"
            db_helper.condition = "username=? AND password=?"
            db_helper.values = [username, password]
            if db_helper.checkIfdataExists():
                # Ubah nilai status dari username dan password menjadi on
                db_helper.fields = ["status"]
                db_helper.values = ("on", )
                db_helper.condition = "username=? and password=?"
                db_helper.condition_value = (username, password)
                db_helper.changeValue()
                # Mengembalikan ke pengecekan awal
                self.destroy()
                main_app = cfg.config()
                main_app
            else:
                messagebox.showerror('Invalid', "Incorrect Username or Password!")

    def onclosing(self):
        funct = func.Functions()
        funct.on_closing(self)
    
