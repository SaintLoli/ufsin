TABLES = {
    'board' : 'Клавиатура',
    'monitor' : 'Монитор',
    'mouse' : 'Компьютерная мышь',
    'printer' : 'Принтер',
    'tel' : 'Стационарный телефон',
    'other' : 'Другое'
}

REVERSE_TABLES = {
    'Клавиатура': 'board',
    'Монитор': 'monitor',
    'Компьютерная мышь': 'mouse',
    'Принтер': 'printer',
    'Стационарный телефон': 'tel',
    'Другое' : 'other'
}

STATUS_TABLE = {
    1 : 'В эксплуатации',
    2 : 'Подлежит замене',
    3 : 'На ремонте',
    4 : 'На рассмотрении'
}

JSON_FORM = {
    'cpu' : '',
    'motherboard' : '',
    'gpu' : '',
    'ram' : '',
    'year' : '',
    's_number' : '',
    'devices' : []
}

DEVICE_TEMPLATE = {
    'type' : '',
    'name' : '',
    's_number' : '',
    'year' : ''
}