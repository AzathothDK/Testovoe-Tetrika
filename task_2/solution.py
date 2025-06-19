import csv
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://ru.wikipedia.org"
CATEGORY_URL = BASE_URL + "/w/index.php?title=Категория:Животные_по_алфавиту&from={letter}"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

ALPHABET = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М',
    'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я'
]

def get_letter_count(letter):
    count = 0
    url = CATEGORY_URL.format(letter=letter)

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Ошибка доступа к {url}: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        ul_elements = soup.select("div.mw-category-group ul li a")
        count += len(ul_elements)

        next_link = soup.find("a", string="Следующая страница")
        if next_link:
            url = BASE_URL + next_link["href"]
            time.sleep(0.5)  
        else:
            break

    return count

def main():
    result = []

    for letter in ALPHABET:
        count = get_letter_count(letter)
        result.append((letter, count))

    with open("beasts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for letter, count in result:
            writer.writerow([letter, count])

    print("\nГотово. Результаты записаны.")

if __name__ == "__main__":
    main()
