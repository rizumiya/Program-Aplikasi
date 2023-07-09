import os
import sqlite3


class Database:
    def __init__(self):
        self.SQLPATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'datas', 'omr.db')
        self.conn = sqlite3.connect(self.SQLPATH)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS logins (
            id integer primary key autoincrement,
            username text,
            password text,
            status text
        )""")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id integer primary key autoincrement,
            sub_name text,
            sub_totalQuestion integer,
            sub_choices integer,
            sub_answer text,
            id_login integer
        )""")
        
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id integer primary key autoincrement,
            id_login integer, 
            cameraNo integer, 
            def_subject text, 
            showAnswer integer, 
            autoSave integer,
            quePerBox integer
        )""")
        
        self.conn.commit()
        self.dumpSQL()
        self.conn.close()

    def create_data(self, table_name, fields, values):
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"
        self.conn.execute(query, values)
        self.conn.commit()
        self.dumpSQL()
        self.conn.close()

    def read_datas(self, table_name, fields=None, condition=None, values=None):
        query = f"SELECT {', '.join(fields) if fields else '*'} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        if values:
            self.cur.execute(query, values)
        else:
            self.cur.execute(query)
        rows = self.cur.fetchall()
        self.dumpSQL()
        self.conn.close()
        return rows

    def update_data(self, table_name, fields, values, condition=None, condition_values=None):
        set_values = ', '.join([f"{field} = ?" for field in fields])
        query = f"UPDATE {table_name} SET {set_values}"
        if condition:
            query += f" WHERE {condition}"
        if condition_values:
            # print(query)
            self.conn.execute(query, values + condition_values)
        else:
            # print(query, values)
            self.conn.execute(query, values)
        self.conn.commit()
        self.dumpSQL()
        self.conn.close()

    def delete_data(self, table_name, condition=None, values=None):
        query = f"DELETE FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        if values:
            self.conn.execute(query, values)
        else:
            self.conn.execute(query)
        self.conn.commit()
        self.dumpSQL()
        self.conn.close()

    def dumpSQL(self):
        with open('database.txt', 'w') as f:
            for line in self.conn.iterdump():
                f.write('%s\n' % line)



# db = Database("path/to/your/database.db")
# db.create_tables()

# # Contoh penggunaan metode CRUD
# db.create_data("logins", ["username", "password", "status"], ["john", "password", "admin"])
# logins = db.read_datas("logins")
# print(logins)

# db.create_data("subjects", ["sub_name", "sub_totalQuestion", "sub_choices", "sub_answer", "id_login"],
#                  ["Math", 20, 4, "A", 1])
# subjects = db.read_datas("subjects")
# print(subjects)

# db.create_data("settings", ["id_login", "cameraNo", "def_subject", "showAnswer", "autoSave"],
#                  [1, 1, "Math", 1, 0])
# settings = db.read_datas("settings")
# print(settings)

# # Contoh penggunaan join query
# query = """
#     SELECT logins.username, subjects.sub_name
#     FROM logins
#     JOIN subjects ON logins.login_id = subjects.id_login
# """
# results = db.read_datas(None, None, query)
# print(results)

# db = Database("path/to/your/database.db")
# db.create_tables()

# # Contoh penggunaan metode create_record
# db.create_record("logins", ["username", "password", "status"], ["john", "password", "admin"])

# # Contoh penggunaan metode read_records
# logins = db.read_records("logins")
# print(logins)

# # Contoh penggunaan metode update_record
# db.update_record("logins", ["password"], ["new_password"], "username = ?", ["john"])

# # Contoh penggunaan metode delete_record
# db.delete_record("logins", "username = ?", ["john"])

# db.close_connection()
