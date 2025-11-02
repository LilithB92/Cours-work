import datetime
import logging
import os.path
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

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


if __name__ == "__main__":
    print(get_greeting())
    # print(get_month_period("2021-12-30 08:16:00"))
    print(read_excel("po"))
