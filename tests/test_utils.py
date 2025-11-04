from freezegun import freeze_time

import src.utils
from src.utils import get_month_period


def test_get_month_period() -> None:
    assert get_month_period("2021-12-30 08:16:00") == ["01.12.2021 08:16:00", "30.12.2021 08:16:00"]


@freeze_time("2025-01-01 12:10:20")
def test_get_greeting_afternoon() -> None:
    assert src.utils.get_greeting() == "Добрый день"


@freeze_time("2025-01-01 09:25:12")
def test_get_greeting_morning() -> None:
    assert src.utils.get_greeting() == "Доброе утро"


@freeze_time("2025-01-01 17:35:12")
def test_get_greeting_evening() -> None:
    assert src.utils.get_greeting() == "Добрый вечер"


@freeze_time("2025-01-01 23:35:12")
def test_get_greeting_night() -> None:
    assert src.utils.get_greeting() == "Доброй ночи"
