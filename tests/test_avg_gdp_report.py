import pytest
import os

# Список файлов для теста
EXISTING_FILES = ['tests/test_economic1.csv', 'tests/test_economic2.csv']


def test_files_exist():
    """Проверяем, что файлы вообще на месте перед тестом"""
    for file in EXISTING_FILES:
        assert os.path.exists(file), f"Файл {file} не найден. Тесты невозможны."


def test_generation_report_structure(gdp_report):
    """Проверяем финальный словарь"""
    report_data = gdp_report._generation_report(EXISTING_FILES)

    assert isinstance(report_data, dict)
    for country, avg_gdp in report_data.items():
        assert isinstance(country, str)
        assert isinstance(avg_gdp, (float, int))


def test_report_sorting(gdp_report):
    """Проверяем, что run() правильно сортирует данные (по убыванию)"""
    report_data = gdp_report._generation_report(EXISTING_FILES)
    sorted_report = dict(sorted(report_data.items(), key=lambda x: x[1], reverse=True))

    values = list(sorted_report.values())
    # Проверяем, что каждое следующее значение меньше или равно предыдущему
    assert all(values[i] >= values[i+1] for i in range(len(values)-1))


@pytest.mark.parametrize("file_name", EXISTING_FILES)
def test_scanning_logic(gdp_report, file_name):
    """Проверяем, что данные из файлов грузятся корректно"""
    data = gdp_report.scanning_data(file_name)
    assert isinstance(data, dict)
    assert len(data) > 0
    # Проверяем название столбцов
    assert 'country' in data[0]
    assert 'gdp' in data[0]


@pytest.mark.parametrize("file_name", EXISTING_FILES)
def test_csv_content_types(gdp_report, file_name):
    """Проверяем, что gdp в файлах — это действительно числа (валидация данных)"""
    data = gdp_report.scanning_data(file_name)
    for entry in data.values():
        # Пытаемся привести к float, если упадет — значит в CSV плохие данные
        assert float(entry['gdp']) >= 0

