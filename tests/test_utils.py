from pathlib import Path
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest
from freezegun import freeze_time

import src.utils
from src.utils import get_each_cards_datas
from src.utils import get_month_period
from src.utils import get_rate_currency
from src.utils import read_excel
from src.utils import stock_price
from src.utils import top_transactions_by_paymant

directory_name = Path(__file__).resolve().parent.parent


def test_get_month_period() -> None:
    assert get_month_period("2021-12-30 08:16:00") == ["01.12.2021 08:16:00", "30.12.2021 08:16:00"]


@freeze_time("2025-01-01 12:10:20")
def test_get_greeting_afternoon() -> None:
    assert src.utils.get_greeting() == "Добрый день"


@freeze_time("2025-01-01 09:25:12")
def test_get_greeting_morning() -> None:
    assert src.utils.get_greeting() == "Доброе утро"


@freeze_time("2025-01-01 17:35:12")
def test_get_greeting_evening() -> None:
    assert src.utils.get_greeting() == "Добрый вечер"


@freeze_time("2025-01-01 23:35:12")
def test_get_greeting_night() -> None:
    assert src.utils.get_greeting() == "Доброй ночи"


@patch("src.utils.requests.get")
def test_get_rate_currency_invalid(mocked_get: Any) -> None:
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = [{}]
    result = get_rate_currency()
    assert result == [{}]


@patch("src.utils.requests.get")
def test_get_rate_currency_(mocked_get: Any) -> None:
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {"result": 70.24}
    result = get_rate_currency()
    assert result == [{"currency": "EUR", "rate": 70.24}, {"currency": "USD", "rate": 70.24}]


@patch("src.utils.requests.get")
def test_stock_price_invalid(mocked_get: Any) -> None:
    mocked_get.return_value.json.return_value = {}
    result = stock_price()
    assert result == [{}]


@patch("src.utils.requests.get")
def test_stock_price(mocked_get: Any, stock_price_expected: list[dict]) -> None:
    mocked_get.return_value.json.return_value = {"price": 70.24, "stock": "AMZN"}
    result = stock_price()
    assert result == stock_price_expected


def test_get_each_cards_datas(cards_datas_expected: list[dict], dataframe_returner: pd.DataFrame) -> None:
    assert get_each_cards_datas(dataframe_returner) == cards_datas_expected


def test_get_each_cards_with_empty_datas() -> None:
    assert get_each_cards_datas(pd.DataFrame()) == [{}]


def test_top_transactions_by_paymant(top_data_expected: list[dict]) -> None:
    trans = read_excel("operations")
    assert top_transactions_by_paymant(trans, 2) == top_data_expected


def test_top_transactions_by_paymant_with_empty_datas() -> None:
    assert top_transactions_by_paymant(pd.DataFrame()) == [{}]


def test_read_excel_not_existed_file() -> None:
    with pytest.raises(ValueError):
        assert read_excel("not_existed_file")
