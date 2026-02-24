# Csport_Pazl_finder

Скрипт на Python + Selenium для сканирования ленты Dota 2 на cybersport.ru и поиска статей, где встречается целевая фраза пазла (`"Хватай свой пазл!"`).  
Результаты сохраняются в SQLite базу данных.

## Возможности

- Открывает страницу тега Dota 2 и подгружает статьи кнопкой **"Показать еще"**
- Для каждой статьи открывает страницу в новой вкладке и проверяет наличие целевой фразы
- Сохраняет результаты в SQLite (`url`, `date`, `has_puzzle`)
- Останавливается:
  - при достижении `target_date`
  - либо если подряд встречается `N` статей без нужного пазла (защита на случай окончания акции/изменения разметки)

## Стек

- Python 3.10+
- Selenium
- SQLite3

## Установка

1. Создать и активировать виртуальное окружение:

bash
python -m venv .venv

### Windows PowerShell:
.venv\Scripts\Activate.ps1

2. Установить зависимости:

pip install -r requirements.txt

Также нужен установленный Google Chrome и совместимый ChromeDriver (обычно Selenium сам подтягивает драйвер, но зависит от окружения).

## Настройка

Файл src/config.py:

URL — базовый домен

BASE_URL — страница тега

target_date_str — дата остановки (YYYY-MM-DD)

DB_PATH — путь к базе данных

## Пример:

URL = "https://www.sport.ru"
BASE_URL = "https://www.sport.ru/tags/cs"
target_date_str = "2026-02-09"

DB_PATH = "data/articles.db"

## Запуск

Из корня проекта:

python -m src.main

## База данных

Создаётся таблица:

CREATE TABLE IF NOT EXISTS articles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT UNIQUE,
  date TEXT,
  has_puzzle INTEGER
);

has_puzzle: 1, если фраза найдена, иначе 0

## Примечания

Селектор пазла сейчас завязан на текст "Хватай свой пазл!". Если текст изменится — нужно обновить XPath в puzzle_check.

Скрипт рассчитан на личное использование и может потребовать адаптации при изменении верстки сайта.

## Лицензия

Для личного использования.