import pandas as pds
import numpy as np

def read_highschools_csv_data(path):
    return pds.read_csv(path, low_memory=False, sep=";")


def group_cities_districts(highschools):
    paris_districts = ['75000',['0', '75101', '75102', '75103', '75104', '75105', '75106', '75107', '75108', '75109', '75110', '75111', '75112', '75113', '75114', '75115', '75116', '75117', '75118', '75119', '75120']]                                            # arrays d'arrondissements pour chaque ville
    marseille_districts = ['13000', ['13201','13202','13203','13204','13205','13206','13207','13208','13209','13210','13211','13212','13213','13214', '13215']]                                            # boucle qui les parcourt, les cherche dans highschools et les change
    lyon_districts = ['69000', ['69381', '69382', '69383', '69384', '69385', '69386', '69387', '69388', '69389']]
    list_of_districts = [paris_districts, marseille_districts, lyon_districts]
    print(list_of_districts)

    def change_insee(list_of_districts):
        for city in list_of_districts:
            for district_insee in city[1]:
                highschools.loc[highschools['Code commune'] == district_insee, 'Code commune'] = city[0]
                print(city[0])
        return highschools

    highschools = change_insee(list_of_districts)
    return highschools
    

def extract_highschools_columns(highschools):
    highschools_df = pds.DataFrame(highschools) 
    return highschools_df.filter(items=['Code commune', 'Taux Brut de Réussite Total séries'])


def average_by_insee(highschools):
    highschools.rename(columns={'Code commune':'Code_commune', 'Taux Brut de Réussite Total séries':'reussite'}, inplace = True) # renommer colonnes
    return highschools.groupby(['Code_commune'], as_index=False).mean()
