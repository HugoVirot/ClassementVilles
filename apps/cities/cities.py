import pandas as pds
from pandas import DataFrame
import settings

def read_cities_csv_data(path):
    """
    Lit le fichier csv et en extrait les données.
    1 paramètre : le chemin d'accès au fichier.
    """
    return pds.read_csv(path, low_memory=False, names=[str(i) for i in range(26)])

def rename_cities_columns(cities):
    """ 
    Renomme les colonnes du tableau fourni.
    1 paramètre : le tableau contenant la liste des villes.
    """
    df_cities = pds.DataFrame(cities)
    df_cities.rename(columns={'4':'Ville', '9':'Code_commune', '13':'Population'}, inplace = True)
    return df_cities

def sort_cities_by_population(cities):
    """
    Trie les villes par population décroissante.
    1 paramètre : le tableau contenant la liste des villes.
    """
    sorted_cities = cities.sort_values(by='Population', ascending=False)
    return sorted_cities

def rename_and_sort(cities_data):
    """
    Appelle les 2 fonctions précédentes.
    1 paramètre : le tableau contenant la liste des villes.
    """
    renamed_cities = rename_cities_columns(cities_data) 
    return sort_cities_by_population(renamed_cities)

