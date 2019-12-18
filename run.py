import matplotlib.pyplot as plot
from apps.cities import cities
from apps.highschools import highschools
import settings
# from database import connect
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        help="Choose an action to execute",
        nargs="?",
        choices=[
            "rank_cities_by_note",
            "insert_cities_and_highschools_into_db"
        ],
    )
    args = parser.parse_args()

    if args.action == "rank_cities_by_note":
        cities_data = cities.read_cities_csv_data(settings.cities_csv_path)  # récup csv villes
        sorted_cities = cities.sort_cities_by_population(cities_data) # renommage colonnes et tri par taille
        highschools_data = highschools.read_highschools_csv_data(settings.highschools_csv_path) # récup csv lycées
        sorted_by_rating_cities = highschools.rate_and_sort_biggest_cities(highschools_data, sorted_cities) # noter et trier par note
        bar_data = highschools.create_graph(sorted_by_rating_cities) # créer un graphique
        plot.show() # l'afficher

    # if args.action == "insert_cities_and_highschools_into_db":
    #     connect.insert_cities_and_highschools_into_db()


    