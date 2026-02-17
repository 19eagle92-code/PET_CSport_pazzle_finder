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


options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")


driver = webdriver.Chrome(options=options)
driver.get(BASE_URL)
# 2026-02-12
time.sleep(2)


def article_finder(n):
    """Функция парсинга элементов на сайте (статей)"""
    markup = driver.page_source
    soup = BeautifulSoup(markup, "html.parser")
    articles = soup.find_all(n)
    return articles


print(len(article_finder("article")))


button = driver.find_element(By.XPATH, "//button[contains(text(),'показать еще')]")

if button:
    print(f"Найдена кнопока")
    actions = ActionChains(driver)
    actions.move_to_element(button).perform()
    time.sleep(1)
    try:
        button.click()
    except:
        # Если обычный клик не работает, пробуем JavaScript клик
        driver.execute_script("arguments[0].click();", button)

else:
    print("Кнопка не найдена")
    # Если кнопка не найдена пролистываем до конца страницы
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# =============================================================


# button = driver.find_element(
#     By.XPATH,
#     "//button[contains(translate(text(), 'ПОКАЗАТЬ ЕЩЕ', 'показать еще'), 'показать еще')]",
# )

# if button:
#     print(f"Найдена кнопока")
# else:
#     print("Кнопка не найдена")

# # driver.execute_script(
# #     "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button
# # )


# # Теперь пробуем кликнуть
# try:
#     button.click()
# except:
#     # Если обычный клик не работает, пробуем JavaScript клик
#     driver.execute_script("arguments[0].click();", button)
#     print("кнопка нажата тут")
#     time.sleep(2)
# markup = driver.page_source
# soup = BeautifulSoup(markup, "html.parser")
# articles = soup.find_all("article")
# print(len(articles))
# print(type(articles))

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(2)

# # actions.move_to_element(articles[-1]).perform()

# markup = driver.page_source
# soup = BeautifulSoup(markup, "html.parser")
# articles = soup.find_all("article")
# print(len(articles))

# if len(articles) < 200:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)

# markup = driver.page_source
# soup = BeautifulSoup(markup, "html.parser")
# articles = soup.find_all("article")

# print(len(articles))

# ==============================================
# button.click()
# time.sleep(2)
# print(len(articles))


# while True:
#     try:
#         button = driver.find_element(
#             By.XPATH, "//button[contains(text(),'Показать ещё')]"
#         )
#         button.click()
#         time.sleep(2)
#         markup = driver.page_source
#         soup = BeautifulSoup(markup, "html.parser")
#         articles = soup.find_all("article")
#         print(len(articles))

#     except:
#         break

# max_iterations = 3

# for i in range(max_iterations):
#     try:
#         button = driver.find_element(
#             By.XPATH, "//button[contains(text(),'Показать еще')]"
#         )
#         button.click()
#         time.sleep(2)

#         markup = driver.page_source
#         soup = BeautifulSoup(markup, "html.parser")
#         articles = soup.find_all("article")
#         print(f"Итерация {i+1}: {len(articles)} статей")

#     except:
#         print("Кнопка 'Показать еЕЩЕ' не найдена")
#         break

# button = driver.find_element(
#             By.XPATH, "//button[contains(text(),'Показать ещё')]"
#         )


# while True:
#     try:
#         button = driver.find_element(
#             By.XPATH, "//button[contains(text(),'Показать ещё')]"
#         )
#         button.click()
#         articles = driver.find_elements(By.CSS_SELECTOR, "article")
#         if len(articles) == 50:
#             print(len(articles))
#             break
#             # time.sleep(2)
#     except:
#         break


# <button class="button_+fnen type-bordered_w6rMh">Показать еще</button>


# def web_driver(URL):

#     driver = webdriver.Chrome(options=options)
#     driver.get(URL)

#     markup = driver.page_source
#     soup = BeautifulSoup(markup, "html.parser")

#     elements = driver.find_elements(
#         By.XPATH, "//*[contains(text(), 'Хватай свой пазл!')]"
#     )
#     driver.quit()

#     return elements


# for article in track(articles, description="Прогресс поиска"):
#     print("\n[bold magenta]Поиск по сайтам:[/bold magenta]")
#     # Ищем заголовок
#     title_tag = article.find("h3")
#     # print(title_tag.text)
#     if not title_tag:
#         continue
#     title = title_tag.text.strip()
#     # print(title)

#     # Ищем ссылку
#     link = article.find("a")["href"]
#     # print(link)

#     if link.startswith("/"):
#         link = URL + link
#         # print(link)

#     # Ищем дату
#     date_tag = article.find("time")
#     date = date_tag["datetime"][:10] if date_tag else "Без даты"
#     # print(date)

#     #     # Видимый текст статьи
#     preview_text = article.get_text().lower()

#     # Проверяем ключевые слова по заголовку
#     if web_driver(link):
#         print(f"{date} – {title} – {link}")
#     else:
#         print("Пазла тут нет")


# print("\n[bold green]✓ Поиск завершен![/bold green]")
# if __name__ == "__main__":


# <button class="button_+fnen type-bordered_w6rMh">Показать еще</button>
