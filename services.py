"""Функции для работы с услугами."""
from typing import Any


def add_service(
    services: dict[int, dict[str, Any]],
    name: str,
    required_specialization: str,
    hours: float,
) -> int:
    """Добавить услугу и вернуть её идентификатор."""
    new_id = max(services.keys(), default=0) + 1
    services[new_id] = {
        "name": name,
        "required_specialization": required_specialization,
        "hours": hours,
    }
    return new_id


def find_services_by_name(
    services: dict[int, dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    """Найти услуги по подстроке названия."""
    query_lower = query.lower()
    return [
        {"id": sid, **data}
        for sid, data in services.items()
        if query_lower in data["name"].lower()
    ]


def calculate_cost(rate: float, hours: float) -> float:
    """Считать предварительную стоимость заявки (из ПР1)."""
    return round(rate * hours, 2)


def get_service_info(service: dict[str, Any]) -> str:
    """Вернуть строку с информацией об услуге (из ПР1)."""
    return (
        f"Услуга: {service['name']}, "
        f"ориентировочное время: {service['hours']} ч"
    )
