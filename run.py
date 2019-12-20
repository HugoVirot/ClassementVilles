import matplotlib.pyplot as plot
from apps.cities.models import create_cities_table
from apps.cities.controllers import read_cities_csv_data
from apps.cities.controllers import sort_cities_by_population
from apps.cities.controllers import insert_cities_into_db
from apps.highschools.models import create_ratings_table
from apps.highschools.controllers import rate_and_sort_biggest_cities
from apps.highschools.controllers import read_highschools_csv_data
from apps.highschools.controllers import insert_ratings_into_database
from apps.highschools.controllers import create_graph
from apps.doctors.controllers import read_doctors_csv_data
from apps.doctors.controllers import group_doctors_by_insee
from apps.doctors.controllers import filter_by_biggest_cities



import settings
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        help="Choose an action to execute",
        nargs="?",
        choices=[
            "rank_cities_by_note",
            "insert_cities_and_highschools_into_db",
            "doctors"
        ],
    )
    args = parser.parse_args()

    if args.action == "rank_cities_by_note":
        cities_data = read_cities_csv_data(settings.cities_csv_path)  # récup csv villes
        sorted_cities = sort_cities_by_population(cities_data) # renommage colonnes et tri par taille
        highschools_data = read_highschools_csv_data(settings.highschools_csv_path) # récup csv lycées
        sorted_by_rating_cities = rate_and_sort_biggest_cities(highschools_data, sorted_cities) # noter et trier par note
        bar_data = create_graph(sorted_by_rating_cities) # créer un graphique
        plot.show() # l'afficher

    if args.action == "insert_cities_and_highschools_into_db":
        create_cities_table()
        insert_cities_into_db()
        create_ratings_table()
        insert_ratings_into_database()

    if args.action == "doctors":
        doctors_data = read_doctors_csv_data(settings.doctors_csv_path)
        grouped_doctors = group_doctors_by_insee(doctors_data)
        filtered_doctors = filter_by_biggest_cities(grouped_doctors)
        print(filtered_doctors)





    