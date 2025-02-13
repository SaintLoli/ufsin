class Device:
    def __init__(self, name, type, status, year='', s_number=''):
        self.name = name
        self.type = type
        self.status = status

        self.year = year
        self.s_number = s_number

        self.id = ''


class User:
    def __init__(self, name, job_title, office, tel, tubel, status):
        self.name = name
        self.job_title = job_title
        self.office = office
        self.tel = tel
        self.tubel = tubel
        self.status = status

        self.id = ''


class Office:
    def __init__(self, key, name, supervisor, address, phone, status):
        self.key = key
        self.name = name
        self.supervisor = supervisor
        self.address = address
        self.phone = phone
        self.status = status

        self.id = ''


class Warehouse:
    def __init__(self, name, address, supervisor):
        self.name = name
        self.address = address
        self.supervisor = supervisor

        self.id = ''

class ItemsOnSklad:
    def __init__(self, iditem, typeitem, stock):
        self.iditem = iditem
        self.typeitem = typeitem
        self.stock = stock

        self.id = ''