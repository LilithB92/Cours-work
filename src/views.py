import pandas as pd

from src.utils import get_greeting


def get_page_main_datas(date: str)->pd.DataFrame():
   """
   Функция реализуйте набор функций и главную функцию, принимающую на вход строку с датой и временем в формате
   YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными: 1. Приветствие;
   2. По каждой карте: последние 4 цифры карты; общая сумма расходов; кешбэк (1 рубль на каждые 100 рублей).
   3.Топ-5 транзакций по сумме платежа; 4. Курс валют; 5. Стоимость акций из S&P500.
   :param date: строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
   :return:  JSON-ответ
   """
   greeting = get_greeting()
   


def for_page_event(data_frame):
   pass
