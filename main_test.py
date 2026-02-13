import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = "https://www.cybersport.ru/tags/dota-2/dyrachyo-posovetoval-novichkam-ne-igrat-v-dota-2"
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


def full_article_by_keywords(url, headers, keywords):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    article_body = soup.find("article")
    if not article_body:
        return False

    text = article_body.get_text().lower()
    return any(keyword.lower() in text for keyword in keywords)
    # return text


with open("try.txt", "w", encoding="utf-8") as f:
    f.write(full_article_by_keywords(URL, HEADERS, KEYWORDS))


def full_article_by_keywords(url, headers, keywords):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # article_body = soup.find("article")
    # if not article_body:
    #     return False

    # text = article_body.get_text().lower()
    # return any(keyword.lower() in text for keyword in keywords)
    return response.text


# with open("links2.csv", "a", encoding="utf-8", newline="") as f:
#     datawriter = csv.writer(f, delimiter=",")
#     # Вместо contacts_list подставьте свой список
#     datawriter.writerows(full_article_by_keywords(URL, HEADERS, KEYWORDS))

with open("try.txt", "w", encoding="utf-8") as f:
    f.write(full_article_by_keywords(URL, HEADERS, KEYWORDS))
