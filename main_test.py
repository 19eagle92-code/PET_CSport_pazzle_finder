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

# 2026-02-12


def create_driver():
    """Функция создающая driver"""
    options = Options()
    options.add_argument("--headless=new")
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
    button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Показать еще')]")
        )
    )
    return button


def button_push(driver, button):
    """Функция нажатия кнопки"""
    try:
        actions = ActionChains(driver)
        actions.move_to_element(button).perform()
        button.click()

    except:
        # Если обычный клик не работает, пробуем JavaScript клик
        driver.execute_script("arguments[0].click();", button)


def scroll(driver):
    """Функция прокрутки страницы"""
    # Если кнопка не найдена пролистываем до конца страницы
    return driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# def articl_data(n):
#     for article in track(article_finder(n), description="Прогресс поиска"):
#         print("\n[bold magenta]Поиск по сайтам:[/bold magenta]")
#         # Ищем заголовок
#         title_tag = article.find("h3")
#         # print(title_tag.text)
#         if not title_tag:
#             continue
#         title = title_tag.text.strip()
#         # print(title)

#         # Ищем ссылку
#         link = article.find("a")["href"]
#         # print(link)

#         if link.startswith("/"):
#             link = URL + link
#             # print(link)

#         # Ищем дату
#         date_tag = article.find("time")
#         date = date_tag["datetime"][:10] if date_tag else "Без даты"
#         # print(date)
#         if web_driver(link):
#             print(f"{date} – {title} – {link}")
#             with open("try_2.txt", "a", encoding="utf-8") as f:
#                 f.write(f"{date} – {title} – {link}\n")
#         else:
#             print("Пазла тут нет")

#     print("\n[bold green]✓ Поиск завершен![/bold green]")
#     return
