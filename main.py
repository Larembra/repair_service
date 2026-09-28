from models import Client, RepairRequest, Service, Specialist
from models.clients import add_client, find_client_by_id
from models.repair_requests import (
    cancel_request,
    create_request,
    get_request_status,
    get_requests_statistics,
    show_requests,
)
from models.services import add_service, find_service_by_id, show_services
from models.specialists import (
    add_specialist,
    check_specialist_availability,
    find_specialist_by_id,
    show_specialists,
)
from storage import (
    load_clients,
    load_requests,
    load_services,
    load_specialists,
    save_clients,
    save_requests,
    save_services,
    save_specialists,
)
from utils import input_date, input_float, input_int, input_non_empty


def create_new_request(
    requests: list[RepairRequest],
    clients: list[Client],
    specialists: list[Specialist],
    services: list[Service],
) -> None:
    if not clients or not specialists or not services:
        print("Сначала добавьте клиента, специалиста и услугу.")
        return

    show_specialists(specialists)
    specialist_id = input_int("ID специалиста: ")
    specialist = find_specialist_by_id(specialists, specialist_id)
    if specialist is None:
        print("Специалист не найден.")
        return

    show_services(services)
    service_id = input_int("ID услуги: ")
    service = find_service_by_id(services, service_id)
    if service is None:
        print("Услуга не найдена.")
        return

    client_id = input_int("ID клиента: ")
    client = find_client_by_id(clients, client_id)
    if client is None:
        print("Клиент не найден.")
        return

    request_date = input_date("Дата заявки (ДД.ММ.ГГГГ): ")

    if not check_specialist_availability(specialist, service):
        print("Специалист не подходит под услугу.")
        return

    request = create_request(
        requests, client, specialist, service, request_date
    )
    if request is None:
        print("Специалист уже занят на эту дату.")
        return

    cost = service.calculate_cost(specialist.rate)
    print(get_request_status(True, request_date))
    print(f"Предварительная стоимость: {cost} руб. (заявка #{request.id})")


def main() -> None:
    clients = load_clients()
    specialists = load_specialists()
    services = load_services()
    requests = load_requests(clients, specialists, services)

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
                show_requests(requests)
            elif choice == "4":
                name = input_non_empty("Имя клиента: ")
                phone = input_non_empty("Телефон: ")
                client = add_client(clients, name, phone)
                print(f"Клиент добавлен, ID = {client.id}.")
            elif choice == "5":
                name = input_non_empty("Имя специалиста: ")
                specialization = input_non_empty("Специализация: ")
                rate = input_float("Ставка (руб/час): ")
                specialist = add_specialist(
                    specialists, name, specialization, rate
                )
                print(f"Специалист добавлен, ID = {specialist.id}.")
            elif choice == "6":
                name = input_non_empty("Название услуги: ")
                required = input_non_empty("Требуемая специализация: ")
                hours = input_float("Ориентировочное время (ч): ")
                service = add_service(services, name, required, hours)
                print(f"Услуга добавлена, ID = {service.id}.")
            elif choice == "7":
                create_new_request(requests, clients, specialists, services)
            elif choice == "8":
                show_requests(requests)
                request_id = input_int("ID заявки для отмены: ")
                if cancel_request(requests, request_id):
                    print("Заявка отменена.")
                else:
                    print("Заявка не найдена.")
            elif choice == "9":
                stats = get_requests_statistics(requests)
                print("\n--- Статистика заявок ---")
                for status, count in stats.items():
                    print(f"{status}: {count}")
            elif choice == "0":
                save_clients(clients)
                save_specialists(specialists)
                save_services(services)
                save_requests(requests)
                print("Данные сохранены. До свидания!")
                break
            else:
                print("Неизвестная команда.")
        except (KeyError, ValueError, TypeError) as error:
            print(f"Ошибка выполнения: {error}")


if __name__ == "__main__":
    main()
