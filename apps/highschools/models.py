from peewee import *
from connect import sqlite_db
from apps.cities.models import CitiesModel


class RatingsModel(Model):
    City = ForeignKeyField(CitiesModel)
    Note = FloatField()

    class Meta:
        database = sqlite_db


def create_ratings_table():
    RatingsModel.create_table()


def delete_ratingsmodel():
    return RatingsModel.delete()


def insert_dictionnary(dictionnary):
    RatingsModel.insert_many(dictionnary).execute()


def select_cities_and_ratings():
    return RatingsModel.select().join(CitiesModel)
