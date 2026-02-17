import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from rich.progress import track
from rich import print
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# BASE_URL = "https://www.cybersport.ru/tags/dota-2?sort=-publishedAt"
URL = "https://www.cybersport.ru"
BASE_URL = "https://www.cybersport.ru/tags/dota-2"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
# KEYWORDS = ["Хватай свой пазл!"]
KEYWORDS = ["Тут пазла нет!"]
# KEYWORDS = ["стареньким"]

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")


def get_response(URL, headers):
    return requests.get(URL, headers=headers)


def markup(URL, headers):
    return get_response(URL, headers).text


# print(markup)


def get_soup(URL, headers):
    soup = BeautifulSoup(markup(URL, headers), "html.parser")
    return soup


driver = webdriver.Chrome(options=options)
driver.get(BASE_URL)

while True:
    try:
        button = driver.find_element(
            By.XPATH, "//button[contains(text(),'Показать ещё')]"
        )
        button.click()
        time.sleep(2)
    except:
        break


articles = get_soup(BASE_URL, HEADERS).find_all("article")
print(len(articles))


def web_driver(URL):

    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    markup = driver.page_source
    soup = BeautifulSoup(markup, "html.parser")

    elements = driver.find_elements(
        By.XPATH, "//*[contains(text(), 'Хватай свой пазл!')]"
    )
    driver.quit()

    return elements


def full_article_by_keywords(url, headers, keywords):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    article_body = soup.find("article")
    if not article_body:
        return False

    text = article_body.get_text().lower()
    return any(keyword.lower() in text for keyword in keywords)


for article in track(articles, description="Прогресс поиска"):
    print("\n[bold magenta]Поиск по сайтам:[/bold magenta]")
    # Ищем заголовок
    title_tag = article.find("h3")
    # print(title_tag.text)
    if not title_tag:
        continue
    title = title_tag.text.strip()
    # print(title)

    # Ищем ссылку
    link = article.find("a")["href"]
    # print(link)

    if link.startswith("/"):
        link = URL + link
        # print(link)

    # Ищем дату
    date_tag = article.find("time")
    date = date_tag["datetime"][:10] if date_tag else "Без даты"
    # print(date)

    #     # Видимый текст статьи
    preview_text = article.get_text().lower()

    # Проверяем ключевые слова по заголовку
    if web_driver(link):
        print(f"{date} – {title} – {link}")
    else:
        print("Пазла тут нет")


print("\n[bold green]✓ Поиск завершен![/bold green]")
# if __name__ == "__main__":
