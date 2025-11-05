import json

import pytest

from src.services import investment_bank
from src.services import search_by_name
from src.services import search_by_phonenumber
from src.services import simple_search


def test_simple_search(data_for_search: list[dict]) -> None:
    results = [{"Дата операции": "2021-6-12", "Сумма операции": 345.96, "Категория": "Пере", "описании": "Валерий А."}]
    expected = json.dumps(results, ensure_ascii=False, indent=4)

    assert simple_search("6", data_for_search) == expected


def test_simple_search_with_empty_result() -> None:
    with pytest.raises(AssertionError):
        assert simple_search("6", [{}])


def test_search_by_phonenumber(data_for_search: list[dict]) -> None:
    result = [
        {
            "Дата операции": "2021-05-2",
            "Сумма операции": 100,
            "Категория": "Переводы",
            "описании": "Тинькофф Мобайл +7 995 555-55-55 А.",
        },
        {
            "Дата операции": "2021-05-13",
            "Сумма операции": 134.14,
            "Категория": "Переводы",
            "описании": "Тинькофф Валерий А. Мобайл +7 995 555-55-55 ",
        },
    ]
    expected = json.dumps(result, ensure_ascii=False, indent=4)
    assert search_by_phonenumber(data_for_search) == expected


def test_search_by_name(data_for_search: list[dict]) -> None:
    result = [
        {
            "Дата операции": "2021-05-13",
            "Сумма операции": 134.14,
            "Категория": "Переводы",
            "описании": "Тинькофф Валерий А. Мобайл +7 995 555-55-55 ",
        },
    ]
    expected = json.dumps(result, ensure_ascii=False, indent=4)
    assert search_by_name(data_for_search) == expected


def test_search_by_name_with_empty_result() -> None:
    with pytest.raises(AssertionError):
        assert search_by_name([{}])


@pytest.mark.parametrize(
    "limit, expected",
    [
        (50, 15.86),
        (10, 5.86),
        (100, 65.86),
    ],
)
def test_investment_bank(data_for_search: list[dict], limit: int, expected: float) -> None:
    assert investment_bank("2021-05", data_for_search, limit) == expected


def test_investment_bank_invalid() -> None:
    assert investment_bank("2021-05", [{}], 10) == 0.00
