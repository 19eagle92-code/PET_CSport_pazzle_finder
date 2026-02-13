import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from rich.progress import track
from rich import print
import time


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


def get_response(URL, headers):
    return requests.get(URL, headers=headers)


def markup(URL, headers):
    return get_response(URL, headers).text


# print(markup)


def get_soup(URL, headers):
    soup = BeautifulSoup(markup(URL, headers), "html.parser")
    return soup


articles = get_soup(BASE_URL, HEADERS).find_all("article")
print(len(articles))


def full_article_by_keywords(url, headers, keywords):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    article_body = soup.find("article")
    if not article_body:
        return False

    text = article_body.get_text().lower()
    return any(keyword.lower() in text for keyword in keywords)


for article in articles:
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
    if any(keyword.lower() in preview_text for keyword in KEYWORDS):
        print(f"{date} – {title} – {link}")
    # Проверяем ключевые слова по тексту статьи
    elif full_article_by_keywords(link, HEADERS, KEYWORDS):
        print(f"Full-{date} – {title} – {link}")


# full_article_by_keywords(link, HEADERS, KEYWORDS)
# print(f" {title} – {link}")

# with open("links.csv", "a", encoding="utf-8", newline="") as f:
#     datawriter = csv.writer(f, delimiter=",")
#     # Вместо contacts_list подставьте свой список
#     datawriter.writerows(full_article_by_keywords(link, HEADERS, KEYWORDS))
