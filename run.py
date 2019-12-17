import matplotlib.pyplot as plot
from apps.cities import cities
from apps.highschools import highschools
import settings
import pandas as pds
from pandas import DataFrame

if __name__ == '__main__':

    cities_data = cities.read_cities_csv_data(settings.cities_csv_path)  # récup csv villes
    sorted_cities = cities.rename_and_sort(cities_data) # renommage colonnes et tri par taille
    highschools_data = highschools.read_highschools_csv_data(settings.highschools_csv_path) # récup csv lycées

    sorted_by_rating_cities = highschools.rate_and_sort_biggest_cities(highschools_data, sorted_cities)
    
    bar_data = highschools.create_graph(sorted_by_rating_cities) # créer un graphique
    plot.show() # l'afficher
    