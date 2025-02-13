import sqlite3
import hashlib

class DBHelper:
    def __init__(self):
        self.con = sqlite3.connect('DB/UFSIN_DB.db', check_same_thread=False)
        self.cur = self.con.cursor()

    def add_user(self, fio, login, password, number, tubel_number, dep):
        self.cur.execute(f"INSERT INTO user (login, password, fio, number, tubel_number, office) VALUES "
                         f"(?, ?, ?, ?, ?, ?)",
                         (login, hashlib.md5(password.encode()).hexdigest(), fio, number, tubel_number, self.get_dep_id_by_name(dep)[0]))
        self.con.commit()

    def check_user(self, login, password):
        if self.cur.execute(f"SELECT * FROM user WHERE login=? and password=?", (login, hashlib.md5(password.encode()).hexdigest())).fetchone():
            return True
        else:
            return False

    def get_user_id(self, login):
        return self.cur.execute(f"SELECT id FROM user WHERE login='{login}'").fetchone()[0]

    def add_computer_info(self, user_id, cpu, motherboard, gpu, ram, year, s_number):
        self.cur.execute(f"INSERT INTO comp (id_user, motherboard, gpu, cpu, ram, year, serial_number)"
                         f" VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (user_id, cpu, motherboard, gpu, ram, year, s_number))
        self.con.commit()

    def get_computer_info(self, user_id):
        return self.cur.execute(
            f"SELECT motherboard, gpu, cpu, ram, year, serial_number FROM comp WHERE id_user=?", str(user_id)
        ).fetchone()

    def get_item(self, item, user_id):
        return self.cur.execute(f"SELECT name FROM {item} WHERE id_user=?", str(user_id)).fetchone()

    def get_users(self):
        return self.cur.execute(
            f"SELECT fio, role, office, number, tubel_number FROM user"
        ).fetchall()

    def get_departments(self):
        return self.cur.execute(
            """
            SELECT key, name, user.fio, address, phone FROM offices 
            LEFT  JOIN user ON offices.supervisor == user.id;
            """
        ).fetchall()

    def get_warehouses(self):
        return self.cur.execute(
            """
            SELECT name, address, user.fio FROM sklad 
            LEFT JOIN user ON sklad.supervisor == user.id;
            """
        ).fetchall()

    def get_dep_id_by_name(self, dep_name):
        return self.cur.execute(
            "SELECT id FROM offices WHERE name=?", (dep_name, )
        ).fetchone()

    def get_dep_name_by_id(self, dep_id):
        req = self.cur.execute(
            "SELECT name FROM offices WHERE id=?", (dep_id, )
        ).fetchone()
        if req:
            return req[0]
        else:
            return None

    def generate_otchet_sklad(self, date_start, date_end):
         return self.cur.execute(
             f"SELECT id_item, type_item, id_stock "
             f"FROM item WHERE arrival_time >= ? AND arrival_time <= ?", (date_start, date_end)).fetchall()


    def get_warehouse_by_id(self, id):
        return self.cur.execute(
            "SELECT name FROM sklad WHERE id=?", (id, )
        ).fetchone()[0]

    def get_item_name_by_type(self, id, type):
        return self.cur.execute(
            f"SELECT name FROM {type} WHERE id=?", (id, )
        ).fetchone()[0]