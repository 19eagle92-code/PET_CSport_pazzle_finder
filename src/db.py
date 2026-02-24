import sqlite3
from src.config import DB_PATH


def init_db():
    """Функцуия создания таблицы ДБ"""
    conn = sqlite3.connect(DB_PATH)
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
