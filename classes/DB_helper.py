import sqlite3
import hashlib

class DBHelper:
    def __init__(self):
        self.con = sqlite3.connect('DB/UFSIN_DB.db', check_same_thread=False)
        self.cur = self.con.cursor()

    def add_user(self, fio, number, tubel_number, dep):
        self.cur.execute(f"INSERT INTO user (fio, number, tubel_number, office) VALUES "
                         f"(?, ?, ?, ?, ?, ?)",
                         (fio, number, tubel_number, self.get_dep_id_by_name(dep)[0]))
        self.con.commit()

    def check_user(self, login, password):
        if self.cur.execute(f"SELECT * FROM user WHERE login=? and password=?", (login, hashlib.md5(password.encode()).hexdigest())).fetchone():
            return True
        else:
            return False

    def add_pc_name(self, pc_name):
        self.cur.execute(f"INSERT INTO user (pc_name) VALUES (?)", (pc_name, ))
        self.con.commit()

    def get_user_id(self, login):
        return self.cur.execute(f"SELECT id FROM user WHERE login='{login}'").fetchone()[0]

    def add_computer_info(self, user_id, cpu, motherboard, gpu, ram, year, s_number):
        self.cur.execute(f"INSERT INTO comp (id_user, motherboard, gpu, cpu, ram, year, serial_number)"
                         f" VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (user_id, cpu, motherboard, gpu, ram, year, s_number))
        self.con.commit()

    def get_computer_info(self, user_id):
        return self.cur.execute(
            f"SELECT motherboard, gpu, cpu, ram, year, serial_number FROM comp WHERE id_user=?", (user_id, )
        ).fetchone()

    def get_pc_name_by_user_id(self, user_id):
        return self.cur.execute(
            "SELECT pc_name FROM user WHERE id=?", (user_id, )
        ).fetchone()[0]

    def get_user_id_by_pc_name(self, pc_name):
        req = self.cur.execute(
            f"SELECT id FROM user WHERE pc_name=?", (pc_name, )
        ).fetchone()

        if req:
            return req[0]
        else:
            return None

    def get_item(self, item, user_id):
        return self.cur.execute(f"SELECT name FROM {item} WHERE id_user=?", (user_id, )).fetchone()

    def add_item(self, item_type, name, user_id):
        self.cur.execute(
            f"INSERT INTO {item_type} (id_user, name) VALUES (?, ?)", (user_id, name)
        )
        self.con.commit()

    def get_users(self):
        return self.cur.execute(
            f"SELECT fio, role, office, number, tubel_number FROM user"
        ).fetchall()

    def get_user_fio(self, user_id):
        return self.cur.execute(
            f"SELECT fio FROM user WHERE id = ?", (user_id, )
        ).fetchone()[0]

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