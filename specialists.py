"""Функции для работы со специалистами."""
from typing import Any


def add_specialist(
    specialists: dict[int, dict[str, Any]],
    name: str,
    specialization: str,
    rate: float,
) -> int:
    """Добавить специалиста и вернуть его идентификатор."""
    new_id = max(specialists.keys(), default=0) + 1
    specialists[new_id] = {
        "name": name,
        "specialization": specialization,
        "rate": rate,
    }
    return new_id


def find_specialists_by_specialization(
    specialists: dict[int, dict[str, Any]],
    specialization: str,
) -> list[dict[str, Any]]:
    """Найти специалистов по специализации (без учёта регистра)."""
    target = specialization.strip().lower()
    return [
        {"id": sid, **data}
        for sid, data in specialists.items()
        if data["specialization"].lower() == target
    ]


def filter_specialists_by_rate(
    specialists: dict[int, dict[str, Any]],
    max_rate: float,
) -> list[dict[str, Any]]:
    """Отобрать специалистов со ставкой не выше max_rate."""
    return [
        {"id": sid, **data}
        for sid, data in specialists.items()
        if data["rate"] <= max_rate
    ]


def sort_specialists_by_rate(
    specialists: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Отсортировать специалистов по ставке (lambda как ключ сортировки)."""
    return sorted(
        ({"id": sid, **data} for sid, data in specialists.items()),
        key=lambda item: item["rate"],
    )


def check_specialist_availability(
    specialization: str,
    required_specialization: str,
) -> bool:
    """Проверка соответствия специалиста услуге (функция из ПР1)."""
    return specialization == required_specialization


def get_specialist_info(specialist: dict[str, Any]) -> str:
    """Вернуть строку с информацией о специалисте (из ПР1)."""
    return (
        f"Специалист: {specialist['name']}, "
        f"специализация: {specialist['specialization']}, "
        f"ставка: {specialist['rate']} руб/час"
    )