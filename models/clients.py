from typing import Any, Optional


class Client:
    def __init__(self, client_id: int, name: str, phone: str) -> None:
        self.id = client_id
        self.name = name
        self.phone = phone

    def __str__(self) -> str:
        return f"Клиент: {self.name}, телефон: {self.phone}"

    def to_data(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "phone": self.phone}

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Client":
        return cls(int(data["id"]), data["name"], data["phone"])


def add_client(clients: list[Client], name: str, phone: str) -> Client:
    new_id = max((client.id for client in clients), default=0) + 1
    client = Client(new_id, name, phone)
    clients.append(client)
    return client


def find_client(clients: list[Client], query: str) -> list[Client]:
    query_lower = query.lower()
    return [client for client in clients if query_lower in client.name.lower()]


def find_client_by_id(
    clients: list[Client],
    client_id: int,
) -> Optional[Client]:
    for client in clients:
        if client.id == client_id:
            return client
    return None


def show_clients(clients: list[Client]) -> None:
    if not clients:
        print("Список клиентов пуст.")
        return
    print("\n--- Клиенты ---")
    for client in clients:
        print(f"[{client.id}] {client}")
