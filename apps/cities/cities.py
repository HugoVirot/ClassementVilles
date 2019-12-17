import pandas as pds
from pandas import DataFrame
import settings

def read_cities_csv_data(path):
    return pds.read_csv(path, low_memory=False, names=[str(i) for i in range(26)])

def rename_cities_columns(cities):
    df_cities = pds.DataFrame(cities) # convertir villes en dataframe
    df_cities.rename(columns={'4':'Ville', '9':'Code_commune', '13':'Population'}, inplace = True) # renommer colonnes
    return df_cities

def sort_cities_by_population(cities):
    sorted_cities = cities.sort_values(by='Population', ascending=False)
    return sorted_cities

def rename_and_sort(cities_data):
    renamed_cities = rename_cities_columns(cities_data) 
    return sort_cities_by_population(renamed_cities) # les trier par population décroissante

