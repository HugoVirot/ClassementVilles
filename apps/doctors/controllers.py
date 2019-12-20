import pandas as pds
from apps.cities import controllers as citiescontrollers
import settings


def read_doctors_csv_data(path):
    """
    Cette fonction permet de lire un fichier csv.
    1 paramètre : le chemin d'accès.
    """
    return pds.read_csv(path, low_memory=False)


def group_doctors_by_insee(doctors_data):
    doctors_df = pds.DataFrame(doctors_data)
    doctors_filtered = doctors_df.filter(items=['c_depcom'])
    doctors_filtered['nombre_medecins'] = ""
    return doctors_filtered.groupby(['c_depcom'], as_index=False).nombre_medecins.count()


def filter_by_biggest_cities(doctors):
    data = citiescontrollers.read_cities_csv_data(settings.cities_csv_path)
    sorted_cities = citiescontrollers.sort_cities_by_population(data)
    biggest_cities = sorted_cities.head(settings.cities_max_number)  # 50 plus grandes villes
    print(biggest_cities)
    doctors_renamed = doctors.rename(columns={'c_depcom': 'Code_commune'})
    biggest_cities_doctors = pds.merge(doctors_renamed, biggest_cities[['Ville', 'Code_commune', 'Population']],
                                       on='Code_commune')
    return biggest_cities_doctors
