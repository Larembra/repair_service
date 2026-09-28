from datetime import date
from pathlib import Path

import pytest

import storage
from models import Client, Service, Specialist
from models.repair_requests import create_request
from storage import (
    load_clients,
    load_data,
    load_requests,
    load_services,
    load_specialists,
    save_clients,
    save_data,
    save_requests,
    save_services,
    save_specialists,
)


@pytest.fixture(autouse=True)
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(storage, "DATA_DIR", str(tmp_path))


def test_load_data_missing_file_returns_default() -> None:
    assert load_data("missing.json", []) == []


def test_clients_roundtrip() -> None:
    save_clients([Client(1, "Анна", "123")])
    loaded = load_clients()
    assert len(loaded) == 1
    assert loaded[0].id == 1
    assert loaded[0].name == "Анна"
    assert loaded[0].phone == "123"


def test_specialists_roundtrip() -> None:
    save_specialists([Specialist(1, "Иван", "сантехник", 800.0)])
    loaded = load_specialists()
    assert loaded[0].specialization == "сантехник"
    assert loaded[0].rate == 800.0


def test_services_roundtrip() -> None:
    save_services([Service(1, "Смеситель", "сантехник", 2.0)])
    loaded = load_services()
    assert loaded[0].name == "Смеситель"
    assert loaded[0].hours == 2.0


def test_requests_roundtrip_restores_links() -> None:
    clients = [Client(1, "Анна", "123")]
    specialists = [Specialist(1, "Иван", "сантехник", 800.0)]
    services = [Service(1, "Смеситель", "сантехник", 2.0)]
    request = create_request(
        [], clients[0], specialists[0], services[0], date(2026, 9, 15)
    )
    assert request is not None
    request.cancel()
    save_requests([request])

    loaded = load_requests(clients, specialists, services)
    assert len(loaded) == 1
    assert loaded[0].client is clients[0]
    assert loaded[0].specialist is specialists[0]
    assert loaded[0].service is services[0]
    assert loaded[0].request_date == date(2026, 9, 15)
    assert loaded[0].is_cancelled


def test_request_with_missing_client_is_skipped() -> None:
    specialists = [Specialist(1, "Иван", "сантехник", 800.0)]
    services = [Service(1, "Смеситель", "сантехник", 2.0)]
    save_data(
        "requests.json",
        [
            {
                "id": 1,
                "client_id": 99,
                "specialist_id": 1,
                "service_id": 1,
                "date": "2026-09-15",
                "is_cancelled": False,
            }
        ],
    )
    assert load_requests([], specialists, services) == []


def test_legacy_pr2_format_is_supported() -> None:
    save_data("clients.json", {"1": {"name": "Анна", "phone": "123"}})
    clients = load_clients()
    assert clients[0].id == 1
    assert clients[0].name == "Анна"

    specialists = [Specialist(1, "Иван", "сантехник", 800.0)]
    services = [Service(1, "Смеситель", "сантехник", 2.0)]
    save_data(
        "requests.json",
        [
            {
                "id": 1,
                "client_id": 1,
                "specialist_id": 1,
                "service_id": 1,
                "date": "2026-09-15",
                "status": "отменена",
            }
        ],
    )
    loaded = load_requests(clients, specialists, services)
    assert loaded[0].is_cancelled
