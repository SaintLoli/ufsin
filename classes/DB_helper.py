import sqlite3

class DBHelper:
    def __init__(self):
        self.con = sqlite3.connect('DB/UFSIN_DB.db', check_same_thread=False)
        self.cur = self.con.cursor()

    def add_user(self, fio, login, password, number, tubel_number):
        self.cur.execute(f"INSERT INTO user (login, password, fio, number, tubel_number) VALUES "
                         f"('{login}', '{password}', '{fio}', '{number}', '{tubel_number}')")
        self.con.commit()

    def check_user(self, login, password):
        if self.cur.execute(f"SELECT * FROM user WHERE login='{login}' and password='{password}'").fetchone():
            return True
        else:
            return False

    def get_user_id(self, login):
        return self.cur.execute(f"SELECT id FROM user WHERE login='{login}'").fetchone()[0]

    def add_computer_info(self, user_id, cpu, motherboard, gpu, ram, year, s_number):
        self.cur.execute(f"INSERT INTO comp (id_user, motherboard, gpu, cpu, ram, year, serial_number)"
                         f" VALUES ('{user_id}', '{cpu}', '{motherboard}', '{gpu}', "
                         f"'{ram}', {year}, '{s_number}')")
        self.con.commit()

    def get_computer_info(self, user_id):
        return self.cur.execute(
            f"SELECT (motherboard, gpu, cpu, ram, year, serial_number) FROM comp WHERE id_user=?", user_id
        ).fetchone()