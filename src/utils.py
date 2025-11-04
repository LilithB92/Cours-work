import datetime
import logging
import os.path
from pathlib import Path
from typing import Any
from typing import Dict

import pandas as pd
import requests
from dotenv import load_dotenv
from requests import JSONDecodeError

load_dotenv()
api_key = os.getenv("API_KEY")
x_api_key = os.getenv("X-Api-Key")
directory_name = Path(__file__).resolve().parent.parent
log_path = os.path.join(directory_name, "logs", "utils.log")

logging.basicConfig(
    filename=log_path,
    format="%(asctime)s - %(filename)s - %(levelname)s:  %(message)s",
    filemode="w",
    level=logging.DEBUG,
    encoding="utf-8",
)

logger = logging.getLogger()


def get_greeting() -> str:
    """
    Функция приветствие в формате «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени.
    :return: Строка «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи».
    """
    logger.info("получение даты и времени пользователя, ее настройка для получения времени")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    logger.info("определение сообщения приветствия")
    if "07:00:00" <= current_time <= "10:00:00":
        greet = "ое утро"
    elif "10:00:01" <= current_time <= "16:00:00":
        greet = "ый день"
    elif "16:00:01" <= current_time <= "22:00:00":
        greet = "ый вечер"
    else:
        greet = "ой ночи"

    return f"Добр{greet}"


def get_month_period(date_time: str) -> list[str]:
    """
    Функция меняет формат даты и фильтрует от начала месяца до указанного числа
    :param date_time: Дата в формате YYYY-MM-DD HH:MM:SS
    :return:список из дат начала месяца и указанного числа месяца
    """
    from_format_date = "%Y-%m-%d %H:%M:%S"
    to_formated_date = "%d.%m.%Y %H:%M:%S"
    logger.info("настройка интервала дат от 1 числа месяца до указанного")
    dt = datetime.datetime.strptime(date_time, from_format_date)
    first_day_of_month = dt.replace(day=1)
    return [first_day_of_month.strftime(to_formated_date), dt.strftime(to_formated_date)]


def read_excel(filename: str) -> pd.DataFrame:
    """
    Функция читает финансовых операций из Excel и возврашает DataFrame с транзакциями.

    :param filename:Имя файла Excel
    :return:DataFrame с транзакциями.
    """
    try:
        excel_file = os.path.join(directory_name, "data", filename + ".xlsx")
        logger.info("Открываем Excel-файл с данными о финансовых транзакциях и вернет DataFrame")
        excel_data = pd.read_excel(excel_file, engine="openpyxl")
        return excel_data
    except (FileNotFoundError, ValueError, AttributeError ) as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return pd.DataFrame()


def get_each_cards_datas(df: pd.DataFrame) -> list[dict]:
    """
    Функция принимает DataFrame с транзакциями и возврашает список словарей:
    По каждой карте: последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей).

    :param df:DataFrame с транзакциями
    :return:список словарей
    """
    try:
        card_datas = []
        card_numbers = df["Номер карты"].dropna().unique()
        logger.info(f"получение Номера карты: {card_numbers}")
        grouped_by_card = df.groupby("Номер карты")
        for card_number in card_numbers:
            amount = grouped_by_card["Сумма платежа"].sum()
            cashback = grouped_by_card["Бонусы (включая кэшбэк)"].sum()
            card_datas.append(
                {
                    "last_digits": card_number,
                    "total_spent": float(amount[card_number]),
                    "cashback": float(cashback[card_number]),
                }
            )
        return card_datas
    except Exception as ex:
        logger.error(f"Произошла ошибка в получение информации карты : {ex}")
        return [{}]


def get_rate_currency() -> list[dict]:
    """
    Функция обращает к внешнему API (https://apilayer.com/marketplace/exchangerates_data-api)
    для получения текущего курса валют "EUR" и "USD" в рублях

    :return: список словарей с валютами и курсами валют
    """
    currencies = ["EUR", "USD"]
    rate = []
    try:
        logger.info("Oбращаем к внешнему API ля получения текущего курса валют EUR и USD в рублях")
        for currency in currencies:
            url = "https://api.apilayer.com/exchangerates_data/convert"
            headers = {"apikey": api_key}
            payload: Dict[str, Any] = {"amount": 1, "from": currency, "to": "RUB"}
            response = requests.get(url, headers=headers, params=payload)
            if response.status_code == 200:
                rate.append({"currency": currency, "rate": round(response.json()["result"], 2)})
        return rate
    except (JSONDecodeError, TypeError, KeyError, ValueError, AssertionError) as ex:
        logger.error(f"Ошибка получение курс валют: {ex}")
        return [{}]


def top_transactions_by_paymant(df: pd.DataFrame, limit: int = 5) -> list[dict[Any, Any]]:
    """
    Функция принимает DataFrame транзакций по сумме платежа, топ число трансакции.Она возвращает tоп-лимит транзакции.

    :param df: Транзакции по сумме платежа
    :param limit: Лимит топ числа
    :return: Топ-5 транзакций по сумме платежа
    """
    try:
        logger.info("Получаем топ-5 транзакции по сумме платежа")
        indexes_of_top_trans = df["Сумма операции с округлением"].nlargest(limit).keys()
        logger.info(f"Получаем индекса топ-5 транзакции : {indexes_of_top_trans}")
        top_transactions = []
        for index in indexes_of_top_trans:
            top_transactions.append(
                {
                    "date": df["Дата платежа"][index],
                    "amount": float(df["Сумма операции"][index]),
                    "category": df["Категория"][index],
                    "description": df["Описание"][index],
                }
            )
        return top_transactions
    except Exception as ex:
        logger.error(f"Ошибка получение топ-5 транзакции: {ex}")
        return [{}]


def stock_price() -> list[dict]:
    """
     Функция обращает к внешнему API (https://api-ninjas.com/api/stockprice) для получения
     стоимость акций из S&P500 ("AAPL", "AMZN", "GOOGL", "MSFT", "TSLA").

    :return: Список словарей тикерами и их ценами
    """
    try:
        logger.info("Oбращаем к внешнему API для получения стоимость акций из S&P500")
        stock_prices = []
        tickers = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        url = "https://api.api-ninjas.com/v1/stockprice"
        headers = {"X-Api-Key": x_api_key}
        for ticker in tickers:
            payload: Dict[str, str] = {"ticker": ticker}
            response = requests.get(url, headers=headers, params=payload)
            stock_prices.append({"stock": ticker, "price": response.json()["price"]})
        return stock_prices
    except Exception as ex:
        logger.error(f"Ошибка получение стоимость акций из S&P500: {ex}")
        return [{}]


if __name__ == "__main__":
    # print(get_greeting())
    print(get_month_period("2021-12-30 08:16:00"))
    # trans = read_excel("operations")
    # print(top_transactions_by_paymant(trans))
    # print(stoke_price())
    # print(get_race_currency())
    # print(get_each_cards_datas(trans))

