import assets.libs.scann as scan
from setting import bukaSetting
from tkinter import messagebox, font, ttk
from tkinter import *
import customtkinter as ctk
from PIL import Image
import sqlite3
import os
import sys

# Mendapatkan direktori dari file main.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Mendapatkan direktori dari file my_module.py
module_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Menambahkan direktori tersebut ke dalam sys.path
sys.path.append(module_dir)

# Mengimpor file my_module.py
from Main_menu import mainMenu





# toplevel
def showSignUp():
    signUpWd = ctk.CTkToplevel(mainMenu)
    signUpWd.title("OMRay | Sign Up")
    signUpWd.geometry('925x500+400+200')
    signUpWd.resizable(False, False)
    signUpWd.iconbitmap('assets/images/OMRay.ico')

    imgbg = ctk.CTkImage(light_image=Image.open("assets/images/bg_wall.png"), size=(1000, 650))
    l1=ctk.CTkLabel(master=signUpWd, image=imgbg, text=None)
    l1.place(x=0, y=0)

    # function ====================================================

    def signup():
        username = user.get()
        password = code.get()
        confirm_password = confirm_code.get()

        if len(username) == 0 or len(password) == 0:
            messagebox.showerror('Invalid', "All fields required!")
        elif password == confirm_password:
            conn.execute("INSERT INTO logins(username, password, status) VALUES (?,?, 'off')",
                         (username, password))
            cursor = conn.execute("SELECT login_id FROM logins WHERE username=? and password=?",(username, password))
            id_long = cursor.fetchone()
            conn.execute("INSERT INTO settings(id_login, cameraNo, showAnswer, autoSave) VALUES (?,0,1,1)",(id_long[0],))
            conn.commit()
            messagebox.showinfo('Sign Up', 'Account created successfully')
            signUpWd.destroy()
            showSignIn()
        else:
            messagebox.showerror('Invalid', "Password doesn't match")

    def signIn_cmd():
        signUpWd.destroy()
        showSignIn()

    # set tampilan ================================================

    frame = ctk.CTkFrame(signUpWd, corner_radius=25, width=350, height=390, bg_color='transparent')
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    heading = ctk.CTkLabel(frame, text='SIGN UP', text_color='#FFF', bg_color='transparent',
                    font=('Fugaz One', 28, 'bold'))
    heading.place(relx=0.5, y=40, anchor=CENTER)

    # entry ========================================================

    # username --------------------------------------

    user = ctk.CTkEntry(frame, width=260, height=40, text_color='white', 
                        placeholder_text='Username', bg_color='transparent', font=('Fresca', 18))
    user.place(relx=0.5, y=100, anchor=CENTER)

    # password --------------------------------------

    code = ctk.CTkEntry(frame, width=260, height=40, text_color='white', 
                        placeholder_text='Password', bg_color='transparent', font=('Fresca', 18))
    code.place(relx=0.5, y=160, anchor=CENTER)

    # confirm password -------------------------------

    confirm_code = ctk.CTkEntry(frame, height=40, width=260, text_color='white', 
                                placeholder_text='Confirm Password', bg_color='transparent', 
                                font=('Fresca', 18))
    confirm_code.place(relx=0.5, y=220, anchor=CENTER)

    # button ------------------------------------------

    sign_up = ctk.CTkButton(frame, width=260, height=40, text='Sign Up',
                     bg_color='transparent', corner_radius=6, text_color='white', 
                     cursor='hand2', font=('Fugaz One', 24), command=signup)
    sign_up.pack()
    sign_up.place(relx=0.5, y=290, anchor=CENTER)

    label = ctk.CTkLabel(frame, text="Already have account?", text_color='#fff',
                  bg_color='transparent', font=('Fresca', 16))
    label.place(x=74, y=320)

    sign_in = ctk.CTkButton(frame, width=6, text='Sign In', border_width=0,
                     bg_color='transparent', fg_color="transparent", cursor='hand2', 
                     text_color='#3B92EA', font=('Fresca', 16, 'bold'), command=signIn_cmd)
    sign_in.place(x=220, y=320)

    # Main app---------------------

    signUpWd.mainloop()
