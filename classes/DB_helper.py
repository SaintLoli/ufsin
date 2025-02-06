import sqlite3

class DBHelper:
    def __init__(self):
        self.con = sqlite3.connect('DB/UFSIN_DB.db', check_same_thread=False)
        self.cur = self.con.cursor()

    def add_user(self, fio, login, password):
        self.cur.execute(f"INSERT INTO user (login, password, fio) VALUES ('{login}', '{password}', '{fio}')")
        self.con.commit()

    def check_user(self, login, password):
        if self.cur.execute(f"SELECT * FROM user WHERE login='{login}'and password='{password}'").fetchone():
            return True
        else:
            return False