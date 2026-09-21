"""Функции для работы с заявками."""
from datetime import date
from typing import Any


def create_request(
    requests: list[dict[str, Any]],
    client_id: int,
    specialist_id: int,
    service_id: int,
    request_date: date,
) -> dict[str, Any]:
    """Создать новую заявку и добавить её в список."""
    new_id = max((r["id"] for r in requests), default=0) + 1
    request = {
        "id": new_id,
        "client_id": client_id,
        "specialist_id": specialist_id,
        "service_id": service_id,
        "date": request_date.isoformat(),
        "status": "новая",
    }
    requests.append(request)
    return request


def cancel_request(
    requests: list[dict[str, Any]],
    request_id: int,
) -> bool:
    """Отменить заявку по идентификатору."""
    for request in requests:
        if request["id"] == request_id:
            request["status"] = "отменена"
            return True
    return False


def is_specialist_available(
    requests: list[dict[str, Any]],
    specialist_id: int,
    request_date: date,
) -> bool:
    """Проверить, свободен ли специалист на указанную дату."""
    target = request_date.isoformat()
    for request in requests:
        if (
            request["specialist_id"] == specialist_id
            and request["date"] == target
            and request["status"] != "отменена"
        ):
            return False
    return True


def filter_requests_by_status(
    requests: list[dict[str, Any]],
    status: str,
) -> list[dict[str, Any]]:
    """Отобрать заявки по статусу (генератор внутри)."""
    return [r for r in requests if r["status"] == status]


def get_requests_statistics(
    requests: list[dict[str, Any]],
) -> dict[str, int]:
    """Собрать статистику по статусам заявок."""
    stats: dict[str, int] = {}
    for request in requests:
        status = request["status"]
        stats[status] = stats.get(status, 0) + 1
    return stats


def get_request_status(
    is_available: bool,
    request_date: date,
) -> str:
    """Текстовый статус заявки (функция из ПР1)."""
    if is_available:
        return f"Заявка от {request_date}: специалист назначен"
    return f"Заявка от {request_date}: специалист не найден"