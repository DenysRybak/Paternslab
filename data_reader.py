import requests
import csv
from io import StringIO


def read_data_from_url(url):
    print(f"Завантаження з URL: {url}")
    response = requests.get(url)
    print(f"Status code: {response.status_code}")  # додано

    if response.status_code == 200:
        csv_data = StringIO(response.text)
        reader = csv.reader(csv_data)

        data = []
        for row in reader:
            data.append(row)
        print(f"Кількість рядків: {len(data)}")  # додано
        return data
    else:
        print(f"❌ Помилка: Неможливо отримати дані. Код статусу: {response.status_code}")
        return []

