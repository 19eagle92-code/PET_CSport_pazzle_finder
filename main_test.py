import requests
import re
from bs4 import BeautifulSoup


URL = "https://habr.com/ru/articles/"
BASE_URL = "https://habr.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

response = requests.get(URL, headers=HEADERS)
print(response)
