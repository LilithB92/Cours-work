import json

import pytest

from src.services import simple_search


def test_simple_search(data_for_search: list[dict]) -> None:
    results = [{"Дата операции": "2021-6-12", "Сумма операции": 345.96, "Категория": "Пере", "описании": "Валерий А."}]
    expected = json.dumps(results, ensure_ascii=False, indent=4)

    assert simple_search("6", data_for_search) == expected


def test_simple_search_with_empty_result() -> None:
    with pytest.raises(AssertionError):
        assert simple_search("6", [{}])
