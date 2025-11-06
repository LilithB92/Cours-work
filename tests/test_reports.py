import datetime

import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from src.reports import filtered_by_date
from src.reports import spending_by_category
from src.reports import spending_by_weekday


def test_filtered_by_date(reports_tests_data: pd.DataFrame) -> None:
    data = [
        {
            "Дата платежа": datetime.datetime.strptime("17.04.2021 16:44:00", "%d.%m.%Y %H:%M:%S"),
            "Сумма платежа": 345.96,
            "Категория": "Пере",
        },
        {
            "Дата платежа": datetime.datetime.strptime("10.04.2021 16:44:00", "%d.%m.%Y %H:%M:%S"),
            "Сумма платежа": 100,
            "Категория": "Каршеринг",
        },
    ]

    expected = pd.DataFrame(data)
    result = filtered_by_date(reports_tests_data, "23.04.2021")
    assert_frame_equal(result, expected)


def test_filtered_by_date_invalide() -> None:
    with pytest.raises(ValueError):
        assert filtered_by_date(pd.DataFrame(), "23.04.2021")


def test_spending_by_category_invalid() -> None:
    with pytest.raises(ValueError):
        assert spending_by_category(pd.DataFrame(), "23.04.2021")


def test_spending_by_weekday(reports_tests_data: pd.DataFrame, weekday_spending_expected: str) -> None:
    assert spending_by_weekday(reports_tests_data, "23.04.2021") == weekday_spending_expected


def test_spending_by_weekday_invalid() -> None:
    assert spending_by_weekday(pd.DataFrame(), "23.04.2021") == ""
