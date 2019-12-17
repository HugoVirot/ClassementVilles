import matplotlib.pyplot as plot
from apps.cities import cities
from apps.highschools import highschools
import settings
import pandas as pds
from pandas import DataFrame

if __name__ == '__main__':

    cities_data = cities.read_cities_csv_data(settings.cities_csv_path)  # récup csv villes
    sorted_cities = cities.sort_cities_by_population(cities_data, '13') # les trier par population décroissante

    sorted_cities = pds.DataFrame(sorted_cities) # convertir villes en dataframe
    sorted_cities.rename(columns={'4':'Ville', '9':'Code_commune', '13':'Population'}, inplace = True) # renommer colonnes

    highschools_data = highschools.read_highschools_csv_data(settings.highschools_csv_path) # récup csv lycées

    grouped_cities = highschools.group_cities_districts(highschools_data) # regrouper Paris en 1 ligne

    extracted_insee = highschools.extract_highschools_columns(grouped_cities) # extraire 2 colonnes

    averages = highschools.average_by_insee(extracted_insee) 
                                           
    merge_result = pds.merge(averages, sorted_cities[['Ville', 'Code_commune', 'Population']], on='Code_commune')
    
    sorted_by_population_results = cities.sort_cities_by_population(merge_result, 'Population') # villes triées par taille
    
    biggest_cities = sorted_by_population_results.head(settings.cities_max_number) # 50 plus grandes villes
    
    ratings = highschools.calculate_ratings(biggest_cities)
    print(ratings)

    sorted_by_success = highschools.sort_cities_by_success(biggest_cities) # villes triées par réussite
    print(sorted_by_success)

    bar_data = highschools.create_graph(sorted_by_success) # créer un graphique
    plot.show() # l'afficher
    