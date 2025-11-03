import json
import logging
import os
from pathlib import Path

import pandas as pd

from src.utils import read_excel

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


def raised_cashback_for_categories(df: pd.DataFrame, year: int, month: int) -> str:
    """
    Анализирует сколько на каждой категории можно заработать кэшбэка, данном месяце году,
     если процент кешбэк 1%. И вернет  JSON с анализом, сколько на каждой категории можно заработать кэшбэка:
     {"Категория 1": 1000,
    "Категория 2": 2000,
    "Категория 3": 500}

    :param df: Данные с транзакциями;
    :param year:год, за который проводится анализ;
    :param month: месяц, за который проводится анализ.
    :return: JSON с анализом, сколько на каждой категории можно заработать кешбэка.
    """
    try:
        logger.info("фильтрация данных")
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        filtered_df = df[(df["Дата операции"].dt.year == year) & (df["Дата операции"].dt.month == month)]
        categories = filtered_df["Категория"].dropna().unique()
        logger.info(f"получение категории: {categories}")
        sum_amount_by_category = filtered_df.groupby("Категория")["Сумма операции с округлением"].sum()
        data = {}
        for category in categories:
            if category in ["Наличные", "Пополнения"]:
                continue
            data[category] = round(float(sum_amount_by_category[category]) / 100, 2)
        return json.dumps(data, ensure_ascii=False, indent=4)
    except Exception as ex:
        logger.error(f"Ошибка получение JSON с анализом  кешбэка: {ex}")
        return ""


if __name__ == "__main__":
    trans = read_excel("operations")
    # json_df = df.to_json(orient='records', force_ascii=False, indent = 4)
    # json_dict =json.loads(json_df)
    # print(type(json_dict))

    print(type(raised_cashback_for_categories(trans, 2021, 5)))
