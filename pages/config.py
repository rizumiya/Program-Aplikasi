import assets.libs.scann as scan
from setting import bukaSetting
from Main_menu import mainMenu
from tkinter import messagebox, font, ttk
from tkinter import *
import customtkinter as ctk
import openpyxl as xl
from PIL import Image
import sqlite3
import os
import sys



def autoRun():
    # creating database
    MYDIR = os.path.dirname(__file__)
    SQLPATH = os.path.join(MYDIR, "assets", "temps", "omr.db")
    global conn
    conn = sqlite3.connect(SQLPATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS logins (
        login_id integer primary key autoincrement,
        username text,
        password text,
        status text
    )""")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        sub_id integer primary key autoincrement,
        sub_name text,
        sub_totalQuestion integer,
        sub_choices integer,
        sub_answer text
    )""")
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        set_id integer primary key autoincrement,
        id_login integer, 
        cameraNo integer, 
        def_subject text, 
        showAnswer integer, 
        autoSave integer
    )""")

    # conn.execute("INSERT INTO subjects(sub_name, sub_totalQuestion, sub_choices, sub_answer) VALUES ('Matematika', 20, 5, '2, 3, 1, 2, 3, 2, 2, 3, 1, 3, 1, 2, 2, 2, 3, 2, 1, 1, 1, 4')")

    conn.commit()

    cursor = conn.execute(
        'SELECT * FROM logins WHERE status= "on"')
    if cursor.fetchone():
        mainMenu.deiconify()
    else:
        # hide dashboard ---------
        mainMenu.withdraw()
        showSignIn()
