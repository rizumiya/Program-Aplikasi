from tkinter import messagebox
from tkinter import *
import customtkinter as ctk
import openpyxl as xl
from PIL import Image
import sqlite3
import os

class Module:
    def __init__(self):
        self.SQLPATH = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'temps', 'omr.db')
        self.conn = sqlite3.connect(self.SQLPATH)
        self.cur = self.conn.cursor()





