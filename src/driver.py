from selenium.webdriver.chrome.options import Options
from selenium import webdriver


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
