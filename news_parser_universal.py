"""
Универсальный сборщик заголовков (Universal Headline Scraper)
Принимает URL сайта как аргумент командной строки.
Результат сохраняется в папку с исполняемым файлом (рядом с EXE).
"""
import sys
import csv
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_headlines(url):
    """Скачивает страницу, извлекает title, h1, h2, h3, возвращает список."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = []

    # Заголовок страницы (title)
    if soup.title and soup.title.string:
        results.append({
            'scraped_at': scraped_at,
            'headline': soup.title.string.strip(),
            'link': url
        })

    # Все теги h1, h2, h3
    for tag in soup.find_all(['h1', 'h2', 'h3']):
        text = tag.get_text(strip=True)
        if text:
            results.append({
                'scraped_at': scraped_at,
                'headline': text,
                'link': url
            })
    return results

def main():
    if len(sys.argv) < 2:
        print("Использование: NewsParser.exe <URL>")
        print("Пример: NewsParser.exe https://example.com")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)

    url = sys.argv[1]
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"Сбор заголовков с {url} ...")
    headlines = scrape_headlines(url)

    if headlines is None:
        input("\nНе удалось загрузить страницу. Нажмите Enter для выхода...")
        sys.exit(1)

    if not headlines:
        print("Заголовки не найдены.")
        input("\nНажмите Enter для выхода...")
        sys.exit(0)

    # Определяем папку, где лежит исполняемый файл (или скрипт)
    if getattr(sys, 'frozen', False):
        # Запущено как скомпилированный exe
        exe_dir = os.path.dirname(sys.executable)
    else:
        # Запущено как .py скрипт
        exe_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file = os.path.join(exe_dir, 'news_export.csv')

    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['scraped_at', 'headline', 'link'])
        writer.writeheader()
        writer.writerows(headlines)

    print(f"Готово! Сохранено {len(headlines)} заголовков в {csv_file}")
    input("\nНажмите Enter, чтобы закрыть окно...")

if __name__ == '__main__':
    main()