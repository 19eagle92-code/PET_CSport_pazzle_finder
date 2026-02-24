from src.config import URL, BASE_URL, target_date_str
from src.db import init_db, save_article
from src.driver import create_driver, open_site, close_browser
from src.scraper.article_page import (
    get_articles,
    get_article_link,
    get_article_date,
    get_article_title,
    puzzle_check,
    load_more,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime


import time

if __name__ == "__main__":

    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")

    driver = create_driver()

    open_site(driver, BASE_URL)

    processed_count = 0
    start_time = time.time()

    conn = init_db()

    try:
        while True:

            articles = get_articles(driver)

            if not articles:
                break

            new_articles = articles[processed_count:]

            # last_date = get_last_article_date(articles)

            for article in new_articles:

                link = get_article_link(article)
                # print(link)
                article_date = get_article_date(article)

                title = get_article_title(article)

                article_date_obj = datetime.strptime(article_date, "%Y-%m-%d")

                if article_date_obj <= target_date:
                    print("Достигнута целевая дата")
                    break

                driver.execute_script("window.open(arguments[0]);", link)
                driver.switch_to.window(driver.window_handles[1])

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//span[contains(text(),'Хватай свой пазл!') or contains(text(), 'Тут пазла нет!')]",
                        )
                    )
                )

                has_puzzle = puzzle_check(driver)

                if has_puzzle:
                    print(f"{article_date}--{title}--{link}")

                try:
                    save_article(conn, link, article_date, has_puzzle)
                except Exception as e:
                    print(f"Ошибка при сохранении статьи {title}: {e}")

                # else:
                #     print("Здесь пазла нет")

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            conn.commit()

            # if link in seen_links:
            #     continue

            # seen_links.add(link)

            processed_count = len(articles)

            load_more(driver)
            new_count = len(get_articles(driver))

            if new_count == processed_count:
                print("Статьи закончились")
                break
    finally:
        conn.close()
        close_browser(driver)

        end_time = time.time()
        execution_time = end_time - start_time
        hours = int(execution_time // 3600)
        minutes = int((execution_time % 3600) // 60)
        seconds = execution_time % 60

        if hours > 0:
            print(f"Время выполнения: {hours}ч {minutes}мин {seconds:.1f}с")
        elif minutes > 0:
            print(f"Время выполнения: {minutes}мин {seconds:.1f}с")
        else:
            print(f"Время выполнения: {seconds:.2f}с")
        exit()
