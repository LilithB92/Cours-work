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
    excel_file = os.path.join(directory_name, "data", filename + ".xlsx")
    try:
        logger.info("Открываем Excel-файл с данными о финансовых транзакциях и вернет DataFrame")
        excel_data = pd.read_excel(excel_file, engine="openpyxl")
        return excel_data
    except FileNotFoundError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return pd.DataFrame()


def get_race_currency() -> list[dict]:
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
            payload:  Dict[str, Any] = {"amount": 1, "from": currency, "to": "RUB"}
            response = requests.get(url, headers=headers, params=payload)
            if response.status_code == 200:
                rate.append({"currency": currency, "rate": round(response.json()["result"], 2)})
        return rate
    except (JSONDecodeError, TypeError, KeyError, ValueError, AssertionError) as ex:
        logger.error(f"Ошибка получение курс валют: {ex}")
        return [{}]


if __name__ == "__main__":
    print(get_greeting())
    # print(get_month_period("2021-12-30 08:16:00"))
    # print(read_excel("po"))
    # print(get_race_currency())
