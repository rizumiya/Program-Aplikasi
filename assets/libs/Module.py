from tkinter import messagebox
from tkinter import *
import customtkinter as ctk
import openpyxl as xl
from PIL import Image
import sqlite3
import os

from assets.libs.Database import Database

class Module:
    def __init__(self):
        self.SQLPATH = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'temps', 'omr.db')
        self.conn = sqlite3.connect(self.SQLPATH)
        self.cur = self.conn.cursor()

        # variable
        
        self.database = Database()

    # ambil jawaban dari subject tertentu
    def ambilJawaban(self, sub_name):
        self.id_subject = self.database.getAnyID('sub_id', 'subject', 'sub_name=' + sub_name)
        self.dataJawaban = self.database.selectAttributes('sub_answer', 'subjects', 'sub_id=' + str(self.id_subject))
        if self.dataJawaban:
            self.jawaban_string = self.dataJawaban[0][0]
            self.jawaban_array = self.jawaban_string.split(",")
            # kode lainnya di sini
        else:
            print("Data kunci jawaban tidak ditemukan")
        print(self.jawaban_array)


    def pisah_karakter(text):
        karakter = ', '.join(text)
        return karakter




