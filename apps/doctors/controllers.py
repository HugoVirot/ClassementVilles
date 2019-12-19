import pandas as pds
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



