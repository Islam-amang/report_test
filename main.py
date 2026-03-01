from collections import defaultdict
from tabulate import tabulate
import csv
import argparse

# --- Блок логики отчетов ---
class BaseReport:
    def scanning_data(self, name_file: str) -> dict:
        # Берет данные из файла и преобразует их в словарь
        data = defaultdict(dict)
        try:
            with open(f'{name_file}', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                title = tuple(next(csvreader))
                for n, row in enumerate(csvreader):
                    for i, val in enumerate(row):
                        data[n][title[i]] = val
        except Exception as e:
            print(f"Ошибка чтения {name_file}: {e}")

        return data


    def report_to_file(self, sorted_average_gdb: dict, arg_report:str, report_file: str) -> None:
        # Принимает отсортированный список данных
        # записывает его в отдельный файл
        try:
            with open(f'{report_file}', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.titles)
                writer.writerows(sorted_average_gdb.items())
        except Exception as e:
            print(f"Ошибка записи {report_file}: {e}")
        return None


class AverageGDPReport(BaseReport):
    def __init__(self) -> None:
        self.titles = ['country','average-gdb'] # Задаем имена столбцов


    def _generation_report(self, files: dict) -> dict:
        # Считает среднее ВВП по странам.
        gdp = defaultdict(float)
        num_count = defaultdict(int)
        average_gdb = defaultdict(float)
        # Разные переборы потому что в первом есть данные по странам за разные года
        for file in files: # проходимся по всем переданным файлам
            data_file = self.scanning_data(file) # преобразуем в словарь один конкретный файл
            for row in data_file.values(): # проходимся по каждой строке одного конкретного файла
                try:
                    country, value = row['country'], row['gdp']
                    gdp[country] += float(value)
                    num_count[country] += 1
                except (KeyError, ValueError):
                    continue # если нет данных по какой-то стране пропускаем ее
        # Во втором переборе данные уже суммарно по всем годам и по всем файлам
        for country in gdp:
            average_gdb[country] = round(gdp[country] / num_count[country], 2)

        return average_gdb #возвращает словарь где ключ-страна значение-средний ввп


    def run(self, files: dict, report_type: str, report_to_file=False) -> None:
        # 1. Собираем средний ввп по всем странам
        final_report = self._generation_report(files)
        # 2. Сортируем результат (по убыванию ВВП)
        sorted_report = dict(sorted(final_report.items(), key=lambda x: x[1], reverse=True))
        # 3. Вывод
        print(tabulate(
            sorted_report.items(),
            tablefmt="fancy_grid",
            headers=self.titles,
            showindex=range(1, len(sorted_report) + 1))
        )
        # 4. Реализован вывод отчета в отдельный файл
        # (если при вызове run() в параметре report_to_file указать True)
        if report_to_file:
            self.report_to_file(sorted_report, report_type, f'report_{report_type}.csv')


class UnemploymentReport(BaseReport):
    """Пример будущего отчета по безработице"""
    def run(self, files, report_type, report_to_file) -> None:
        print("Отчет по безработице пока не реализован.")

# --- Инфраструктура ---
REPORTS = {
    'gdp_avg': AverageGDPReport,
    'unemployment': UnemploymentReport
} # Реестр доступных отчетов


def main():
    parser = argparse.ArgumentParser()
    # какие значения мы принимаем
    parser.add_argument('--files',
                        nargs='+',
                        required=True,
                        help="ввести названия файлов с исходными данными"
                        )
    parser.add_argument('--report',
                        default='gdp_avg',
                        choices=REPORTS.keys(),
                        help=f"Выберете один из доступных видов отчета: {', '.join(REPORTS.keys())}"
                        )

    # куда записываем эти значения
    args = parser.parse_args()
    # Динамический выбор и запуск отчета
    report_class = REPORTS[args.report]
    report_instance = report_class()
    report_instance.run(
        files=args.files,
        report_type=args.report,
        report_to_file=False # хотим ли мы создать файл с отчетом
    )


if __name__ == "__main__":
    main()
#python main.py --files economic1.csv economic2.csv
#python -m pytest --cov-report html --cov .