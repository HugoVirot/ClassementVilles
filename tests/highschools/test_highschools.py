from apps.highschools import highschools
import settings
import pandas as pds 

def test_csv_loading():
    data = highschools.read_highschools_csv_data(settings.highschools_csv_path)
    assert (data['Etablissement'][0]) == "LYCEE PIERRE-GILLES DE GENNES"
    assert len(data) == 16210    

def test_columns_extraction():
    data = highschools.read_highschools_csv_data(settings.highschools_csv_path)
    extracted_columns = highschools.extract_highschools_columns(data)
    assert len(extracted_columns.columns) == 3

def test_one_line_per_insee():
    data = {'Code commune': ['99999','99999','99999'], 'réussite' : [50.0, 75.0, 100.0]}
    df = pds.DataFrame(data)
    averages = highschools.average_by_insee(df)
    assert averages.iloc[0]['réussite'] == 75.0

def test_check_duplicated_insee_codes():
    data = highschools.read_highschools_csv_data(settings.highschools_csv_path)
    grouped_cities = highschools.group_cities_districts(data)
    extracted_columns = highschools.extract_highschools_columns(grouped_cities)
    averages = highschools.average_by_insee(extracted_columns)
    boolean = any(averages['Code_commune'].duplicated())
    assert boolean == False





