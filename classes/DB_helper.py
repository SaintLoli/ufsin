import sqlite3
import hashlib
from datetime import date


class DBHelper:
    def __init__(self, filepath="DB/UFSIN_DB.db"):
        self.con = sqlite3.connect(filepath, check_same_thread=False)
        self.cur = self.con.cursor()



    def check_user(self, login, password):
        if self.cur.execute(f"SELECT * FROM user WHERE login=? and password=?",
                            (login, hashlib.md5(password.encode()).hexdigest())).fetchone():
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
        if item != "other":
            return self.cur.execute(f"SELECT name, id FROM {item} WHERE id_user=?", (user_id, )).fetchall()
        else:
            return self.cur.execute(f"SELECT name, type, id FROM {item} WHERE id_user=?", (user_id, )).fetchall()

    def get_item_type_by_id(self, id):
        return self.cur.execute(f"SELECT type FROM other WHERE id=?", (id,)).fetchone()

    def add_item(self, item_type, name, user_id, custom_type=""):
        if item_type != "other":
            self.cur.execute(
                f"INSERT INTO {item_type} (id_user, name) VALUES (?, ?)", (user_id, name)
            )
        else:
            self.cur.execute(
                f"INSERT INTO {item_type} (id_user, type, name) VALUES (?, ?, ?)", (user_id, custom_type, name)
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

    def get_priority_by_organization_name(self, organization):
        return self.cur.execute(
            f"SELECT priority FROM organization WHERE name = ?", (organization,)
        ).fetchone()[0]

    def get_departments(self, name):
        return self.cur.execute(
            """
            SELECT key, name, user.fio, address, phone FROM offices
            LEFT  JOIN user ON offices.supervisor == user.id
            WHERE offices.organization = ?;
            """,  (name,)
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

    def generate_otchet_sklad(self, date_start="", date_end=""):
        if date_end == "":
            date_end = date.today()

        if date_start != "":
            return self.cur.execute(
                 f"SELECT id_item, type_item, id_stock "
                 f"FROM item WHERE arrival_time >= ? AND arrival_time <= ?", (date_start, date_end)).fetchall()
        else:
            return self.cur.execute(
                 f"SELECT id_item, type_item, id_stock "
                 f"FROM item WHERE arrival_time <= ?", (date_end, )).fetchall()

    def get_warehouse_by_id(self, id):
        return self.cur.execute(
            "SELECT name FROM sklad WHERE id=?", (id, )
        ).fetchone()[0]

    def get_item_name_by_type(self, id, type):
        return self.cur.execute(
            f"SELECT name FROM {type} WHERE id=?", (id, )
        ).fetchone()[0]

    def get_other_types(self):
        return self.cur.execute(
            "SELECT type FROM other group by type"
        ).fetchall()

    def get_item_name_by_warehouse_ok_status(self, whs_name):
        return self.cur.execute(
            """
            SELECT type_item, id_item, arrival_time FROM item LEFT JOIN sklad ON id_stock == sklad.id
            WHERE sklad.name == ? and item.status == 'ok'
            """, (whs_name, )
        ).fetchall()

    def get_item_name_by_warehouse_remove_status(self, whs_name):
        return self.cur.execute(
            """
            SELECT type_item, id_item, arrival_time FROM item LEFT JOIN sklad ON id_stock == sklad.id
            WHERE sklad.name == ? and item.status == 'removed'
            """, (whs_name, )
        ).fetchall()

    def get_item_name_by_warehouse_underchange_status(self, whs_name):
        return self.cur.execute(
            """
            SELECT type_item, id_item, arrival_time FROM item LEFT JOIN sklad ON id_stock == sklad.id
            WHERE sklad.name == ? and item.status == 'underchange'
            """, (whs_name, )
        ).fetchall()

    def get_user_role(self, id):
        return self.cur.execute(
            f"SELECT role FROM user WHERE id=?", (id ,)
        ).fetchone()[0]

    def get_organization_name(self, id):

        return self.cur.execute(
            f"SELECT organization FROM user WHERE id = ?", (id, )
        ).fetchone()[0]

    def get_organizations(self, role, organization):
        if(role==1):
            return self.cur.execute(
                f"SELECT name, address, priority FROM organization "
            ).fetchall()
        elif (role == 2):
            return self.cur.execute(
                f"SELECT name, address, priority FROM organization WHERE name = ?",
                (organization, )
            ).fetchall()

    def get_office_id_by_name(self, office):
        return self.cur.execute(
            f"SELECT id FROM offices WHERE name = ?", (office,)
        ).fetchone()[0]

    def get_staff(self, organization, office):
        print(organization, office)
        return self.cur.execute(
            f"SELECT fio, role, office, number, tubel_number FROM user WHERE office = ? ",
            (office, )
        ).fetchall()
    def get_user_id_by_name(self, name):
        return self.cur.execute(
            f"SELECT id FROM user WHERE fio = ?", (name,)
        ).fetchone()[0]

    def EXCEL_REPORT_ITEMS_ON_WAREHOUSE(self):
        ...
    def get_user_organization_by_id(self, id):
        return self.cur.execute(
            f"SELECT organization FROM user WHERE id = ?", (id,)
        ).fetchone()[0]
    def get_department_organization_by_department_name(self, name):
        return self.cur.execute(
            f"SELECT organization FROM offices WHERE name = ?", (name,)
        ).fetchone()[0]

    def add_person(self, fio, role, organization, office):
        self.cur.execute(f"INSERT INTO user (fio,  role, office, organization)"
                         f" VALUES (?, ?,  ?, ?)",
                         (fio,  role, office, organization))
        self.con.commit()

    def change_person(self, fio, role, organization, office,  id):
        self.cur.execute("UPDATE user SET fio=?, role=?, office=?, organization=? WHERE id=?",
                         (fio,  role, office, organization, id))
        self.con.commit()

    def get_office_by_name_of_ofiice(self, name):
        return self.cur.execute(
            f"SELECT id FROM offices WHERE name = ?", (name,)
        ).fetchone()[0]

    def add_device(self, device_type, id_user, name, s_number='', year='', custom_type=""):

        if custom_type == "":

            self.cur.execute(
                f"INSERT INTO {device_type} (id_user, name) VALUES (?, ?)", (id_user, name)
            )
        else:
            self.cur.execute(
                f"INSERT INTO {device_type} (id_user, type, name) VALUES (?, ?, ?)", (id_user, custom_type, name)
            )
        self.con.commit()

    def edit_device(self, device_type, name, globalId, s_number='', year='', custom_type=""):
        print(globalId, "<---")
        if custom_type == "":
            self.cur.execute(
                f"UPDATE {device_type} SET name=? WHERE id=?", (name, globalId)
            )

        self.con.commit()

    def delete_device(self, device_type, global_id):
        self.cur.execute(
            f"DELETE FROM {device_type} WHERE id=?", (global_id, )
        )
        self.con.commit()

    def add_department(self, key, name, supervisor, address, phone, organization):
        self.cur.execute(
                """
                INSERT INTO offices (key, name, supervisor, address, phone, organization)
                VALUES (?, ?, ?, ?, ?, ?);
                """, (key, name, supervisor, address, phone, organization)
            )
        self.con.commit()
        return self.cur.lastrowid

    def update_department(self, dep_id, key, name, supervisor, address, phone):
        self.cur.execute(
            """
            UPDATE offices SET key = ?, name = ?, supervisor = ?, address = ?, phone = ?
               WHERE id = ?;
               """, (key, name, supervisor, address, phone, dep_id)
           )
        self.con.commit()


    def delete_department(self, dep_id):
        self.cur.execute("DELETE FROM offices WHERE id = ?;", (dep_id,))
        self.con.commit()

    def add_organization(self, name, address, priority):
        self.cur.execute(
            "INSERT INTO organization (name, address, priority) VALUES (?, ?, ?)",
            (name, address, priority)
        )
        self.con.commit()
        return self.cur.lastrowid

    def update_organization(self, org_id, name, address, priority):
        self.cur.execute(
            "UPDATE organization SET name = ?, address = ?, priority = ? WHERE id = ?",
            (name, address, priority, org_id)
        )
        self.con.commit()

    def delete_organization(self, org_id):
        self.cur.execute("DELETE FROM organization WHERE id = ?", (org_id,))
        self.con.commit()

    def get_organization_id_by_name(self,name):
        return self.cur.execute(
            f"SELECT id FROM organization WHERE name = ?", (name,)
        ).fetchone()[0]