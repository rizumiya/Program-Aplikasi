import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
import sqlite3
import os

# Membuat jendela utama
def bukaSetting():
    settingMenu = ctk.CTk()
    settingMenu.title('OMRay | Setting')
    settingMenu.geometry('700x380+680+300')
    settingMenu.resizable(False, False)
    settingMenu.iconbitmap('assets/images/OMRay.ico')


    # ambil data dari database ================================================================

    MYDIR = os.path.dirname(__file__)
    SQLPATH = os.path.join(MYDIR, "assets", "temps", "omr.db")
    global conn
    conn = sqlite3.connect(SQLPATH)
    cur = conn.cursor()

    # contoh kode ambil jawaban dari subject tertentu
    cur.execute('SELECT sub_answer FROM subjects WHERE sub_id = "1"')
    kunci_jwb = cur.fetchall()
    if kunci_jwb:
        jawaban_string = kunci_jwb[0][0]
        jawaban_array = jawaban_string.split(",")
        # kode lainnya di sini
    else:
        print("Data kunci jawaban tidak ditemukan")
    # print(jawaban_array)

    # ambil daftar subject
    cur.execute("SELECT sub_name FROM subjects")
    # simpan hasil query ke dalam array
    data = cur.fetchall()
    subject_names = ['No Subject'] if len(data) == 0 else [row[0] for row in data]

    # ===========================================================================================

    # function

    def ambil_login():
        cur.execute("SELECT login_id FROM logins WHERE status='on'")
        id_long = cur.fetchone()
        return id_long[0]

    id_login = ambil_login()

    cur.execute("SELECT cameraNo, def_subject, showAnswer, autoSave FROM settings WHERE id_login=?",(id_login,))
    rows = cur.fetchall()
    if rows:
        selectedCamera, selectedSub, showAnswer, autoSave = rows[0]


    def on_closing():
        if messagebox.askokcancel("Quit", "Unsaved changes will be discarded, continue?"):
            settingMenu.destroy()


    def optionmenu_callback(choice):
        print("optionmenu dropdown clicked:", choice)


    def cek(boolCek):
        if boolCek:
            return 1
        else:
            return 0
        

    def simpan_pengaturan(login, camera, subject, showAns, autoSV):
        conn.execute("UPDATE settings SET cameraNo=?, def_subject=?, showAnswer=?, autoSave=? WHERE id_login=?", (camera, subject, cek(showAns), cek(autoSV), login))
        conn.commit()

        messagebox.showinfo('Setting', 'Settings updated!')
        settingMenu.destroy()


    def dumpSQL():
        with open('database.txt', 'w') as f:
            for line in conn.iterdump():
                f.write('%s\n' % line)


    dumpSQL()

    # ===========================================================================================
    # Menambahkan judul
    heading = ctk.CTkLabel(settingMenu, text='Setting', text_color='#fff', font=('Fugaz One', 36, 'bold'))
    heading.place(x=20, y=10)

    # bagian kiri
    defaultScn_label = ctk.CTkLabel(settingMenu, text="Default Scanning")
    defaultScn_label.place(x=20, y=70)

    defaultScanScrollableFrame = ctk.CTkScrollableFrame(settingMenu, width=300, height=80)
    defaultScanScrollableFrame.place(x=20, y=100)

    aturtampilan = ctk.CTkLabel(defaultScanScrollableFrame, text="")
    aturtampilan.grid(row=0, column=0, padx=0, pady=80, sticky="n")

    camera_label = ctk.CTkLabel(defaultScanScrollableFrame, text="Camera : ")
    camera_label.place(x=10, y=10)

    options = {
        0: "Default webcam",
        1: "External source"
    }

    caption = options[selectedCamera]
    defaultCam = ctk.StringVar(value=caption)

    camera_box = ctk.CTkOptionMenu(master=defaultScanScrollableFrame,
                                width=190,
                                values=list(options.values()),
                                variable=defaultCam,
                                command=optionmenu_callback)
    camera_box.place(x=100, y=10)

    def ambilCam():
        if camera_box.get() == "Default webcam":
            return 0
        else : 
            return 1

    subject_label = ctk.CTkLabel(defaultScanScrollableFrame, text="Subject : ")
    subject_label.place(x=10, y=60)

    subject_box = ctk.CTkOptionMenu(master=defaultScanScrollableFrame,
                                width=190,
                                values=subject_names,
                                command=optionmenu_callback)
    subject_box.place(x=100, y=60)


    show_answer_var = ctk.BooleanVar()

    if showAnswer == 1:
        show_answer_var.set(True) 
    elif showAnswer == 0:
        show_answer_var.set(False) 

    show_answer_checkbox = ctk.CTkCheckBox(defaultScanScrollableFrame, text='Show Answer', variable=show_answer_var)

    show_answer_checkbox.place(x=10, y=110)


    auto_save_var = ctk.BooleanVar()

    if autoSave == 1:
        auto_save_var.set(True) 
    elif autoSave == 0:
        auto_save_var.set(False) 

    auto_save_checkbox = ctk.CTkCheckBox(defaultScanScrollableFrame, text='Auto Save', variable=auto_save_var)
    auto_save_checkbox.place(x=160, y=110)


    # bagian kanan =============================================================================
    defaultScn_label = ctk.CTkLabel(settingMenu, text="Account Setting")
    defaultScn_label.place(x=360, y=70)

    accountScanScrollableFrame = ctk.CTkScrollableFrame(settingMenu, width=300, height=80)
    accountScanScrollableFrame.place(x=360, y=100)

    aturtampilan = ctk.CTkLabel(accountScanScrollableFrame, text="")
    aturtampilan.grid(row=0, column=0, padx=0, pady=80, sticky="n")

    password_label = ctk.CTkLabel(accountScanScrollableFrame, text="Change password")
    password_label.place(x=10, y=10)

    oldPass_entry = ctk.CTkEntry(accountScanScrollableFrame, height=40, width=260, text_color='white',placeholder_text='Old Password',
                    bg_color='transparent', font=('Fresca', 14))
    oldPass_entry.place(x=10, y=40)

    newPass_entry = ctk.CTkEntry(accountScanScrollableFrame, height=40, width=260, text_color='white',placeholder_text='New Password',
                    bg_color='transparent', font=('Fresca', 14))
    newPass_entry.place(x=10, y=90)

    reset_button = ctk.CTkButton(accountScanScrollableFrame, text="Reset account", width=130, height=35, fg_color="#a13535", hover_color="#a61717")
    reset_button.place(x=10, y=150)

    delete_button = ctk.CTkButton(accountScanScrollableFrame, text="Delete account", width=130, height=35, fg_color="#a13535", hover_color="#a61717")
    delete_button.place(x=150, y=150)

    # Menambahkan tombol untuk menyimpan pengaturan
    save_button = ctk.CTkButton(settingMenu, text="Save", height=35, command=lambda:
    simpan_pengaturan(id_login,ambilCam(),subject_box.get(),show_answer_checkbox.get(),auto_save_checkbox.get()))
    save_button.place(x=540, y=330)


    # Menjalankan aplikasi

    settingMenu.protocol("WM_DELETE_WINDOW", on_closing)

    settingMenu.mainloop()
