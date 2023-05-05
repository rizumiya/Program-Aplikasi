import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from PIL import Image
import sqlite3
import os

class LoginForm(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OMRay | Sign In")
        self.geometry('925x500+400+200')
        self.resizable(False, False)
        self.iconbitmap('./assets/images/OMRay.ico')

        # creating database

        self.SQLPATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'temps', 'omr.db')
        global conn
        self.conn = sqlite3.connect(self.SQLPATH)
        self.cur = self.conn.cursor()

        # set tampilan ================================================

        self.imgSi = ctk.CTkImage(light_image=Image.open("./assets/images/wp.png"), size=(298, 298))
        ctk.CTkLabel(self, image=self.imgSi, bg_color='transparent', text=None).place(x=60, rely=0.2)

        self.frameSignIn = ctk.CTkFrame(self, corner_radius=25, width=350, height=350, bg_color="transparent")
        self.frameSignIn.place(relx=0.5, y=70)

        self.heading = ctk.CTkLabel(self.frameSignIn, text='SIGN IN', text_color='#FFF', bg_color='transparent',
                        font=('Fugaz One', 28, 'bold'))
        self.heading.place(relx=0.5, y=40, anchor=CENTER)

        # entry ========================================================

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
                                cursor='hand2',font=('Fugaz One', 24), command=self.signInCmd)
        self.sign_in.pack()
        self.sign_in.place(relx=0.5, y=230, anchor=CENTER)

        self.label = ctk.CTkLabel(self.frameSignIn, text="Don't have an account?", text_color='#fff',
                    bg_color='transparent', font=('Fresca', 16))
        self.label.place(x=72, y=260)

        self.sign_up = ctk.CTkButton(self.frameSignIn, width=6, text='Sign Up', border_width=0, 
                                bg_color='transparent', fg_color="transparent", cursor='hand2', 
                                text_color='#3B92EA', font=('Fresca', 16, 'bold'), command=self.signUp_cmd)
        self.sign_up.place(x=221, y=260)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    # function ====================================================


    def signInCmd(self):
        self.username = self.user.get()
        self.password = self.code.get()

        self.cursor = self.conn.execute(
            'SELECT * FROM logins WHERE username="%s" and password="%s"' % (self.username, self.password))
        if self.cursor.fetchone():
            self.conn.execute(
                "UPDATE logins SET status = 'on' WHERE username=? and password=?", (self.username, self.password))
            self.conn.commit()
            self.conn.close()
            self.destroy()
            from MainMenu import MainMenu
            mainMenu = MainMenu()
            mainMenu.mainloop()
        else:
            messagebox.showerror("Invalid", "invalid username or password")


    def signUp_cmd(self):
        self.conn.close()
        self.destroy()
        from pages.SignupForm import SignupForm
        signup_form = SignupForm()
        signup_form.mainloop()

    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.conn.close()
            self.destroy()
