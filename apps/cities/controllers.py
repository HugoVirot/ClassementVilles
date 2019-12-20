import pandas as pds
from apps.cities import models
import settings


def read_cities_csv_data(path):
    """
    Lit le fichier csv et en extrait les données.
    1 paramètre : le chemin d'accès au fichier.
    """
    return pds.read_csv(path, low_memory=False,
                        names=["ville_id", "ville_departement", "ville_slug", "Ville", "ville_nom_simple",
                               "ville_nom_reel", "ville_nom_soundex", "ville_nom_metaphone", "ville_code_postal",
                               "ville_commune", "Code_commune", "ville_arrondissement", "ville_canton", "ville_amdi",
                               "ville_population_2010", "ville_population_1999", "Population", "ville_densite_2010",
                               "ville_surface", "Longitude", "Latitude", "ville_longitude_grd", "ville_latitude_grd",
                               "ville_longitude_dms", "ville_latitude_dms", "ville_zmin", "ville_zmax"])


def sort_cities_by_population(cities):
    """
    Trie les villes par population décroissante.
    1 paramètre : le tableau contenant la liste des villes.
    """
    df_cities = pds.DataFrame(cities)
    sorted_cities = df_cities.sort_values(by='Population', ascending=False)
    return sorted_cities


def remove_biggest_cities_columns(sorted_cities):
    """
    Permet de garder seulement 4 colonnes du tableau des villes.
    1 paramètre : la liste des 50 plus grandes villes avec leur note.
    """
    biggest_cities = sorted_cities.head(50)
    # 50 plus grandes villes
    return biggest_cities.filter(items=['Code_commune', 'Ville', 'Latitude', 'Longitude'])


def insert_cities_into_db():
    cities_data = read_cities_csv_data(settings.cities_csv_path)
    sorted_cities = sort_cities_by_population(cities_data)
    biggest_cities = remove_biggest_cities_columns(sorted_cities)
    cities_dict = biggest_cities.to_dict('records')
    query = models.delete_citiesmodel()
    query.execute()
    models.insert_cities(cities_dict)
