"""Тесты функций работы с услугами."""
from services import add_service, calculate_cost, find_services_by_name


def test_add_service() -> None:
    services: dict = {}
    sid = add_service(services, "Протечка", "Сантехник", 2.0)
    assert sid == 1
    assert services[1]["hours"] == 2.0


def test_calculate_cost() -> None:
    assert calculate_cost(1500, 2.0) == 3000.0
    assert calculate_cost(1800, 1.5) == 2700.0


def test_find_services_by_name() -> None:
    services: dict = {}
    add_service(services, "Замена крана", "Сантехник", 1.5)
    add_service(services, "Замена розетки", "Электрик", 1.0)
    found = find_services_by_name(services, "крана")
    assert len(found) == 1