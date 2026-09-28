import pytest

from models import Service, Specialist
from models.specialists import (
    add_specialist,
    check_specialist_availability,
    filter_specialists_by_rate,
    find_specialist_by_id,
    find_specialists_by_specialization,
    sort_specialists_by_rate,
)


@pytest.fixture
def specialists() -> list[Specialist]:
    return [
        Specialist(1, "Иван", "сантехник", 800.0),
        Specialist(2, "Пётр", "электрик", 1200.0),
        Specialist(3, "Олег", "Сантехник", 600.0),
    ]


def test_specialist_creation() -> None:
    specialist = Specialist(1, "Иван", "сантехник", 800.0)
    assert specialist.id == 1
    assert specialist.name == "Иван"
    assert specialist.specialization == "сантехник"
    assert specialist.rate == 800.0


def test_specialist_str() -> None:
    specialist = Specialist(1, "Иван", "сантехник", 800.0)
    assert str(specialist) == (
        "Специалист: Иван, специализация: сантехник, ставка: 800.0 руб/час"
    )


def test_is_suitable_for() -> None:
    specialist = Specialist(1, "Иван", "сантехник", 800.0)
    plumbing = Service(1, "Смеситель", "сантехник", 2.0)
    wiring = Service(2, "Проводка", "электрик", 3.0)
    assert specialist.is_suitable_for(plumbing)
    assert not specialist.is_suitable_for(wiring)
    assert check_specialist_availability(specialist, plumbing)
    assert not check_specialist_availability(specialist, wiring)


def test_validate_rate() -> None:
    assert Specialist.validate_rate(100)
    assert not Specialist.validate_rate(0)
    assert not Specialist.validate_rate(-5)


def test_add_specialist() -> None:
    items: list[Specialist] = []
    specialist = add_specialist(items, "Иван", "сантехник", 800.0)
    assert specialist.id == 1
    assert items == [specialist]


def test_add_specialist_invalid_rate() -> None:
    items: list[Specialist] = []
    with pytest.raises(ValueError):
        add_specialist(items, "Иван", "сантехник", -1)
    assert items == []


def test_find_by_specialization(specialists: list[Specialist]) -> None:
    result = find_specialists_by_specialization(specialists, " САНТЕХНИК ")
    assert result == [specialists[0], specialists[2]]


def test_filter_by_rate(specialists: list[Specialist]) -> None:
    result = filter_specialists_by_rate(specialists, 800.0)
    assert result == [specialists[0], specialists[2]]


def test_sort_by_rate(specialists: list[Specialist]) -> None:
    result = sort_specialists_by_rate(specialists)
    assert [item.id for item in result] == [3, 1, 2]
    assert [item.id for item in specialists] == [1, 2, 3]


def test_find_specialist_by_id(specialists: list[Specialist]) -> None:
    assert find_specialist_by_id(specialists, 2) is specialists[1]
    assert find_specialist_by_id(specialists, 9) is None


def test_specialist_from_data_and_to_data() -> None:
    data = {
        "id": 4,
        "name": "Олег",
        "specialization": "маляр",
        "rate": 700.0,
    }
    assert Specialist.from_data(data).to_data() == data
