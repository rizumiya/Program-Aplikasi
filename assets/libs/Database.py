import os
import sqlite3

class Database:
    def __init__(self):
        self.SQLPATH = os.path.join(os.path.dirname(__file__), '..', 'temps', 'omr.db')
        self.conn = sqlite3.connect(self.SQLPATH)
        self.cur = self.conn.cursor()

    # buat tabel
    def createTables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS logins (
            login_id integer primary key autoincrement,
            username text,
            password text,
            status text
        )""")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            sub_id integer primary key autoincrement,
            sub_name text,
            sub_totalQuestion integer,
            sub_choices integer,
            sub_answer text
        )""")
        
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            set_id integer primary key autoincrement,
            id_login integer, 
            cameraNo integer, 
            def_subject text, 
            showAnswer integer, 
            autoSave integer
        )""")
        self.conn.commit()

    # login 
    def insert_login(self, username, password, status):
        self.cur.execute("INSERT INTO logins (username, password, status) VALUES (?, ?, ?)", (username, password, status))
        self.conn.commit()


    def update_login(self, login_id, username, password, status):
        self.cur.execute("UPDATE logins SET username=?, password=?, status=? WHERE login_id=?", (username, password, status, login_id))
        self.conn.commit()


    def delete_login(self, login_id):
        self.cur.execute("DELETE FROM logins WHERE login_id=?", (login_id,))
        self.conn.commit()

    # subject
    def insert_subject(self, sub_name, sub_totalQuestion, sub_choices, sub_answer):
        self.cur.execute("INSERT INTO subjects (sub_name, sub_totalQuestion, sub_choices, sub_answer) VALUES (?, ?, ?, ?)", (sub_name, sub_totalQuestion, sub_choices, sub_answer))
        self.conn.commit()


    def update_subject(self, sub_id, sub_name, sub_totalQuestion, sub_choices, sub_answer):
        self.cur.execute("UPDATE subjects SET sub_name=?, sub_totalQuestion=?, sub_choices=?, sub_answer=? WHERE sub_id=?", (sub_name, sub_totalQuestion, sub_choices, sub_answer, sub_id))
        self.conn.commit()


    def delete_subject(self, sub_id):
        self.cur.execute("DELETE FROM subjects WHERE sub_id=?", (sub_id,))
        self.conn.commit()

    # setting
    def insert_setting(self, id_login, cameraNo, def_subject, showAnswer, autoSave):
        self.cur.execute("INSERT INTO settings (id_login, cameraNo, def_subject, showAnswer, autoSave) VALUES (?, ?, ?, ?, ?)", (id_login, cameraNo, def_subject, showAnswer, autoSave))
        self.conn.commit()


    def update_setting(self, set_id, id_login, cameraNo, def_subject, showAnswer, autoSave):
        self.cur.execute("UPDATE settings SET id_login=?, cameraNo=?, def_subject=?, showAnswer=?, autoSave=? WHERE set_id=?", (id_login, cameraNo, def_subject, showAnswer, autoSave, set_id))
        self.conn.commit()


    def delete_setting(self, set_id):
        self.cur.execute("DELETE FROM settings WHERE set_id=?", (set_id,))
        self.conn.commit()


    # operasi select
    def selectAttributes(self, attributes, table, where=None):
        query = "SELECT {} FROM {} ".format(attributes, table)
        if where:
            query += "WHERE {}".format(where)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        if rows:
            datas = []
            for row in rows:
                datas.append(row)
            return datas
        return None

    
    # select active
    def selectActive(self):
        self.cur.execute("SELECT login_id FROM logins WHERE status='on'")
        id_login = self.cur.fetchone()
        if id_login:
            return id_login[0]
        else:
            return None

    
    
    def getAnyID(self, id, table, where):
        query = "SELECT {} FROM {} WHERE {}".format(id, table, where)
        self.cur.execute(query)
        any_id = self.cur.fetchone()[0]
        return any_id