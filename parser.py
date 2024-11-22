import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Настраиваем CSV файл
csv_file = 'news.csv'
today_date = datetime.now().strftime('%Y-%m-%d')  # Текущая дата в формате YYYY-MM-DD

# Проверяем, существует ли файл, и добавляем заголовки, если он новый
try:
    with open(csv_file, 'x', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['data_key', 'title', 'img_url', 'post_url', 'parsed_date'])
except FileExistsError:
    pass

# Функция очистки неактуальных записей
def clean_old_entries():
    rows_to_keep = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['parsed_date'] == today_date:  # Оставляем только сегодняшние записи
                rows_to_keep.append(row)

    # Перезаписываем файл только с актуальными записями
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['data_key', 'title', 'img_url', 'post_url', 'parsed_date'])
        writer.writeheader()
        writer.writerows(rows_to_keep)

# Функция парсинга новостей
def fetch_news():
    base_url = "https://stopgame.ru"
    url = f"{base_url}/news/all/p"  # URL сайта с новостями

    # Читаем существующие data_key из файла
    existing_keys = set()
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_keys.add(row['data_key'])




    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        today_news_ended = False
        index = 1

        while not today_news_ended:
            response = requests.get(f"{url}{index}")
            if response.status_code != 200:
                print(f"Ошибка загрузки страницы: {response.status_code}")
                return
            soup = BeautifulSoup(response.content, "html.parser")
            news_items = soup.find_all('div', class_='_card_1vlem_1')  # Указываем класс карточек новостей
            for item in news_items:
                # Извлекаем ключевые данные
                data_key = item.find_parent().get('data-key')
                title_tag = item.find('a', class_='_title_1vlem_60')
                img_tag = item.find('img')

                # Если элемент уже в файле, прекращаем выполнение
                if data_key in existing_keys:
                    print("Эта и все последующие новости уже добавлены.")
                    today_news_ended = True
                    break

                title = title_tag.text.strip() if title_tag else ""
                img_url = img_tag['src'] if img_tag else ""
                post_url = base_url + title_tag['href'] if title_tag else ""

                # Проверяем дату поста
                date_tag = item.find('div', class_='_info-row_1vlem_121').find('span')
                if date_tag and "Сегодня" in date_tag.text:
                    writer.writerow([data_key, title, img_url, post_url, today_date])
                    print(f"Добавлена новость: {title}")
                else:
                    print("Не сегодняшняя новость, пропускаем.")
                    today_news_ended = True  # Прерываем поиск, так как новости идут в обратном хронологическом порядке
                    break
            index += 1

    print("Все новости обработаны.")
