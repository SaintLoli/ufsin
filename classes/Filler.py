from classes.Models import *
from classes.TABLENAMES import *
from classes.DB_helper import DBHelper

database = DBHelper()


"""
Информация о Models
"""
DEVICES = []
USERS = []
DEPARTMENTS = []
WAREHOUSES = []
ITEMSONSKLAD = []

def fill_devices(USER_ID):
    global DEVICES
    DEVICES.clear()
    id = 1
    fio = database.get_user_fio(USER_ID)

    PC = database.get_computer_info(int(USER_ID))
    DEVICES.append(Device(database.get_pc_name_by_user_id(USER_ID), "Системный блок", "В эксплуатации", PC[4], PC[5],
                          fio, cpu=PC[2], motherboard=PC[0], gpu=PC[1], ram=PC[3]))

    DEVICES[-1].id = id
    id += 1

    for table_name in TABLES.keys():
        device = database.get_item(table_name, int(USER_ID))
        if device:
            DEVICES.append(Device(device[0], TABLES[table_name], "В эксплуатации", user_fio=fio))
            DEVICES[-1].id = id
            id += 1


def fill_users():
    global USERS
    USERS.clear()
    id = 1

    for user in database.get_users():
        USERS.append(User(user[0],
                          user[1] if not None else '',
                          database.get_dep_name_by_id(user[2]) if not None else '',
                          user[3] if not None else '',
                          user[4] if not None else '',
                          "Активен"))
        USERS[-1].id = id
        id += 1


def fill_departments():
   global DEPARTMENTS
   DEPARTMENTS.clear()
   id = 1

   for dep in database.get_departments():
       DEPARTMENTS.append(Office(dep[0],
                                 dep[1],
                                 dep[2],
                                 dep[3],
                                 dep[4],
                                 "Активен"))
       DEPARTMENTS[-1].id = id
       id += 1


def fill_warehouses():
    global WAREHOUSES
    WAREHOUSES.clear()
    id = 1

    for whs in database.get_warehouses():
        WAREHOUSES.append(Warehouse(whs[0],
                                    whs[1],
                                    whs[2]))

        WAREHOUSES[-1].id = id
        id += 1


def fill_report_warehouse(date_start, date_end):
    global ITEMSONSKLAD
    ITEMSONSKLAD.clear()
    id = 1

    for item in database.generate_otchet_sklad(date_start, date_end):
        ITEMSONSKLAD.append(ItemsOnSklad(item[0],
                                         TABLES[item[1]],
                                         database.get_warehouse_by_id(item[2]),
                                         database.get_item_name_by_type(item[0], item[1])))

        ITEMSONSKLAD[-1].id = id
        id += 1