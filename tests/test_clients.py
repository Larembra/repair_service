from models import Client
from models.clients import add_client, find_client, find_client_by_id


def test_client_creation() -> None:
    client = Client(1, "Анна", "+7 900 000-00-00")
    assert client.id == 1
    assert client.name == "Анна"
    assert client.phone == "+7 900 000-00-00"


def test_client_str() -> None:
    client = Client(1, "Анна", "123")
    assert str(client) == "Клиент: Анна, телефон: 123"


def test_client_from_data_and_to_data() -> None:
    data = {"id": 3, "name": "Пётр", "phone": "555"}
    client = Client.from_data(data)
    assert client.id == 3
    assert client.to_data() == data


def test_add_client_returns_object_and_increments_id() -> None:
    clients: list[Client] = []
    first = add_client(clients, "Анна", "1")
    second = add_client(clients, "Пётр", "2")
    assert first.id == 1
    assert second.id == 2
    assert clients == [first, second]


def test_find_client_by_name() -> None:
    clients = [Client(1, "Анна", "1"), Client(2, "Антон", "2")]
    assert find_client(clients, "ан") == clients
    assert find_client(clients, "анн") == [clients[0]]
    assert find_client(clients, "xyz") == []


def test_find_client_by_id() -> None:
    clients = [Client(1, "Анна", "1")]
    assert find_client_by_id(clients, 1) is clients[0]
    assert find_client_by_id(clients, 5) is None
