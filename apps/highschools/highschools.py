import pandas as pds
from apps.cities import cities
import settings

def read_highschools_csv_data(path):
    """
    Cette fonction permet de lire un fichier csv.
    1 paramètre : le chemin d'accès.
    """
    return pds.read_csv(path, low_memory=False, sep=";")


def group_cities_districts(highschools):
    """
    Permet de modifier les codes insee des arrondissements des grandes villes,  pour leur donner celui de la ville en question.
    1 paramètre : la liste des lycées de France.
    """
    paris_districts = ['75056',['0', '75101', '75102', '75103', '75104', '75105', '75106', '75107', '75108', '75109', '75110', '75111', '75112', '75113', '75114', '75115', '75116', '75117', '75118', '75119', '75120']]                                            # arrays d'arrondissements pour chaque ville
    marseille_districts = ['13055', ['13201','13202','13203','13204','13205','13206','13207','13208','13209','13210','13211','13212','13213','13214', '13215']]                                            # boucle qui les parcourt, les cherche dans highschools et les change
    lyon_districts = ['69123', ['69381', '69382', '69383', '69384', '69385', '69386', '69387', '69388', '69389']]
    list_of_districts = [paris_districts, marseille_districts, lyon_districts]
    print(list_of_districts)

    def change_insee(list_of_districts):
        """
        Cherche dans la liste des lycées ceux qui ont le code insee de l'arrondissement en question.
        Il est remplacé par celui de la ville qui l'englobe.
        1 paramètre : une liste contenant le code insee de la ville + la liste des arrondissements de la ville.
        """
        for city in list_of_districts:
            for district_insee in city[1]:
                highschools.loc[highschools['Code commune'] == district_insee, 'Code commune'] = city[0]
                print(city[0])
        return highschools

    highschools = change_insee(list_of_districts)
    return highschools
    

def extract_highschools_columns(highschools):
    """
    Permet d'extraire trois colonnes de la liste des lycées.
    1 paramètre : la liste des lycées avec codes insee des arrondissements des grandes villes uniformisés.
    """
    highschools_df = pds.DataFrame(highschools) 
    return highschools_df.filter(items=['Code commune', 'Taux_Mention_brut_toutes_series', 'Taux Brut de Réussite Total séries'])


def average_by_insee(highschools):
    """
    Réduit la liste à une ligne par code insee, tout en faisant une moyenne des taux de mentions et de réussite.
    1 paramètre : la liste des lycées (après extraction des 3 colonnes)
    """
    highschools.rename(columns={'Code commune':'Code_commune', 'Taux_Mention_brut_toutes_series':'mentions', 'Taux Brut de Réussite Total séries':'reussite'}, inplace = True) # renommer colonnes
    return highschools.groupby(['Code_commune'], as_index=False).mean()


def calculate_ratings(highschools):
    """
    Calcule une note pour chaque ville (résultat de taux mentions + taux réussite, divisé par 10).
    1 paramètre : liste des villes ayant un lycée (avec moyennes des taux effectuées)
    """
    cols = ["mentions","reussite"]
    highschools["note"] = highschools[cols].sum(axis=1)
    highschools["note"] /= 10
    return highschools


def sort_cities_by_success(data):
    """
    Trie les villes par note.
    1 paramètre : la liste des 50 (settins.cities_max_number, nombre modifiable) plus grandes villes de France.
    """
    return data.sort_values(by='note', ascending=False)


def rate_and_sort_biggest_cities(highschools_data, sorted_cities):
    """
    Appelle toutes les fonctions précédentes (sauf la 1ère) pour réaliser le traitement complet.
    Retourne les les 50 (settins.cities_max_number, nombre modifiable) plus grandes villes triées par note.
    2 paramètres : la liste des lycées et les villes triées par taille.
    """
    grouped_cities = group_cities_districts(highschools_data) # regrouper Paris en 1 ligne
    extracted_insee = extract_highschools_columns(grouped_cities) # extraire 2 colonnes
    averages = average_by_insee(extracted_insee) 
    merge_result = pds.merge(averages, sorted_cities[['Ville', 'Code_commune', 'Population']], on='Code_commune')
    sorted_by_population_results = cities.sort_cities_by_population(merge_result) # villes triées par taille
    biggest_cities = sorted_by_population_results.head(settings.cities_max_number) # 50 plus grandes villes
    print(biggest_cities)
    rate_biggest_cities = calculate_ratings(biggest_cities)
    sorted_by_rating_cities = sort_cities_by_success(rate_biggest_cities) # villes triées par réussite
    return sorted_by_rating_cities


def create_graph(sorted_data):
    """
    Crée un graphique à partir des données fournies.
    1 paramètre : les 50 (settins.cities_max_number, nombre modifiable) plus grandes villes triées par note.
    """
    return sorted_data.plot(x='Ville', y='note', kind='bar')