import json
import logging
import os
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

import pandas as pd

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


def raised_cashback_for_categories(transactions: list[dict], year: int, month: int) -> str:
    """
    Анализирует сколько на каждой категории можно заработать кэшбэка, данном месяце году,
     если процент кешбэк 1%. И вернет  JSON с анализом, сколько на каждой категории можно заработать кэшбэка:
     {"Категория 1": 1000, "Категория 2": 2000, "Категория 3": 500}

    :param transactions: Данные с транзакциями;
    :param year:год, за который проводится анализ;
    :param month: месяц, за который проводится анализ.
    :return: JSON с анализом, сколько на каждой категории можно заработать кешбэка.
    """
    try:
        logger.info("фильтрация данных")
        df = pd.DataFrame(transactions)
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


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Можно задать комфортный порог округления: 10, 50 или 100 ₽.
    Траты будут округляться, и разница между фактической суммой трат по карте и
    суммой округления будет попадать на счет «Инвесткопилки».

    :param month: месяц, для которого рассчитывается отложенная сумма (строка в формате 'YYYY-MM').
    :param transactions: список словарей, содержащий информацию о транзакциях, в которых содержатся следующие поля:
    Дата операции— дата, когда произошла транзакция (строка в формате 'YYYY-MM-DD').
    Сумма операции— сумма транзакции в оригинальной валюте (число).
    :param limit: предел, до которого нужно округлять суммы операций (целое число).
    :return: сумму, которую удалось бы отложить в «Инвесткопилку»
    """
    try:
        if transactions:
            logger.info("Округление трат")
            divider = 10
            if limit > 10:
                divider = 100
            investments = [
                (limit - (tr["Сумма операции"] % divider))
                for tr in transactions
                if (tr["Дата операции"][:7] == month)
                and (0 < (limit - (tr["Сумма операции"] % divider)) < limit)
            ]
            return round(float(sum(investments)), 2)
        raise Exception
    except Exception as ex:
        logger.error(f"Ошибка получение  сумму, которую нужно отложить в «Инвесткопилку»: {ex}")
        return 0.00


if __name__ == "__main__":
    # trans = read_excel("operations")
    # json_df = df.to_json(orient='records', force_ascii=False, indent = 4)
    # json_dict =json.loads(json_df)
    # print(type(json_dict))
    data = [
        {"Дата операции": "2021-6-12", "Сумма операции": 345.96},
        {"Дата операции": "2021-05-2", "Сумма операции": 100},
        {"Дата операции": "2021-05-13", "Сумма операции": 134.14},
    ]
    print(investment_bank("2021-05", data, 10))

    # print(type(raised_cashback_for_categories(trans, 2021, 5)))
