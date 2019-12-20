import pandas as pds
from apps.cities import controllers as citiescontrollers
from apps.doctors import models
from apps.highschools import controllers as highschoolscontrollers
import settings


def read_doctors_csv_data(path):
    """
    Cette fonction permet de lire un fichier csv.
    1 paramètre : le chemin d'accès.
    """
    return pds.read_csv(path, low_memory=False)


def filter_by_biggest_cities(doctors):
    data = citiescontrollers.read_cities_csv_data(settings.cities_csv_path)
    sorted_cities = citiescontrollers.sort_cities_by_population(data)
    biggest_cities = sorted_cities.head(settings.cities_max_number)

    doctors_renamed = doctors.rename(columns={'c_depcom': 'Code_commune'})
    grouped_doctors = group_doctors_by_insee(doctors_renamed)
    print(grouped_doctors)
    biggest_cities_doctors = pds.merge(grouped_doctors, biggest_cities[['Ville', 'Code_commune', 'Population']],
                                       on='Code_commune')
    sorted_biggest_cities_doctors = citiescontrollers.sort_cities_by_population(biggest_cities_doctors)
    return sorted_biggest_cities_doctors


def group_doctors_by_insee(doctors_data):
    doctors_df = pds.DataFrame(doctors_data)
    doctors_renamed = doctors_df.rename(columns={'c_depcom': 'Code_commune'})
    doctors_filtered = doctors_renamed.filter(items=['Code_commune'])
    doctors_filtered['nombre_medecins'] = ""
    doctors_grouped_cities = group_cities_districts(doctors_filtered)
    return doctors_grouped_cities.groupby(['Code_commune'], as_index=False).nombre_medecins.count()


def group_cities_districts(doctors):
    """
    Permet de modifier les codes insee des arrondissements des grandes villes,  pour leur donner celui de la ville en question.
    1 paramètre : la liste des lycées de France.
    """
    paris_districts = ['75056',
                       ['0', '75101', '75102', '75103', '75104', '75105', '75106', '75107', '75108', '75109', '75110',
                        '75111', '75112', '75113', '75114', '75115', '75116', '75117', '75118', '75119',
                        '75120']]  # arrays d'arrondissements pour chaque ville
    marseille_districts = ['13055',
                           ['13201', '13202', '13203', '13204', '13205', '13206', '13207', '13208', '13209', '13210',
                            '13211', '13212', '13213', '13214',
                            '13215']]  # boucle qui les parcourt, les cherche dans highschools et les change
    lyon_districts = ['69123', ['69381', '69382', '69383', '69384', '69385', '69386', '69387', '69388', '69389']]
    list_of_districts = [paris_districts, marseille_districts, lyon_districts]

    doctors = change_insee(list_of_districts, doctors)
    return doctors


def change_insee(list_of_districts, doctors):

    """
    Cherche dans la liste des lycées ceux qui ont le code insee de l'arrondissement en question.
    Il est remplacé par celui de la ville qui l'englobe.
    1 paramètre : une liste contenant le code insee de la ville + la liste des arrondissements de la ville.
    """
    for city in list_of_districts:
        for district_insee in city[1]:
            doctors.loc[doctors['Code_commune'] == district_insee, 'Code_commune'] = city[0]
    return doctors


def calculate_ratio(data):
    data["habitants_par_medecin"] = data["Population"] / data["nombre_medecins"]
    return data


def insert_doctors_into_db():
    doctors_data = read_doctors_csv_data(settings.doctors_csv_path)
    filtered_doctors = filter_by_biggest_cities(doctors_data)
    doctors_ratio = calculate_ratio(filtered_doctors)
    doctors_dict = doctors_ratio.to_dict('records')
    query = models.delete_doctorsmodel()
    query.execute()
    models.insert_doctors(doctors_dict)
