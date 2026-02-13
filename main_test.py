import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")


URL = "https://www.cybersport.ru/tags/dota-2/dyrachyo-posovetoval-novichkam-ne-igrat-v-dota-2"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def web_driver(
    URL,
):

    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    markup = driver.page_source
    soup = BeautifulSoup(markup, "html.parser")

    elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Тут пазла нет!')]")
    driver.quit()
    return elements


# time.sleep(10)
