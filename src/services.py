import json
import logging
import os
import re
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

import pandas as pd
from black import JSONDecodeError

directory_name = Path(__file__).resolve().parent.parent
log_path = os.path.join(directory_name, "logs", "services.log")

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
        datas = {}
        for category in categories:
            if category in ["Наличные", "Пополнения"]:
                continue
            datas[category] = round(float(sum_amount_by_category[category]) / 100, 2)
        return json.dumps(datas, ensure_ascii=False, indent=4)
    except (ValueError, KeyError,TypeError,JSONDecodeError) as ex:
        logger.error(f"Ошибка получение JSON с анализом  кешбэка: {ex}")
        return "some"


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

        logger.info("Округление трат")
        divider = 10
        if limit > 10:
            divider = 100
        investments = [
            (limit - (tr["Сумма операции"] % divider))
            for tr in transactions
            if (tr["Дата операции"][:7] == month) and (0 < (limit - (tr["Сумма операции"] % divider)) < limit)
        ]
        return round(float(sum(investments)), 2)

    except (KeyError, AssertionError, TypeError) as ex:
        logger.error(f"Ошибка получение  сумму, которую нужно отложить в «Инвесткопилку»: {ex}")
        return 0.00


def simple_search(query: str, transactions: list[dict]) -> str:
    """
    Функция принимает строку — запрос  для поиска и транзакции в формате списка словарей.
    Функция  корректный JSON - ответ с транзакциями.

    :param query: Строку-запрос для поиска
    :param transactions: транзакции в формате списка словарей
    :return: JSON - ответ с транзакциями
    """
    try:
        logger.info("Поиск транзакции")
        pattern = rf"{query}"
        results = [trans for trans in transactions if re.search(pattern, str(trans), flags=re.IGNORECASE)]
        if not results:
            raise Exception
        logger.info(f"Получение транзакции:  {results}")
        return json.dumps(results, ensure_ascii=False, indent=4)
    except Exception as ex:
        logger.error(f"Ошибка получение транзакции : {ex}")
        return ""


def search_by_phonenumber(transactions: list[dict]) -> str:
    """
    Функция возвращает JSON со всеми транзакциями,
    содержащими в описании мобильные номера(Я МТС +7 921 11-22-33  Тинькофф Мобайл +7 995 555-55-55).

    :param transactions: транзакции в формате списка словарей
    :return: JSON - ответ с транзакциями
    """

    logger.info("Поиск транзакции по номеу телефона")
    pattern = r"\+\d{1} \d{3} \d{2,3}(-\d{2}){2}"

    results = [trans for trans in transactions if re.search(pattern, str(trans), flags=re.IGNORECASE)]
    logger.info(f"Получение транзакции:  {results}")
    return json.dumps(results, ensure_ascii=False, indent=4)


def search_by_name(transactions: list[dict]) -> str:
    """
    Функция принимает транзакции в формате списка словарей и возвращает JSON со всеми транзакциями,
    которые относятся к переводам физлицам. Категория такой транзакции — Переводы,
     а в описании есть имя и первая буква фамилии с точкой.
    Например: Валерий А. Сергей З. Артем П.

    :param transactions: Транзакции в формате списка словарей
    :return: JSON со всеми транзакциями, которые относятся к переводам физ лицам
    """
    try:
        logger.info("Поиск транзакции по номеу телефона")
        pattern = r"[А-ЯЁ]{1}[а-яё]* [А-ЯЁ]{1}\."

        results = [
            trans
            for trans in transactions
            if (trans["Категория"] == "Переводы") and (re.search(pattern, trans["описании"], flags=re.IGNORECASE))
        ]
        logger.info(f"Получение транзакции:  {results}")
        return json.dumps(results, ensure_ascii=False, indent=4)
    except (JSONDecodeError,ValueError,TypeError,AssertionError,KeyError) as ex:
        logger.error(f"Ошибка получение транзакции : {ex}")
        return ""


if __name__ == "__main__":
    # trans = read_excel("operations")
    # json_df = df.to_json(orient='records', force_ascii=False, indent = 4)
    # json_dict =json.loads(json_df)
    # print(type(json_dict))
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
    # print(investment_bank("2021-05", data, 100))
    # print(simple_search("6", data))
    # print(search_by_name(data))

    print(raised_cashback_for_categories(data, 2021, 12))
