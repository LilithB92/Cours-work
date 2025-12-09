import datetime
import json
import os
from pathlib import Path
from typing import NoReturn

import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from src.reports import filtered_by_date
from src.reports import log_json_data
from src.reports import spending_by_category
from src.reports import spending_by_weekday
from src.reports import spending_by_workday


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


def test_spending_by_workday(reports_tests_data: pd.DataFrame, weekday_spending_expected: str) -> None:
    weekday_expected = json.loads(weekday_spending_expected)
    data = {"рабочий день": weekday_expected[:5], "выходной день": weekday_expected[5:]}
    expected = json.dumps(data, ensure_ascii=False, indent=4)
    assert spending_by_workday(reports_tests_data, "23.04.2021") == expected


def test_spending_by_workday_invalid() -> None:
    assert spending_by_workday(pd.DataFrame(), "23.04.2021") == ""


def test_log_json_data_decorator_writes_correct_content() -> None:
    """Tests if the decorator correctly writes the function's result to the file."""
    filename = "test_log"

    @log_json_data(filename)
    def my_function(x: int, y: int) -> int:
        return x + y

    expected_result = 5
    actual_result = my_function(2, 3)

    assert actual_result == expected_result
    directory_name = Path(__file__).resolve().parent.parent
    user_settings_file = os.path.join(directory_name, filename + ".json")
    with open(user_settings_file, "r") as f:
        content = f.read()

    expected_log_entry = f"{expected_result}"
    assert expected_log_entry in content


def test_log_to_file_decorator_invalid() -> None:
    """Tests if the decorator correctly writes the function's result to the file."""
    filename = "test_log"

    @log_json_data(filename)
    def my_function() -> NoReturn:
        raise AssertionError

    with pytest.raises(AssertionError):
        assert my_function() == ""
