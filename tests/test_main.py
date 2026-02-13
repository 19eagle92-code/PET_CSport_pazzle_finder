import requests
import pytest
from main import get_response

BASE_URL = "https://www.cybersport.ru/tags/dota-2"


def test_response():
    assert get_response(BASE_URL).status_code == 200


def test_response_1():
    result = get_response(BASE_URL)
    assert result.status_code == 200
