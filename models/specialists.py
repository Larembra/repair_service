from typing import Any, Optional

from .services import Service


class Specialist:
    def __init__(
        self,
        specialist_id: int,
        name: str,
        specialization: str,
        rate: float,
    ) -> None:
        self.id = specialist_id
        self.name = name
        self.specialization = specialization
        self.rate = rate

    @staticmethod
    def validate_rate(rate: float) -> bool:
        return rate > 0

    def is_suitable_for(self, service: Service) -> bool:
        return self.specialization == service.required_specialization

    def __str__(self) -> str:
        return (
            f"Специалист: {self.name}, "
            f"специализация: {self.specialization}, "
            f"ставка: {self.rate} руб/час"
        )

    def to_data(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "rate": self.rate,
        }

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Specialist":
        return cls(
            int(data["id"]),
            data["name"],
            data["specialization"],
            float(data["rate"]),
        )


def add_specialist(
    specialists: list[Specialist],
    name: str,
    specialization: str,
    rate: float,
) -> Specialist:
    if not Specialist.validate_rate(rate):
        raise ValueError("Ставка должна быть больше нуля.")
    new_id = max((item.id for item in specialists), default=0) + 1
    specialist = Specialist(new_id, name, specialization, rate)
    specialists.append(specialist)
    return specialist


def find_specialist_by_id(
    specialists: list[Specialist],
    specialist_id: int,
) -> Optional[Specialist]:
    for specialist in specialists:
        if specialist.id == specialist_id:
            return specialist
    return None


def find_specialists_by_specialization(
    specialists: list[Specialist],
    specialization: str,
) -> list[Specialist]:
    target = specialization.strip().lower()
    return [
        item for item in specialists if item.specialization.lower() == target
    ]


def filter_specialists_by_rate(
    specialists: list[Specialist],
    max_rate: float,
) -> list[Specialist]:
    return [item for item in specialists if item.rate <= max_rate]


def sort_specialists_by_rate(
    specialists: list[Specialist],
) -> list[Specialist]:
    return sorted(specialists, key=lambda item: item.rate)


def check_specialist_availability(
    specialist: Specialist,
    service: Service,
) -> bool:
    return specialist.is_suitable_for(service)


def show_specialists(specialists: list[Specialist]) -> None:
    if not specialists:
        print("Список специалистов пуст.")
        return
    print("\n--- Специалисты ---")
    for specialist in specialists:
        print(f"[{specialist.id}] {specialist}")
