from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String, unique=True)
    password = database.Column(database.String)
    fio = database.Column(database.String, unique=True)
    role = database.Column(database.Integer)
    office = database.Column(database.Integer)