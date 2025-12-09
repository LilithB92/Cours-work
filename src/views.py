import json

import pandas as pd

from src.utils import get_each_cards_datas
from src.utils import get_greeting
from src.utils import get_month_period
from src.utils import get_rate_currency
from src.utils import read_excel
from src.utils import stock_price
from src.utils import top_transactions_by_paymant


def get_page_main_datas(date: str) -> str:
    """
    Функция реализуйте набор функций и главную функцию, принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными: 1. Приветствие;
    2. По каждой карте: последние 4 цифры карты; общая сумма расходов; кешбэк (1 рубль на каждые 100 рублей).
    3.Топ-5 транзакций по сумме платежа; 4. Курс валют; 5. Стоимость акций из S&P500.
    :param date: строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    :return:
     JSON-ответ
    """
    tr = read_excel("operations")
    month_period = get_month_period(date)

    filtered_df = tr[
        (pd.to_datetime(tr["Дата операции"], dayfirst=True) >= pd.to_datetime(month_period[0], dayfirst=True))
        & (pd.to_datetime(tr["Дата операции"], dayfirst=True) <= pd.to_datetime(month_period[1], dayfirst=True))
    ]

    greeting = get_greeting()
    currency_rates = get_rate_currency()
    stock_prices = stock_price()
    top_transactions = top_transactions_by_paymant(filtered_df)
    cards = get_each_cards_datas(filtered_df)

    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    return json.dumps(data, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(get_page_main_datas("2021-12-10 08:16:00"))
