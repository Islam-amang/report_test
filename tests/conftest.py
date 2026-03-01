import pytest
from main import AverageGDPReport

#заменяем вызов нашего класса на более удобный
@pytest.fixture
def gdp_report():
    return AverageGDPReport()
