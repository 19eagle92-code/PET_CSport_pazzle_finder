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


URL = "https://www.cybersport.ru"


options = Options()
# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")


driver = webdriver.Chrome(options=options)
driver.get(URL)


def puzzle_check(driver):
    """Функция проверки наличия пазла"""
    try:
        driver.find_element(By.XPATH, "//span[contains(text(), 'Хватай свой пазл!')]")
        return True
    except NoSuchElementException:
        return False


# link = URL + "/tags/dota-2/korb3n-o-team-spirit-spad-yeto-normalno-byvayet"
link = (
    URL
    + "/tags/dota-2/kiritych-o-betboom-team-my-gotovy-rugat-sya-drug-s-drugom-chtoby-stat-luchshe-no"
)

driver.execute_script("window.open(arguments[0]);", link)
driver.switch_to.window(driver.window_handles[1])


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "//span[contains(text(),'Хватай свой пазл!') or contains(text(), 'Тут пазла нет!') or contains(text(), 'Этот пазл уже твой!')]",
        )
    )
)


if puzzle_check(driver):
    print("Пазл найден")
else:
    print("Пазл не найден")

driver.close()
driver.switch_to.window(driver.window_handles[0])

driver.quit()
exit()
