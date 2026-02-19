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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3

# BASE_URL = "https://www.cybersport.ru/tags/dota-2?sort=-publishedAt"
URL = "https://www.cybersport.ru"
BASE_URL = "https://www.cybersport.ru/tags/dota-2"

# 2026-02-12


def init_db():
    """Функцуия создания таблицы ДБ"""
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            date TEXT,
            has_puzzle INTEGER
        )
    """
    )

    conn.commit()
    return conn


def save_article(conn, url, date, has_puzzle):
    """Функция сохранения статей в ДБ"""
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO articles (url, date, has_puzzle)
        VALUES (?, ?, ?)
    """,
        (url, date, int(has_puzzle)),
    )


def create_driver():
    """Функция создающая driver"""
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)
    return driver


def open_site(driver, URL):
    """Функция открывающая сайт"""
    return driver.get(URL)


def close_browser(driver):
    """Функция закрывающая браузер"""
    return driver.quit()


def puzzle_check(driver):
    """Функция проверки наличия пазла"""
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'пазл')]")
            )
        )
        return "Хватай свой пазл" in element.text
    except:
        return False


def get_articles(driver):
    """Функция получения статей"""
    return driver.find_elements(By.TAG_NAME, "article")


def button_check(driver):
    """Функция проверки существования кнопки"""
    try:
        return WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Показать еще')]")
            )
        )
    except:
        return None


def button_push(driver):
    """Функция нажатия кнопки"""

    button = button_check(driver)
    if button is None:
        return False

    try:

        actions = ActionChains(driver)
        actions.move_to_element(button).perform()
        button.click()
        return True

    except:
        try:
            # Если обычный клик не работает, пробуем JavaScript клик
            driver.execute_script("arguments[0].click();", button)
            return True
        except:
            return False


def scroll(driver):
    """Функция прокрутки страницы"""
    # Если кнопка не найдена пролистываем до конца страницы
    return driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def get_last_article_date(driver):
    """Функция полученпия даты последней статьи"""
    articles = get_articles(driver)
    last_article = articles[-1]

    time_tag = last_article.find_element(By.TAG_NAME, "time")
    date_str = time_tag.get_attribute("datetime")[:10]

    return datetime.strptime(date_str, "%Y-%m-%d")


def get_article_title(article):
    """Функция получения заголовка статьи"""
    return article.find_element(By.TAG_NAME, "h3").text.strip()


def get_article_date(article):
    """Функция получения даты статьи"""
    time_tag = article.find_element(By.TAG_NAME, "time")
    date_str = time_tag.get_attribute("datetime")[:10]

    return datetime.strptime(date_str, "%Y-%m-%d")


def get_article_link(article):
    """Функция получения link (ссылки) статьи"""
    link_tag = article.find_element(By.TAG_NAME, "a")
    href = link_tag.get_attribute("href")
    if href.startswith("/"):
        link = URL + href

    return link


def load_more(driver):
    """Функция подгрузки статей"""
    old_article_count = len(get_articles(driver))

    if button_check(driver) is not None:
        button_push(driver)
    else:
        scroll(driver)

    WebDriverWait(driver, 10).until(lambda d: len(get_articles(d)) > old_article_count)


driver = create_driver()
open_site(driver, BASE_URL)

while True:

    articles = get_articles(driver)
    last_date = get_last_article_date(driver)
    target_date_str = "2026-02-09"

    if last_date <= datetime.strptime(target_date_str, "%Y-%m-%d"):
        print("Достигнута целевая дата")
        break

    old_article_count = len(articles)

    button = button_check(driver)

    if button:
        button_push(driver)
    else:
        scroll(driver)

    WebDriverWait(driver, 10).until(lambda d: len(get_articles(d)) > old_article_count)

    new_count = len(get_articles(driver))

    if new_count == old_article_count:
        print("Статьи закончились")
        break

close_browser(driver)
