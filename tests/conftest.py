import datetime
import json

import pandas as pd
import pytest
from numpy import nan


@pytest.fixture
def stock_price_expected() -> list[dict]:
    result = [
        {"stock": "AAPL", "price": 70.24},
        {"stock": "AMZN", "price": 70.24},
        {"stock": "GOOGL", "price": 70.24},
        {"stock": "MSFT", "price": 70.24},
        {"stock": "TSLA", "price": 70.24},
    ]

    return result


@pytest.fixture
def cards_datas_expected() -> list[dict]:
    result = [
        {"last_digits": "*5091", "total_spent": -10187.64, "cashback": 343.0},
        {"last_digits": "*4556", "total_spent": 2547.1, "cashback": 41.0},
        {"last_digits": "*7197", "total_spent": -5306.53, "cashback": 88.0},
    ]
    return result


@pytest.fixture
def dataframe_returner() -> pd.DataFrame:
    data = {
        "Номер карты": ["*5091", "*4556", "*7197"],
        "Сумма платежа": [-10187.64, 2547.1, -5306.53],
        "Бонусы (включая кэшбэк)": [
            343.0,
            41.0,
            88.0,
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture
def top_data_expected() -> list[dict]:
    result = [
        {
            "amount": 190044.51,
            "category": "Переводы",
            "date": "21.03.2019",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "amount": -190044.51,
            "category": "Переводы",
            "date": "21.03.2019",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
    ]
    return result


@pytest.fixture
def top_dataframe() -> pd.DataFrame:
    data = {
        "Дата платежа": ["02.12.2021", "05.12.2021"],
        "Сумма операции": [-5510.8, 3500.0],
        "Категория": ["Каршеринг", "Пополнения"],
        "Описание": ["Ситидрайв", "Внесение наличных через банкомат Тинькофф"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def data_for_search() -> list[dict]:
    data = [
        {"Дата операции": "2021-6-12", "Сумма операции": 345.96, "Категория": "Пере", "описании": "Валерий А."},
        {
            "Дата операции": "2021-05-2",
            "Сумма операции": 100,
            "Категория": "Переводы",
            "описании": "Тинькофф Мобайл +7 995 555-55-55 А.",
        },
        {
            "Дата операции": "2021-05-13",
            "Сумма операции": 134.14,
            "Категория": "Переводы",
            "описании": "Тинькофф Валерий А. Мобайл +7 995 555-55-55 ",
        },
    ]
    return data


@pytest.fixture
def data_for_cashback() -> list[dict]:
    data = [
        {
            "Дата операции": "05.12.2021 16:42:04",
            "Сумма операции с округлением": 345.96,
            "Категория": "Пере",
        },
        {
            "Дата операции": "12.12.2021 16:32:04",
            "Сумма операции с округлением": 100,
            "Категория": "Переводы",
        },
        {
            "Дата операции": "31.12.2021 12:12:04",
            "Сумма операции с округлением": 134.14,
            "Категория": "Переводы",
        },
    ]
    return data


@pytest.fixture
def reports_tests_data() -> pd.DataFrame:
    data = [
        {
            "Дата платежа": datetime.datetime.strptime("17.04.2021 16:44:00", "%d.%m.%Y %H:%M:%S"),
            "Сумма платежа": 345.96,
            "Категория": "Пере",
        },
        {
            "Дата платежа": datetime.datetime.strptime("10.04.2021 16:44:00", "%d.%m.%Y %H:%M:%S"),
            "Сумма платежа": 100,
            "Категория": "Каршеринг",
        },
        {
            "Дата платежа": datetime.datetime.strptime("11.05.2021 16:44:00", "%d.%m.%Y %H:%M:%S"),
            "Сумма платежа": 134.14,
            "Категория": "Каршеринг",
        },
    ]
    return pd.DataFrame(data)


@pytest.fixture
def weekday_spending_expected() -> str:
    data = [
        {"Monday": nan},
        {"Tuesday": nan},
        {"Wednesday": nan},
        {"Thursday": nan},
        {"Friday": nan},
        {"Saturday": 222.98},
        {"Sunday": nan},
    ]
    return json.dumps(data, ensure_ascii=False, indent=4)
