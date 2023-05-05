import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from PIL import Image
import sqlite3
import os

class SignupForm(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OMRay | Sign Up")
        self.geometry('925x500+400+200')
        self.resizable(False, False)
        self.iconbitmap('./assets/images/OMRay.ico')

        self.SQLPATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'temps', 'omr.db')
        global conn
        self.conn = sqlite3.connect(self.SQLPATH)
        self.cur = self.conn.cursor()


        self.imgbg = ctk.CTkImage(light_image=Image.open("./assets/images/bg_wall.png"), size=(1000, 650))
        self.l1=ctk.CTkLabel(master=self, image=self.imgbg, text=None)
        self.l1.place(x=0, y=0)

        # set tampilan ================================================

        self.frame = ctk.CTkFrame(self, corner_radius=25, width=350, height=390, bg_color='transparent')
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.heading = ctk.CTkLabel(self.frame, text='SIGN UP', text_color='#FFF', bg_color='transparent',
                        font=('Fugaz One', 28, 'bold'))
        self.heading.place(relx=0.5, y=40, anchor=CENTER)

        # entry ========================================================

        # username --------------------------------------

        self.user = ctk.CTkEntry(self.frame, width=260, height=40, text_color='white', 
                            placeholder_text='Username', bg_color='transparent', font=('Fresca', 18))
        self.user.place(relx=0.5, y=100, anchor=CENTER)

        # password --------------------------------------

        self.code = ctk.CTkEntry(self.frame, width=260, height=40, text_color='white', 
                            placeholder_text='Password', bg_color='transparent', font=('Fresca', 18))
        self.code.place(relx=0.5, y=160, anchor=CENTER)

        # confirm password -------------------------------

        self.confirm_code = ctk.CTkEntry(self.frame, height=40, width=260, text_color='white', 
                                    placeholder_text='Confirm Password', bg_color='transparent', 
                                    font=('Fresca', 18))
        self.confirm_code.place(relx=0.5, y=220, anchor=CENTER)

        # button ------------------------------------------

        self.sign_up = ctk.CTkButton(self.frame, width=260, height=40, text='Sign Up',
                        bg_color='transparent', corner_radius=6, text_color='white', 
                        cursor='hand2', font=('Fugaz One', 24), command=self.signup)
        self.sign_up.pack()
        self.sign_up.place(relx=0.5, y=290, anchor=CENTER)

        self.label = ctk.CTkLabel(self.frame, text="Already have account?", text_color='#fff',
                    bg_color='transparent', font=('Fresca', 16))
        self.label.place(x=74, y=320)

        self.sign_in = ctk.CTkButton(self.frame, width=6, text='Sign In', border_width=0,
                        bg_color='transparent', fg_color="transparent", cursor='hand2', 
                        text_color='#3B92EA', font=('Fresca', 16, 'bold'), command=self.signIn_cmd)
        self.sign_in.place(x=220, y=320)

        # Main app---------------------

        self.mainloop()

    # function ====================================================


    def signup(self):
        self.username = self.user.get()
        self.password = self.code.get()
        self.confirm_password = self.confirm_code.get()

        if len(self.username) == 0 or len(self.password) == 0:
            messagebox.showerror('Invalid', "All fields required!")

        elif self.password == self.confirm_password:
            self.conn.execute("INSERT INTO logins(username, password, status) VALUES (?,?, 'off')",
                        (self.username, self.password))
            self.cursor = self.conn.execute("SELECT login_id FROM logins WHERE username=? and password=?",(self.username, self.password))
            self.id_long = self.cursor.fetchone()
            self.conn.execute("INSERT INTO settings(id_login, cameraNo, showAnswer, autoSave) VALUES (?,0,1,1)",(self.id_long[0],))
            self.conn.commit()
            messagebox.showinfo('Sign Up', 'Account created successfully')
            self.conn.close()
            self.destroy()
            from pages.LoginForm import LoginForm
            login_form = LoginForm()
            login_form.mainloop()
        else:
            messagebox.showerror('Invalid', "Password doesn't match")


    def signIn_cmd(self):
        self.conn.close()
        self.destroy()
        from pages.LoginForm import LoginForm
        login_form = LoginForm()
        login_form.mainloop()
        
