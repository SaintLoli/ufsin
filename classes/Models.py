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
        self.id = ''
        self.name = name
        self.job_title = job_title
        self.office = office
        self.tel = tel
        self.tubel = tubel
        self.status = status