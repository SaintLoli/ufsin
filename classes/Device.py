class Device:
    def __init__(self, name, type, status, year='', s_number=''):
        self.name = name
        self.type = type
        self.status = status

        self.year = year
        self.s_number = s_number
        self.id = ''
