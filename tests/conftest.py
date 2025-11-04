import pandas as pd
import pytest

@pytest.fixture
def stock_price_expected()->list[dict]:
    result = [
        {
            "stock": "AAPL",
            "price": 70.24
        },
        {
            "stock": "AMZN",
            "price": 70.24
        },
        {
            "stock": "GOOGL",
            "price": 70.24
        },
        {
            "stock": "MSFT",
            "price": 70.24
        },
        {
            "stock": "TSLA",
            "price": 70.24
        }
    ]

    return result

@pytest.fixture
def cards_datas_expected()->list[dict]:
    result =  [
            {
                "last_digits": "*5091",
                "total_spent": -10187.64,
                "cashback": 343.0
            },
            {
                "last_digits": "*4556",
                "total_spent": 2547.1,
                "cashback": 41.0
            },
            {
                "last_digits": "*7197",
                "total_spent": -5306.53,
                "cashback": 88.0
            }
        ]
    return result

@pytest.fixture
def dataframe_returner()->pd.DataFrame:
    data = {
        'Номер карты': ['*5091', '*4556', '*7197'],
        'Сумма платежа': [-10187.64, 2547.1,-5306.53],
        'Бонусы (включая кэшбэк)': [343.0, 41.0, 88.0,]
    }
    return  pd.DataFrame(data)


@pytest.fixture
def top_data_expected()->list[dict]:
    result = [
        {'amount': 190044.51,
        'category': 'Переводы',
        'date': '21.03.2019',
        'description': 'Перевод Кредитная карта. ТП 10.2 RUR'},
        {'amount': -190044.51,
        'category': 'Переводы',
        'date': '21.03.2019',
        'description': 'Перевод Кредитная карта. ТП 10.2 RUR'}
    ]
    return result

@pytest.fixture
def top_dataframe()->pd.DataFrame:
    data = {
        'Дата платежа': ['02.12.2021', '05.12.2021'],
        'Сумма операции': [-5510.8, 3500.0 ],
        'Категория': ["Каршеринг", "Пополнения" ],
        'Описание': ["Ситидрайв", "Внесение наличных через банкомат Тинькофф" ],
    }
    return pd.DataFrame(data)