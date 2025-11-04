import json
import logging
import os
from functools import wraps
from pathlib import Path
from typing import Any
from typing import Callable

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
