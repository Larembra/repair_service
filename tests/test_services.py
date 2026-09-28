import pytest

from models import Service
from models.services import (
    add_service,
    find_service_by_id,
    find_services_by_name,
)


def test_service_creation() -> None:
    service = Service(1, "Замена смесителя", "сантехник", 2.0)
    assert service.id == 1
    assert service.name == "Замена смесителя"
    assert service.required_specialization == "сантехник"
    assert service.hours == 2.0


def test_service_str() -> None:
    service = Service(1, "Замена смесителя", "сантехник", 2.0)
    assert str(service) == (
        "Услуга: Замена смесителя, ориентировочное время: 2.0 ч"
    )


def test_calculate_cost() -> None:
    service = Service(1, "Проводка", "электрик", 2.5)
    assert service.calculate_cost(1000.0) == 2500.0
    assert service.calculate_cost(333.333) == 833.33


def test_validate_hours() -> None:
    assert Service.validate_hours(1.5)
    assert not Service.validate_hours(0)
    assert not Service.validate_hours(-1)


def test_add_service() -> None:
    services: list[Service] = []
    service = add_service(services, "Покраска", "маляр", 4.0)
    assert service.id == 1
    assert services == [service]


def test_add_service_invalid_hours() -> None:
    services: list[Service] = []
    with pytest.raises(ValueError):
        add_service(services, "Покраска", "маляр", 0)
    assert services == []


def test_find_services_by_name() -> None:
    services = [
        Service(1, "Замена смесителя", "сантехник", 2.0),
        Service(2, "Замена розетки", "электрик", 1.0),
    ]
    assert find_services_by_name(services, "замена") == services
    assert find_services_by_name(services, "розетк") == [services[1]]


def test_find_service_by_id() -> None:
    services = [Service(1, "Покраска", "маляр", 4.0)]
    assert find_service_by_id(services, 1) is services[0]
    assert find_service_by_id(services, 2) is None


def test_service_from_data_and_to_data() -> None:
    data = {
        "id": 2,
        "name": "Покраска",
        "required_specialization": "маляр",
        "hours": 4.0,
    }
    assert Service.from_data(data).to_data() == data
