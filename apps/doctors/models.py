from peewee import *
from connect import sqlite_db
from apps.cities.models import CitiesModel


class DoctorsModel(Model):
    City = ForeignKeyField(CitiesModel)
    Number = DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        database = sqlite_db


def create_doctors_table():
    DoctorsModel.create_table()


def delete_doctorsmodel():
    return DoctorsModel.delete()


def insert_doctors(dictionnary):
    DoctorsModel.insert_many(dictionnary).execute()
