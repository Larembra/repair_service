from typing import Any, Optional


class Service:
    def __init__(
        self,
        service_id: int,
        name: str,
        required_specialization: str,
        hours: float,
    ) -> None:
        self.id = service_id
        self.name = name
        self.required_specialization = required_specialization
        self.hours = hours

    @staticmethod
    def validate_hours(hours: float) -> bool:
        return hours > 0

    def calculate_cost(self, rate: float) -> float:
        return round(rate * self.hours, 2)

    def __str__(self) -> str:
        return f"Услуга: {self.name}, ориентировочное время: {self.hours} ч"

    def to_data(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "required_specialization": self.required_specialization,
            "hours": self.hours,
        }

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Service":
        return cls(
            int(data["id"]),
            data["name"],
            data["required_specialization"],
            float(data["hours"]),
        )


def add_service(
    services: list[Service],
    name: str,
    required_specialization: str,
    hours: float,
) -> Service:
    if not Service.validate_hours(hours):
        raise ValueError("Время выполнения должно быть больше нуля.")
    new_id = max((service.id for service in services), default=0) + 1
    service = Service(new_id, name, required_specialization, hours)
    services.append(service)
    return service


def find_services_by_name(
    services: list[Service],
    query: str,
) -> list[Service]:
    query_lower = query.lower()
    return [
        service for service in services if query_lower in service.name.lower()
    ]


def find_service_by_id(
    services: list[Service],
    service_id: int,
) -> Optional[Service]:
    for service in services:
        if service.id == service_id:
            return service
    return None


def show_services(services: list[Service]) -> None:
    if not services:
        print("Каталог услуг пуст.")
        return
    print("\n--- Услуги ---")
    for service in services:
        print(f"[{service.id}] {service}")
