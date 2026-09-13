from datetime import date



client_name = "Иванов Иван"
client_phone = "+7-900-123-45-67"

specialist_name = "Петров Пётр"
specialist_specialization = "Сантехник"
specialist_rate = 1500  # руб/час

service_name = "Устранение протечки крана"
service_hours = 2.0

request_date = date(2026, 9, 15)
request_status = "новая"




def get_client_info(name, phone):
    """Возвращает строку с информацией о клиенте."""
    return f"Клиент: {name}, телефон: {phone}"


def get_specialist_info(name, specialization, rate):
    """Возвращает строку с информацией о специалисте."""
    return (f"Специалист: {name}, специализация: {specialization}, "
            f"ставка: {rate} руб/час")


def get_service_info(name, hours):
    """Возвращает строку с информацией об услуге."""
    return f"Услуга: {name}, ориентировочное время: {hours} ч"


def calculate_cost(rate, hours):
    """Считает предварительную стоимость заявки."""
    cost = rate * hours
    return round(cost, 2)


def check_specialist_availability(specialization, required_specialization):
    """Проверяет, подходит ли специалист под услугу."""
    if specialization == required_specialization:
        return True
    return False


def get_request_status(is_available, request_date):
    """Возвращает статус заявки в зависимости от доступности специалиста."""
    if is_available:
        return f"Заявка от {request_date}: специалист назначен"
    return f"Заявка от {request_date}: специалист не найден"




print("=== Сервис поиска специалистов по ремонту ===")
print(get_client_info(client_name, client_phone))
print(get_specialist_info(specialist_name,
                         specialist_specialization,
                         specialist_rate))
print(get_service_info(service_name, service_hours))

required = "Сантехник"
available = check_specialist_availability(specialist_specialization, required)

print(get_request_status(available, request_date))

if available:
    cost = calculate_cost(specialist_rate, service_hours)
    print(f"Предварительная стоимость: {cost} руб.")
else:
    print("Попробуйте выбрать другого специалиста.")