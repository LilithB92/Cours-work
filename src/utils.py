import datetime
import logging
import os.path
from pathlib import Path

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


if __name__ == "__main__":
    print(get_greeting())
