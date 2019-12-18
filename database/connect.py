import sqlite3
from apps.cities import cities
from apps.highschools import highschools
import settings
from peewee import *

sqlite_db = SqliteDatabase('cities_ranking.db', pragmas={'journal_mode': 'wal'})


class BaseModel(Model):
    class Meta:
        database = sqlite_db

class CitiesModel(BaseModel):
    Code_commune = CharField(primary_key=True)
    Ville = CharField()
    Latitude = DecimalField(max_digits=9, decimal_places=6)
    Longitude = DecimalField(max_digits=9, decimal_places=6)

class RatingsModel(BaseModel):
    Code_commune = ForeignKeyField(CitiesModel, to_field="Code_commune")
    Note = FloatField()

CitiesModel.create_table()
RatingsModel.create_table()

def insert_cities_and_highschools_into_db():
    cities_data = cities.read_cities_csv_data(settings.cities_csv_path)
    sorted_cities = cities.sort_cities_by_population(cities_data)
    biggest_cities = cities.remove_biggest_cities_columns(sorted_cities)

    cities_dict = biggest_cities.to_dict('records')
    query = CitiesModel.delete()
    query.execute()
    CitiesModel.insert_many(cities_dict).execute()

    highschools_data = highschools.read_highschools_csv_data(settings.highschools_csv_path)
    sorted_by_rating_cities = highschools.rate_and_sort_biggest_cities(highschools_data, sorted_cities)
    filtered_columns_cities = sorted_by_rating_cities.filter(items=['Code_commune', 'Note'])

    rated_cities_dict = filtered_columns_cities.to_dict('records')

    query = RatingsModel.delete()
    query.execute()
    RatingsModel.insert_many(rated_cities_dict).execute()
    # query = RatingsModel.select()
    # for city in query:
    #     print(city.id, city.Code_commune, city.Note)

    query2 = RatingsModel.select().join(CitiesModel)
    query2.execute()
    for rating in query2:
        print(rating.Code_commune.Code_commune, rating.Code_commune.Ville, rating.Code_commune.Latitude, rating.Code_commune.Longitude, rating.Note)
