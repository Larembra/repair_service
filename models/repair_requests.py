from datetime import date
from typing import Any, Optional

from .clients import Client
from .services import Service
from .specialists import Specialist


class RepairRequest:
    def __init__(
        self,
        request_id: int,
        client: Client,
        specialist: Specialist,
        service: Service,
        request_date: date,
    ) -> None:
        self.id = request_id
        self.client = client
        self.specialist = specialist
        self.service = service
        self.request_date = request_date
        self.is_cancelled = False

    def cancel(self) -> None:
        self.is_cancelled = True

    @property
    def status(self) -> str:
        return "отменена" if self.is_cancelled else "новая"

    def __str__(self) -> str:
        return (
            f"{self.request_date.isoformat()} | "
            f"статус: {self.status} | "
            f"клиент: {self.client.name} | "
            f"специалист: {self.specialist.name} | "
            f"услуга: {self.service.name}"
        )

    def to_data(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "client_id": self.client.id,
            "specialist_id": self.specialist.id,
            "service_id": self.service.id,
            "date": self.request_date.isoformat(),
            "is_cancelled": self.is_cancelled,
        }

    @classmethod
    def from_data(
        cls,
        data: dict[str, Any],
        client: Client,
        specialist: Specialist,
        service: Service,
    ) -> "RepairRequest":
        request = cls(
            int(data["id"]),
            client,
            specialist,
            service,
            date.fromisoformat(data["date"]),
        )
        request.is_cancelled = bool(
            data.get("is_cancelled", data.get("status") == "отменена")
        )
        return request


def is_specialist_available(
    requests: list[RepairRequest],
    specialist: Specialist,
    request_date: date,
) -> bool:
    for request in requests:
        if (
            request.specialist.id == specialist.id
            and request.request_date == request_date
            and not request.is_cancelled
        ):
            return False
    return True


def create_request(
    requests: list[RepairRequest],
    client: Client,
    specialist: Specialist,
    service: Service,
    request_date: date,
) -> Optional[RepairRequest]:
    if not is_specialist_available(requests, specialist, request_date):
        return None
    new_id = max((item.id for item in requests), default=0) + 1
    request = RepairRequest(new_id, client, specialist, service, request_date)
    requests.append(request)
    return request


def find_request_by_id(
    requests: list[RepairRequest],
    request_id: int,
) -> Optional[RepairRequest]:
    for request in requests:
        if request.id == request_id:
            return request
    return None


def cancel_request(
    requests: list[RepairRequest],
    request_id: int,
) -> bool:
    request = find_request_by_id(requests, request_id)
    if request is None:
        return False
    request.cancel()
    return True


def filter_requests_by_status(
    requests: list[RepairRequest],
    status: str,
) -> list[RepairRequest]:
    return [request for request in requests if request.status == status]


def get_requests_statistics(
    requests: list[RepairRequest],
) -> dict[str, int]:
    stats: dict[str, int] = {}
    for request in requests:
        stats[request.status] = stats.get(request.status, 0) + 1
    return stats


def get_request_status(is_available: bool, request_date: date) -> str:
    if is_available:
        return f"Заявка от {request_date}: специалист назначен"
    return f"Заявка от {request_date}: специалист не найден"


def show_requests(requests: list[RepairRequest]) -> None:
    if not requests:
        print("Заявок пока нет.")
        return
    print("\n--- Заявки ---")
    for request in requests:
        print(f"[{request.id}] {request}")
