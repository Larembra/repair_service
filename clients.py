"""Функции для работы с клиентами."""
from typing import Any


def add_client(
    clients: dict[int, dict[str, Any]],
    name: str,
    phone: str,
) -> int:
    """Добавить клиента в словарь clients и вернуть его идентификатор."""
    new_id = max(clients.keys(), default=0) + 1
    clients[new_id] = {"name": name, "phone": phone}
    return new_id


def find_client_by_name(
    clients: dict[int, dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    """Найти клиентов по подстроке имени."""
    query_lower = query.lower()
    return [
        {"id": cid, **data}
        for cid, data in clients.items()
        if query_lower in data["name"].lower()
    ]


def get_client_info(client: dict[str, Any]) -> str:
    """Вернуть строку с информацией о клиенте (преемственность из ПР1)."""
    return f"Клиент: {client['name']}, телефон: {client['phone']}"
