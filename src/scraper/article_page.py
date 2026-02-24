from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from src.config import URL


def get_articles(driver):
    """Функция получения статей"""
    return driver.find_elements(By.TAG_NAME, "article")


def get_article_title(article):
    """Функция получения заголовка статьи"""
    return article.find_element(By.TAG_NAME, "h3").text.strip()


def get_article_date(article):
    """Функция получения даты статьи"""
    time_tag = article.find_element(By.TAG_NAME, "time")
    date_str = time_tag.get_attribute("datetime")[:10]
    # date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    return date_str


def get_article_link(article):
    """Функция получения link (ссылки) статьи"""
    link_tag = article.find_element(By.TAG_NAME, "a")
    href = link_tag.get_attribute("href")
    if href.startswith("http"):
        return href
    elif href.startswith("/"):
        return URL + href
    else:
        return URL + "/" + href


def get_last_article_date(articles):
    """Функция полученпия даты последней статьи"""

    last_article = articles[-1]

    time_tag = last_article.find_element(By.TAG_NAME, "time")
    date_str = time_tag.get_attribute("datetime")[:10]

    return datetime.strptime(date_str, "%Y-%m-%d")


def load_more(driver):
    """Функция подгрузки статей"""
    old_article_count = len(get_articles(driver))

    if button_check(driver) is not None:
        button_push(driver)
    else:
        scroll(driver)

    WebDriverWait(driver, 10).until(lambda d: len(get_articles(d)) > old_article_count)


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


def puzzle_check(driver):
    """Функция проверки наличия пазла по фразе"""
    try:
        driver.find_element(By.XPATH, "//span[contains(text(), 'Хватай свой пазл!')]")
        return True
    except NoSuchElementException:
        return False
