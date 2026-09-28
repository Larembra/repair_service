from datetime import date

import pytest

from models import Client, RepairRequest, Service, Specialist
from models.repair_requests import (
    cancel_request,
    create_request,
    filter_requests_by_status,
    find_request_by_id,
    get_request_status,
    get_requests_statistics,
    is_specialist_available,
)

DAY = date(2026, 9, 15)


@pytest.fixture
def client() -> Client:
    return Client(1, "Анна", "123")


@pytest.fixture
def other_client() -> Client:
    return Client(2, "Пётр", "456")


@pytest.fixture
def specialist() -> Specialist:
    return Specialist(1, "Иван", "сантехник", 800.0)


@pytest.fixture
def service() -> Service:
    return Service(1, "Смеситель", "сантехник", 2.0)


def test_request_creation(
    client: Client, specialist: Specialist, service: Service
) -> None:
    request = RepairRequest(1, client, specialist, service, DAY)
    assert request.id == 1
    assert request.client is client
    assert request.specialist is specialist
    assert request.service is service
    assert request.request_date == DAY
    assert not request.is_cancelled


def test_request_cancel_and_status(
    client: Client, specialist: Specialist, service: Service
) -> None:
    request = RepairRequest(1, client, specialist, service, DAY)
    assert request.status == "новая"
    request.cancel()
    assert request.is_cancelled
    assert request.status == "отменена"


def test_request_str(
    client: Client, specialist: Specialist, service: Service
) -> None:
    request = RepairRequest(1, client, specialist, service, DAY)
    text = str(request)
    assert "2026-09-15" in text
    assert "новая" in text
    assert "Анна" in text
    assert "Иван" in text
    assert "Смеситель" in text


def test_create_request_adds_to_collection(
    client: Client, specialist: Specialist, service: Service
) -> None:
    requests: list[RepairRequest] = []
    request = create_request(requests, client, specialist, service, DAY)
    assert request is not None
    assert request.id == 1
    assert request.client is client
    assert requests == [request]


def test_second_active_request_is_rejected(
    client: Client,
    other_client: Client,
    specialist: Specialist,
    service: Service,
) -> None:
    requests: list[RepairRequest] = []
    create_request(requests, client, specialist, service, DAY)
    second = create_request(requests, other_client, specialist, service, DAY)
    assert second is None
    assert len(requests) == 1


def test_cancelled_request_does_not_block(
    client: Client,
    other_client: Client,
    specialist: Specialist,
    service: Service,
) -> None:
    requests: list[RepairRequest] = []
    first = create_request(requests, client, specialist, service, DAY)
    assert first is not None
    first.cancel()
    assert is_specialist_available(requests, specialist, DAY)
    second = create_request(requests, other_client, specialist, service, DAY)
    assert second is not None
    assert len(requests) == 2


def test_other_date_and_other_specialist_are_available(
    client: Client, specialist: Specialist, service: Service
) -> None:
    requests: list[RepairRequest] = []
    create_request(requests, client, specialist, service, DAY)
    assert is_specialist_available(requests, specialist, date(2026, 9, 16))
    other = Specialist(2, "Олег", "сантехник", 700.0)
    assert is_specialist_available(requests, other, DAY)


def test_cancel_request_function(
    client: Client, specialist: Specialist, service: Service
) -> None:
    requests: list[RepairRequest] = []
    request = create_request(requests, client, specialist, service, DAY)
    assert request is not None
    assert cancel_request(requests, request.id)
    assert request.is_cancelled
    assert len(requests) == 1
    assert not cancel_request(requests, 99)


def test_find_request_by_id(
    client: Client, specialist: Specialist, service: Service
) -> None:
    requests: list[RepairRequest] = []
    request = create_request(requests, client, specialist, service, DAY)
    assert find_request_by_id(requests, 1) is request
    assert find_request_by_id(requests, 5) is None


def test_statistics_and_filter(
    client: Client,
    other_client: Client,
    specialist: Specialist,
    service: Service,
) -> None:
    requests: list[RepairRequest] = []
    first = create_request(requests, client, specialist, service, DAY)
    create_request(
        requests, other_client, specialist, service, date(2026, 9, 16)
    )
    assert first is not None
    first.cancel()
    assert get_requests_statistics(requests) == {
        "отменена": 1,
        "новая": 1,
    }
    assert filter_requests_by_status(requests, "отменена") == [first]
    assert len(filter_requests_by_status(requests, "новая")) == 1


def test_get_request_status() -> None:
    assert get_request_status(True, DAY) == (
        "Заявка от 2026-09-15: специалист назначен"
    )
    assert get_request_status(False, DAY) == (
        "Заявка от 2026-09-15: специалист не найден"
    )


def test_request_to_data_and_from_data(
    client: Client, specialist: Specialist, service: Service
) -> None:
    request = RepairRequest(7, client, specialist, service, DAY)
    request.cancel()
    data = request.to_data()
    assert data == {
        "id": 7,
        "client_id": 1,
        "specialist_id": 1,
        "service_id": 1,
        "date": "2026-09-15",
        "is_cancelled": True,
    }
    restored = RepairRequest.from_data(data, client, specialist, service)
    assert restored.id == 7
    assert restored.request_date == DAY
    assert restored.is_cancelled
    assert restored.client is client
