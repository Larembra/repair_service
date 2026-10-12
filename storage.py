import json
import os
from pathlib import Path
from typing import Any, Callable, TypeVar

from models import Client, RepairRequest, Service, Specialist
from models.clients import find_client_by_id
from models.services import find_service_by_id
from models.specialists import find_specialist_by_id

DATA_DIR = Path(__file__).resolve().parent / "data"
CLIENTS_FILE = "clients.json"
SPECIALISTS_FILE = "specialists.json"
SERVICES_FILE = "services.json"
REQUESTS_FILE = "requests.json"

T = TypeVar("T")


def _data_path(filename: str) -> Path:
    return Path(DATA_DIR) / filename


def _ensure_data_dir() -> None:
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)


def load_data(filename: str, default: Any) -> Any:
    path = _data_path(filename)
    if not os.path.exists(path):
        return default
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Предупреждение: не удалось прочитать {filename}: {error}")
        return default


def save_data(filename: str, data: Any) -> None:
    _ensure_data_dir()
    path = _data_path(filename)
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Ошибка сохранения {filename}: {error}")


def _to_records(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        return [{"id": int(key), **value} for key, value in raw.items()]
    if isinstance(raw, list):
        return raw
    return []


def _build_objects(
    records: list[dict[str, Any]],
    factory: Callable[[dict[str, Any]], T],
    filename: str,
) -> list[T]:
    objects: list[T] = []
    for record in records:
        try:
            objects.append(factory(record))
        except (KeyError, TypeError, ValueError) as error:
            print(f"Предупреждение: запись в {filename} пропущена: {error}")
    return objects


def load_clients() -> list[Client]:
    records = _to_records(load_data(CLIENTS_FILE, []))
    return _build_objects(records, Client.from_data, CLIENTS_FILE)


def save_clients(clients: list[Client]) -> None:
    save_data(CLIENTS_FILE, [client.to_data() for client in clients])


def load_specialists() -> list[Specialist]:
    records = _to_records(load_data(SPECIALISTS_FILE, []))
    return _build_objects(records, Specialist.from_data, SPECIALISTS_FILE)


def save_specialists(specialists: list[Specialist]) -> None:
    save_data(SPECIALISTS_FILE, [item.to_data() for item in specialists])


def load_services() -> list[Service]:
    records = _to_records(load_data(SERVICES_FILE, []))
    return _build_objects(records, Service.from_data, SERVICES_FILE)


def save_services(services: list[Service]) -> None:
    save_data(SERVICES_FILE, [service.to_data() for service in services])


def load_requests(
    clients: list[Client],
    specialists: list[Specialist],
    services: list[Service],
) -> list[RepairRequest]:
    records = _to_records(load_data(REQUESTS_FILE, []))
    requests: list[RepairRequest] = []
    for record in records:
        try:
            client = find_client_by_id(clients, int(record["client_id"]))
            specialist = find_specialist_by_id(
                specialists, int(record["specialist_id"])
            )
            service = find_service_by_id(services, int(record["service_id"]))
            if client is None or specialist is None or service is None:
                print(
                    f"Предупреждение: заявка {record.get('id')} пропущена: "
                    "связанный объект не найден."
                )
                continue
            requests.append(
                RepairRequest.from_data(record, client, specialist, service)
            )
        except (KeyError, TypeError, ValueError) as error:
            print(f"Предупреждение: заявка пропущена: {error}")
    return requests


def save_requests(requests: list[RepairRequest]) -> None:
    save_data(REQUESTS_FILE, [request.to_data() for request in requests])
