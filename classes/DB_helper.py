import sqlite3

class DBHelper:
    def __init__(self):
        self.con = sqlite3.connect('DB/UFSIN_DB.db')
        self.cur = self.con.cursor()