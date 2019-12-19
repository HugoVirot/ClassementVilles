from peewee import *
from connect import sqlite_db


class CitiesModel(Model):
    Code_commune = CharField(primary_key=True)
    Ville = CharField()
    Latitude = DecimalField(max_digits=9, decimal_places=6)
    Longitude = DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        database = sqlite_db


def create_cities_table():
    CitiesModel.create_table()


def delete_citiesmodel():
    return CitiesModel.delete()


def insert_dictionnary(dictionnary):
    CitiesModel.insert_many(dictionnary).execute()