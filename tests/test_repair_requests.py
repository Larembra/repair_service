"""Тесты функций работы с заявками."""
from datetime import date

from repair_requests import (
    cancel_request,
    create_request,
    get_requests_statistics,
    is_specialist_available,
)


def test_create_request() -> None:
    requests: list = []
    request = create_request(requests, 1, 1, 1, date(2026, 9, 15))
    assert request["id"] == 1
    assert len(requests) == 1


def test_specialist_available() -> None:
    requests: list = []
    assert is_specialist_available(requests, 1, date(2026, 9, 15))


def test_duplicate_booking_forbidden() -> None:
    requests: list = []
    create_request(requests, 1, 1, 1, date(2026, 9, 15))
    assert not is_specialist_available(requests, 1, date(2026, 9, 15))


def test_cancel_request() -> None:
    requests: list = []
    create_request(requests, 1, 1, 1, date(2026, 9, 15))
    assert cancel_request(requests, 1)
    assert requests[0]["status"] == "отменена"


def test_statistics() -> None:
    requests: list = []
    create_request(requests, 1, 1, 1, date(2026, 9, 15))
    create_request(requests, 1, 2, 2, date(2026, 9, 16))
    stats = get_requests_statistics(requests)
    assert stats.get("новая") == 2