from apps.highschools import controllers
import settings
import pandas as pds


def test_csv_loading():
    data = controllers.read_highschools_csv_data(settings.highschools_csv_path)
    assert (data['Etablissement'][0]) == "LYCEE PIERRE-GILLES DE GENNES"
    assert len(data) == 16210


def test_columns_extraction():
    data = controllers.read_highschools_csv_data(settings.highschools_csv_path)
    extracted_columns = controllers.extract_highschools_columns(data)
    assert len(extracted_columns.columns) == 3


def test_one_line_per_insee():
    data = {'Code commune': ['99999', '99999', '99999'], 'réussite': [50.0, 75.0, 100.0]}
    df = pds.DataFrame(data)
    averages = controllers.average_by_insee(df)
    assert averages.iloc[0]['réussite'] == 75.0


def test_check_duplicated_insee_codes():
    data = controllers.read_highschools_csv_data(settings.highschools_csv_path)
    grouped_cities = controllers.group_cities_districts(data)
    extracted_columns = controllers.extract_highschools_columns(grouped_cities)
    averages = controllers.average_by_insee(extracted_columns)
    boolean = any(averages['Code_commune'].duplicated())
    assert not boolean


def test_ratings_calculation():
    data = {'Mentions': [50], 'Réussite': [50]}
    df = pds.DataFrame(data)
    result = controllers.calculate_ratings(df)
    print(result)
    assert result.iloc[0]['Note'] == 10.0
