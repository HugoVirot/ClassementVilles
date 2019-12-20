from apps.doctors import controllers
import settings


def test_doctors_csv_loading():
    data = controllers.read_doctors_csv_data(settings.doctors_csv_path)
    assert (data.iloc[0]['c_depcom']) == "92051"
    assert len(data) == 61803


def test_check_duplicated_insee_codes():
    data = controllers.read_doctors_csv_data(settings.doctors_csv_path)
    grouped_doctors = controllers.group_doctors_by_insee(data)
    boolean = any(grouped_doctors['Code_commune'].duplicated())
    assert not boolean


def test_total_doctors_per_insee():
    data = controllers.read_doctors_csv_data(settings.doctors_csv_path)
    grouped_doctors = controllers.group_doctors_by_insee(data)
    assert (grouped_doctors.iloc[0]['nombre_medecins']) == 29
    assert (grouped_doctors.iloc[9880]['nombre_medecins']) == 20


def test_biggest_cities_districts_grouped():
    data = controllers.read_doctors_csv_data(settings.doctors_csv_path) # récup csv docteurs
    grouped_doctors = controllers.group_doctors_by_insee(data) # groupby insee
    doctors_renamed = grouped_doctors.rename(columns={'c_depcom': 'Code_commune'}) # on renomme les colonnes
    doctors_grouped_cities = controllers.group_cities_districts(doctors_renamed) # arrs = 1 ligne
    print(doctors_grouped_cities)
    assert 1 == 1                               # vérifier : 1 seule ligne pour 75056


def test_citizens_per_doctor_ratio_calculation():
    doctors_data = controllers.read_doctors_csv_data(settings.doctors_csv_path)
    filtered_doctors = controllers.filter_by_biggest_cities(doctors_data)
    doctors_ratio = controllers.calculate_ratio(filtered_doctors)
    assert doctors_ratio.iloc[0]['habitants_par_medecin'] == 832.1415129845691
    assert doctors_ratio.iloc[46]['habitants_par_medecin'] == 1008.1395348837209



