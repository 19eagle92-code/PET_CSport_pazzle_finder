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


def create_driver():
    """Функция создающая driver"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)
    return driver


def has_puzzle(driver):
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


options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")


driver = webdriver.Chrome(options=options)
driver.get(BASE_URL)
# 2026-02-12
time.sleep(2)

a = "article"
# button = driver.find_element(By.XPATH, "//button[contains(text(),'Показать еще')]")


def article_finder(n):
    """Функция парсинга элементов на сайте (статей)"""
    markup = driver.page_source
    soup = BeautifulSoup(markup, "html.parser")
    articles = soup.find_all(n)
    return articles


def button_check():
    try:
        time.sleep(2)
        button = driver.find_element(
            By.XPATH, "//button[contains(text(),'Показать еще')]"
        )
        if button:
            print(f"Найдена кнопока")
            actions = ActionChains(driver)
            actions.move_to_element(button).perform()
            time.sleep(1)
            try:
                button.click()
                time.sleep(2)
                return "Кнопка просто нажата"

            except:
                # Если обычный клик не работает, пробуем JavaScript клик
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
                return "Кнопка нажата через JavaScript"
        else:
            # Если кнопка не найдена пролистываем до конца страницы
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            return "Кнопки нет, пролистываем до конца"
    except Exception as e:
        return f"Ошибка при клике: {e}"


def web_driver(URL):

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(2)

    markup = driver.page_source
    soup = BeautifulSoup(markup, "html.parser")

    elements = driver.find_elements(
        By.XPATH, "//*[contains(text(), 'Хватай свой пазл!')]"
    )
    # driver.quit()

    return elements


def articl_data(n):
    for article in track(article_finder(n), description="Прогресс поиска"):
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
        if web_driver(link):
            print(f"{date} – {title} – {link}")
            with open("try_2.txt", "a", encoding="utf-8") as f:
                f.write(f"{date} – {title} – {link}\n")
        else:
            print("Пазла тут нет")

    print("\n[bold green]✓ Поиск завершен![/bold green]")
    return


while len(article_finder(a)) <= 200:
    button_check()
    print(len(article_finder(a)))
    if len(article_finder(a)) == 50:
        print("цикл завершен")
        articl_data(a)
