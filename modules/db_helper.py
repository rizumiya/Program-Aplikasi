from . import database as db

from typing import Union

class db_helper:
    def __init__(self):
        self.table_name: str = ""
        self.fields: str = None
        self.condition: str = None
        self.values: str = None
        self.condition_value: Union[int, str] = None

    # Mengecek apakah ada data pada table
    def checkIfdataExists(self):
        dbase = db.Database()
        dataExists = dbase.read_datas(
            table_name=self.table_name,
            fields=self.fields,
            condition=self.condition,
            values=self.values
        )
        try:
            if dataExists[0][0]:
                # Jika data ada
                return True
            # Jika belum ada 
            return False
        except:
            return False
    
    # Ganti nilai suatu data pada table
    def changeValue(self):
        dbase = db.Database()
        dbase.update_data(
            table_name=self.table_name, 
            fields=self.fields, 
            values=self.values, 
            condition=self.condition, 
            condition_values=self.condition_value
        )

    # Ambil id utama pada table
    def getIdFromData(self):
        dbase = db.Database()
        id = dbase.read_datas(
            table_name=self.table_name,
            fields=["id"],
            condition=self.condition,
            values=self.values
        )
        return id[0][0]
    
    # Ambil seluruh data pada table
    def getDataFromTable(self):
        dbase = db.Database()
        rows = dbase.read_datas(
            table_name=self.table_name,
            fields=self.fields,
            condition=self.condition,
            values=self.values
        )
        return rows

    def deleteDataFromTable(self):
        dbase = db.Database()
        dbase.delete_data(
            table_name=self.table_name,
            condition=self.condition,
            values=self.values
        )


class DB_User(db_helper):
    def __init__(self):
        super().__init__()
        self.table_name = "logins"
        self.fields = None

    def checkActiveUser(self):
        dbase = db.Database()
        userActive = dbase.read_datas(
            table_name=self.table_name,
            fields=self.fields,
            condition="status=?",
            values=["on"]
        )
        if userActive:
            # Jika ada user yang aktif
            return True, userActive
        # Jika tidak ada
        return False, None
    
    def checkUsernameExists(self, username):
        dbase = db.Database()
        data = dbase.read_datas(
            table_name=self.table_name,
            fields=self.fields,
            condition="username=?",
            values=[username]
        )
        if data:
            # Jika username sudah ada
            return True
        # Jika belum ada
        return False
    
    def addUser(self, username, password):
        dbase = db.Database()
        self.fields = ["username"]
        self.table_name = "logins"
        if not self.checkUsernameExists(username):
            dbase.create_data(
                table_name=self.table_name, 
                fields=["username", "password", "status"],
                values=[username, password, "off"]
            )
            return True
        return False

    def getIdLogin(self, username, password):
        self.table_name = "logins"
        self.condition = "username=? AND password=?"
        self.values = (username, password)
        idLogin = self.getIdFromData()
        return idLogin
    
    def editLoginPass(self, passw, stat):
        self.table_name = self.table_name
        self.fields=["password"]
        self.values=[passw]
        self.condition=f"status='{stat}'"
        self.changeValue()

    def deleteUser(self):
        self.table_name = self.table_name
        self.condition=f"status='on'"
        self.deleteDataFromTable()


class DB_Setting(db_helper):
    def __init__(self):
        super().__init__()
        self.table_name: str = "settings"
        self.username: str = ""
        self.password: str = ""
        self.cameraNo: int = 0
        self.def_sub: str = ""
        self.showAnswer: int = 0
        self.autoSave: int = 0
        self.quePerBox: int = 10
    
    def getDataSetting(self):
        db_user = DB_User()
        id = db_user.getIdLogin(self.username, self.password)
        self.table_name = self.table_name
        self.condition = "id_login=?"
        self.values = [id]
        rows = self.getDataFromTable()
        return rows

    def addSetting(self):
        dbase = db.Database()
        db_user = DB_User()
        id = db_user.getIdLogin(self.username, self.password)
        dbase.create_data(
                table_name=self.table_name,
                fields=["id_login", "cameraNo", "def_subject", "showAnswer", "autoSave", "quePerBox"],
                values=[id, 0, "No Subject", 1, 1, 10]
            )
        
    def updateSetting(self, id_login):
        self.table_name=self.table_name
        self.fields=["cameraNo", "def_subject", "showAnswer", "autoSave", "quePerBox"]
        self.values=(self.cameraNo, self.def_sub, self.showAnswer, self.autoSave, self.quePerBox)
        self.condition=f"id_login={id_login}"
        self.changeValue()

    def deleteSetting(self, idlogin):
        self.table_name = self.table_name
        self.condition=f"id_login={idlogin}"
        self.deleteDataFromTable()
        

class DB_Subject(db_helper):
    def __init__(self):
        super().__init__()
        self.table_name: str = "subjects"

    def getSubjectASC(self, idLogin):
        self.table_name = self.table_name
        self.condition = "id_login=? ORDER BY sub_name ASC"
        self.values = [idLogin]
        rows = self.getDataFromTable()
        return rows
    
    def checkSubjectExists(self, idLogin, sub_name):
        self.fields = ["sub.sub_name"]
        self.table_name = "subjects as sub JOIN logins ON logins.id = sub.id_login"
        self.condition = "sub.id_login=? AND sub.sub_name=?"
        self.values = [idLogin, sub_name]
        exists = self.getDataFromTable()
        # print(exists)
        if exists:
            return True
        return False
    
    def addSubject(self, idLogin, sub_name, bykSoal, bykPilgan, jawaban):
        dbase = db.Database()
        if not self.checkSubjectExists(idLogin, sub_name):
            dbase.create_data(
                table_name="subjects", 
                fields=["sub_name", "sub_totalQuestion", "sub_choices", "sub_answer", "id_login"],
                values=[sub_name, bykSoal, bykPilgan, jawaban, idLogin]
            )
            return True
        return False
    
    def getDataFromSubName(self, sub_name):
        self.table_name = self.table_name
        self.condition = "sub_name=?"
        self.values = [sub_name]
        rows = self.getDataFromTable()
        return rows[0]

    def deleteSubName(self, sub_name):
        self.table_name = self.table_name
        self.condition = "sub_name=?"
        self.values = [sub_name]
        self.deleteDataFromTable()
