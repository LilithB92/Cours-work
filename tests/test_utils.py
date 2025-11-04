from src.utils import get_month_period


def test_get_month_period() -> None:
    assert get_month_period("2021-12-30 08:16:00") == ["01.12.2021 08:16:00", "30.12.2021 08:16:00"]
