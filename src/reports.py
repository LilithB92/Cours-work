import datetime
import json
import logging
import os
from functools import wraps
from json import JSONDecodeError
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import read_excel

directory_name = Path(__file__).resolve().parent.parent
log_path = os.path.join(directory_name, "logs", "reports.log")

logging.basicConfig(
    filename=log_path,
    format="%(asctime)s - %(filename)s - %(levelname)s:  %(message)s",
    filemode="w",
    level=logging.DEBUG,
    encoding="utf-8",
)

logger = logging.getLogger()


def log(filename: str = "user_settings") -> Callable[..., Any]:
    """
    Декоратор  результат  функции сохраняет в файл.

    :param filename: Название файла, где сохраняет результат  функции
    :return: результат функции(если функция не выдает ошибки) или строка(если функция выдает ошибки)
    """

    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                logger.info("получение результат  функции ")
                user_settings_file = os.path.join(directory_name, filename + ".json")
                result = func(*args, **kwargs)
                logger.info(f"сохранение результат функции в файл : {result}")
                with open(user_settings_file, "w", encoding="utf-8") as file:
                    json.dump(result, file)
                return result
            except Exception as ex:
                logger.error(f"Ошибка сохранение результат функции в файл: {ex}")
                return "file have not saved"

        return inner

    return wrapper


def filtered_by_date(df: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция принимает датафрейм с транзакциями, категории, дату.
    Функция филтрует транзакции за последние три месяца (от переданной даты

    :param df: датафрейм с транзакциями
    :param date: опциональную дату в формате 'dd.mm.YYYY'
    :return: транзакции за последние три месяца (от переданной даты)
    """
    try:
        logger.info("фильтрация транзакции за последние три месяца")
        df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")
        date_format = "%d.%m.%Y"
        if not date:
            date = datetime.datetime.now().strftime(date_format)
        dt = datetime.datetime.strptime(date, date_format)
        logger.info(f"получение даты: {dt}")
        past_datetime = dt - relativedelta(months=3)
        filtered_by_date = df[(df["Дата платежа"] >= past_datetime) & (df["Дата платежа"] <= dt)]

        return filtered_by_date
    except (KeyError, TypeError, AssertionError) as ex:
        logger.error(f"Ошибка получение транзакции за последние три месяца : {ex}")
        return pd.DataFrame()


def spending_by_category(df: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция принимает датафрейм с транзакциями, категории, дату.
    Функция филтрует траты по заданной категории за последние три месяца (от переданной даты
    Если дата не передана, то берется текущая дата.

    :param df: датафрейм с транзакциями,
    :param category: название категории
    :param date: опциональную дату в формате 'dd.mm.YYYY'.
    :return: траты по заданной категории за последние три месяца (от переданной даты)
    """
    try:
        date_df = filtered_by_date(df, date)
        filter_category = date_df[date_df["Категория"] == category]
        logger.info("получение траты по заданной категории за последние три месяца")
        return filter_category[["Дата платежа", "Категория", "Сумма платежа"]]
    except Exception as ex:
        logger.error(f"Ошибка получение траты по заданной категории за последние три месяца: {ex}")
        return pd.DataFrame()


def spending_by_weekday(df: pd.DataFrame, date: Optional[str] = None) -> str:
    """
    Функция принимает датафрейм с транзакциями,  дату.
    Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)
    Если дата не передана, то берется текущая дата.

    :param df:датафрейм с транзакциями
    :param date:опциональную дату в формате 'dd.mm.YYYY'
    :return: Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)
    """
    try:
        filter_df = filtered_by_date(df, date)
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        data = []
        for weekday in weekdays:
            filter_by_weekday = filter_df[filter_df["Дата платежа"].dt.day_name() == weekday]
            avg_amount = filter_by_weekday["Сумма платежа"].mean()
            if avg_amount:
                avg_amount = 0.00
            data.append({weekday: round(float(avg_amount), 2)})
        logger.info(f"получение средние траты в каждый из дней недели за последние три месяца: {data}")
        return json.dumps(data, ensure_ascii=False, indent=4)
    except (KeyError, JSONDecodeError, TypeError, AssertionError) as ex:
        logger.error(f"Ошибка получение средние траты в каждый из дней недели за последние три месяца : {ex}")
        return ""


def spending_by_workday(df: pd.DataFrame, date: Optional[str] = None) -> str:
    """
    Функция принимает датафрейм с транзакциями,  дату.
    Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты).
    Если дата не передана, то берется текущая дата.

    :param df:датафрейм с транзакциями
    :param date:опциональную дату в формате 'dd.mm.YYYY'
    :return: Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты).
    """
    weekday_spending = spending_by_weekday(df, date)
    if weekday_spending:
        weekday_data = json.loads(weekday_spending)
        result = {"рабочий день": weekday_data[:5], "выходной день": weekday_data[5:]}
        logger.info(f"средние траты в рабочий и в выходной день за последние три месяца(от переданной даты): {result}")
        return json.dumps(result, ensure_ascii=False, indent=4)
    logger.error("Ошибка получение  средние траты в рабочий и в выходной день за последние три месяца")
    return ""


if __name__ == "__main__":
    dtf = read_excel("operations")
    # print(spending_by_category(dtf,"Супермаркеты",'21.03.2021' ))
    print(spending_by_workday(dtf, "21.03.2026"))
