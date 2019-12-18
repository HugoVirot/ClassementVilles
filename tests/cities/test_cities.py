from apps.cities import cities
import settings

def test_csv_loading():
    data = cities.read_cities_csv_data(settings.cities_csv_path)
    assert (data.iloc[0][3]) == "OZAN"
    assert len(data) == 36700

def test_sorting():
    data = cities.read_cities_csv_data(settings.cities_csv_path)
    sorted_cities = cities.sort_cities_by_population(data)
    assert (sorted_cities.iloc[0][3]) == "PARIS"

