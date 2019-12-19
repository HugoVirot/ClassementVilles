from apps.doctors import controllers
import pandas as pds
import settings


def test_doctors_csv_loading():
    data = controllers.read_doctors_csv_data(settings.doctors_csv_path)
    assert (data.iloc[0]['c_depcom']) == "92051"
    assert len(data) == 61803


def test_check_duplicated_insee_codes():
    data = controllers.read_doctors_csv_data(settings.doctors_csv_path)
    grouped_doctors = controllers.group_doctors_by_insee(data)
    boolean = any(grouped_doctors['c_depcom'].duplicated())
    assert not boolean


def test_total_doctors_per_insee():
    data = controllers.read_doctors_csv_data(settings.doctors_csv_path)
    grouped_doctors = controllers.group_doctors_by_insee(data)
    assert (grouped_doctors.iloc[0]['nombre_medecins']) == 29
    assert (grouped_doctors.iloc[9919]['nombre_medecins']) == 3



