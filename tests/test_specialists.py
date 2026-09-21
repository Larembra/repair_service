"""Тесты функций работы со специалистами."""
from specialists import (
    add_specialist,
    check_specialist_availability,
    filter_specialists_by_rate,
    find_specialists_by_specialization,
    sort_specialists_by_rate,
)


def test_add_specialist() -> None:
    specialists: dict = {}
    sid = add_specialist(specialists, "Петров", "Сантехник", 1500)
    assert sid == 1
    assert len(specialists) == 1


def test_find_by_specialization() -> None:
    specialists: dict = {}
    add_specialist(specialists, "Петров", "Сантехник", 1500)
    add_specialist(specialists, "Сидоров", "Электрик", 1800)
    found = find_specialists_by_specialization(specialists, "сантехник")
    assert len(found) == 1
    assert found[0]["name"] == "Петров"


def test_filter_by_rate() -> None:
    specialists: dict = {}
    add_specialist(specialists, "Петров", "Сантехник", 1500)
    add_specialist(specialists, "Сидоров", "Электрик", 1800)
    cheap = filter_specialists_by_rate(specialists, 1600)
    assert len(cheap) == 1


def test_sort_by_rate() -> None:
    specialists: dict = {}
    add_specialist(specialists, "Сидоров", "Электрик", 1800)
    add_specialist(specialists, "Петров", "Сантехник", 1500)
    ordered = sort_specialists_by_rate(specialists)
    assert ordered[0]["rate"] == 1500
    assert ordered[-1]["rate"] == 1800


def test_check_specialist_availability() -> None:
    assert check_specialist_availability("Сантехник", "Сантехник")
    assert not check_specialist_availability("Электрик", "Сантехник")