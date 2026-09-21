"""Сервис поиска специалистов по ремонту — точка запуска."""
from typing import Any

from clients import add_client
from repair_requests import (
    cancel_request,
    create_request,
    get_requests_statistics,
    get_request_status,
    is_specialist_available,
)
from services import (
    add_service,
    calculate_cost,
    get_service_info,
)
from specialists import (
    add_specialist,
    check_specialist_availability,
    get_specialist_info,
)
from storage import load_data, save_data
from utils import input_date, input_float, input_int, input_non_empty


def show_specialists(specialists: dict[int, dict[str, Any]]) -> None:
    """Вывести список специалистов."""
    if not specialists:
        print("Список специалистов пуст.")
        return
    print("\n--- Специалисты ---")
    for sid, data in specialists.items():
        print(f"[{sid}] {get_specialist_info(data)}")


def show_services(services: dict[int, dict[str, Any]]) -> None:
    """Вывести каталог услуг."""
    if not services:
        print("Каталог услуг пуст.")
        return
    print("\n--- Услуги ---")
    for sid, data in services.items():
        print(f"[{sid}] {get_service_info(data)}")


def show_requests(
    requests: list[dict[str, Any]],
    specialists: dict[int, dict[str, Any]],
    services: dict[int, dict[str, Any]],
    clients: dict[int, dict[str, Any]],
) -> None:
    """Вывести список заявок с расшифровкой идентификаторов."""
    if not requests:
        print("Заявок пока нет.")
        return
    print("\n--- Заявки ---")
    for request in requests:
        specialist = specialists.get(request["specialist_id"], {})
        service = services.get(request["service_id"], {})
        client = clients.get(request["client_id"], {})
        print(
            f"[{request['id']}] {request['date']} | "
            f"статус: {request['status']} | "
            f"клиент: {client.get('name', '?')} | "
            f"специалист: {specialist.get('name', '?')} | "
            f"услуга: {service.get('name', '?')}"
        )


def handle_booking(
    clients: dict[int, dict[str, Any]],
    specialists: dict[int, dict[str, Any]],
    services: dict[int, dict[str, Any]],
    requests: list[dict[str, Any]],
) -> None:
    """Сценарий создания новой заявки."""
    if not clients or not specialists or not services:
        print("Сначала добавьте клиента, специалиста и услугу.")
        return

    show_specialists(specialists)
    specialist_id = input_int("ID специалиста: ")
    if specialist_id not in specialists:
        print("Специалист не найден.")
        return

    show_services(services)
    service_id = input_int("ID услуги: ")
    if service_id not in services:
        print("Услуга не найдена.")
        return

    client_id = input_int("ID клиента: ")
    if client_id not in clients:
        print("Клиент не найден.")
        return

    request_date = input_date("Дата заявки (ДД.ММ.ГГГГ): ")

    specialist = specialists[specialist_id]
    service = services[service_id]

    if not check_specialist_availability(
        specialist["specialization"], service["required_specialization"]
    ):
        print("Специалист не подходит под услугу.")
        return

    if not is_specialist_available(requests, specialist_id, request_date):
        print("Специалист уже занят на эту дату.")
        return

    request = create_request(
        requests, client_id, specialist_id, service_id, request_date
    )
    cost = calculate_cost(specialist["rate"], service["hours"])
    print(get_request_status(True, request_date))
    print(f"Предварительная стоимость: {cost} руб. (заявка #{request['id']})")


def main() -> None:
    """Точка запуска: цикл меню и вызов функций проекта."""
    clients = load_data("clients.json", {})
    specialists = load_data("specialists.json", {})
    services = load_data("services.json", {})
    requests = load_data("requests.json", [])

    # Приведение ключей словарей к int после JSON
    clients = {int(k): v for k, v in clients.items()}
    specialists = {int(k): v for k, v in specialists.items()}
    services = {int(k): v for k, v in services.items()}

    menu = (
        "\n=== Сервис поиска специалистов по ремонту ===\n"
        "1. Показать специалистов\n"
        "2. Показать услуги\n"
        "3. Показать заявки\n"
        "4. Добавить клиента\n"
        "5. Добавить специалиста\n"
        "6. Добавить услугу\n"
        "7. Оформить заявку\n"
        "8. Отменить заявку\n"
        "9. Статистика заявок\n"
        "0. Выход\n"
    )

    while True:
        print(menu)
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                show_specialists(specialists)
            elif choice == "2":
                show_services(services)
            elif choice == "3":
                show_requests(requests, specialists, services, clients)
            elif choice == "4":
                name = input_non_empty("Имя клиента: ")
                phone = input_non_empty("Телефон: ")
                cid = add_client(clients, name, phone)
                print(f"Клиент добавлен, ID = {cid}.")
            elif choice == "5":
                name = input_non_empty("Имя специалиста: ")
                spec = input_non_empty("Специализация: ")
                rate = input_float("Ставка (руб/час): ")
                sid = add_specialist(specialists, name, spec, rate)
                print(f"Специалист добавлен, ID = {sid}.")
            elif choice == "6":
                name = input_non_empty("Название услуги: ")
                req = input_non_empty("Требуемая специализация: ")
                hours = input_float("Ориентировочное время (ч): ")
                sid = add_service(services, name, req, hours)
                print(f"Услуга добавлена, ID = {sid}.")
            elif choice == "7":
                handle_booking(clients, specialists, services, requests)
            elif choice == "8":
                show_requests(requests, specialists, services, clients)
                rid = input_int("ID заявки для отмены: ")
                if cancel_request(requests, rid):
                    print("Заявка отменена.")
                else:
                    print("Заявка не найдена.")
            elif choice == "9":
                stats = get_requests_statistics(requests)
                print("\n--- Статистика заявок ---")
                for status, count in stats.items():
                    print(f"{status}: {count}")
            elif choice == "0":
                save_data("clients.json", clients)
                save_data("specialists.json", specialists)
                save_data("services.json", services)
                save_data("requests.json", requests)
                print("Данные сохранены. До свидания!")
                break
            else:
                print("Неизвестная команда.")
        except (KeyError, ValueError, TypeError) as error:
            print(f"Ошибка выполнения: {error}")


if __name__ == "__main__":
    main()
