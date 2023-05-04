from tkinter import messagebox
from tkinter import *
import customtkinter as ctk
from pages.signUp import showSignUp
from PIL import Image
import sqlite3
import os
import sys

MYDIR = os.path.dirname(__file__)
module_dir = os.path.abspath(os.path.join(MYDIR, '..'))
sys.path.append(module_dir)

# Mengimpor file my_module.py
from Main_menu import mainMenu, on_closing

SQLPATH = os.path.join(MYDIR, "assets", "temps", "omr.db")
global conn
conn = sqlite3.connect(SQLPATH)


# toplevel
def showSignIn():
    signInWd = ctk.CTkToplevel(mainMenu)
    signInWd.title('OMRay | Sign In')
    signInWd.geometry('925x500+400+200')
    signInWd.resizable(False, False)
    signInWd.iconbitmap('assets/images/OMRay.ico')

    # set tampilan ================================================

    imgSi = ctk.CTkImage(light_image=Image.open("assets/images/wp.png"), size=(298, 298))
    ctk.CTkLabel(signInWd, image=imgSi, bg_color='transparent', text=None).place(x=60, rely=0.2)

    frameSignIn = ctk.CTkFrame(signInWd, corner_radius=25, width=350, height=350, bg_color="transparent")
    frameSignIn.place(relx=0.5, y=70)

    heading = ctk.CTkLabel(frameSignIn, text='SIGN IN', text_color='#FFF', bg_color='transparent',
                    font=('Fugaz One', 28, 'bold'))
    heading.place(relx=0.5, y=40, anchor=CENTER)

    # function ====================================================

    def signInCmd():
        username = user.get()
        password = code.get()

        cursor = conn.execute(
            'SELECT * FROM logins WHERE username="%s" and password="%s"' % (username, password))
        if cursor.fetchone():
            conn.execute(
                "UPDATE logins SET status = 'on' WHERE username=? and password=?", (username, password))
            conn.commit()
            mainMenu.deiconify()
            signInWd.destroy()
        else:
            messagebox.showerror("Invalid", "invalid username or password")

    def signUp_cmd():
        signInWd.destroy()
        showSignUp()

    # entry ========================================================

    # username --------------------------------------

    user = ctk.CTkEntry(frameSignIn, height=40, width=260, text_color='white', placeholder_text='Username',
                 bg_color='transparent', font=('Fresca', 18))
    user.place(relx=0.5, y=100, anchor=CENTER)

    # password --------------------------------------

    code = ctk.CTkEntry(frameSignIn, height=40, width=260, text_color='white', placeholder_text='Password',
                        bg_color='transparent', font=('Fresca', 18))
    code.place(relx=0.5, y=160, anchor=CENTER)

    # button ------------------------------------------

    sign_in = ctk.CTkButton(frameSignIn, width=260, height=40, text='Sign In',
                            bg_color='transparent', corner_radius=6, text_color='white', 
                            cursor='hand2',font=('Fugaz One', 24), command=signInCmd)
    sign_in.pack()
    sign_in.place(relx=0.5, y=230, anchor=CENTER)

    label = ctk.CTkLabel(frameSignIn, text="Don't have an account?", text_color='#fff',
                  bg_color='transparent', font=('Fresca', 16))
    label.place(x=72, y=260)

    sign_up = ctk.CTkButton(frameSignIn, width=6, text='Sign Up', border_width=0, 
                            bg_color='transparent', fg_color="transparent", cursor='hand2', 
                            text_color='#3B92EA', font=('Fresca', 16, 'bold'), command=signUp_cmd)
    sign_up.place(x=221, y=260)

    signInWd.protocol("WM_DELETE_WINDOW", on_closing)
    signInWd.mainloop()
