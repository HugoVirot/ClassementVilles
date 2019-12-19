from peewee import *
from connect import sqlite_db
from apps.cities.models import CitiesModel


class DoctorsModel(Model):
    City = ForeignKeyField(CitiesModel)
    Number = FloatField()

    class Meta:
        database = sqlite_db