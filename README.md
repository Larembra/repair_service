# Сервис поиска специалистов по ремонту

Консольное приложение для поиска специалистов по ремонту
(сантехников, электриков, мастеров отделочных работ),
оформления и отмены заявок, ведения каталога услуг.

## Возможности

- просмотр и поиск специалистов по специализации и ставке;
- сортировка специалистов по ставке;
- ведение каталога услуг;
- регистрация клиентов;
- создание заявок с проверкой доступности специалиста на дату;
- отмена заявок;
- статистика заявок по статусам;
- сохранение и загрузка данных в JSON-файлах;
- обработка некорректного ввода пользователя.

## Предметная область

Клиент создаёт заявку на услугу, которую выполняет специалист
подходящей специализации. У специалиста не может быть двух активных
заявок на одну дату. Отменённая заявка не удаляется и не блокирует
специалиста.

## Основные классы

### Client — клиент

- атрибуты: `id`, `name`, `phone`;
- методы: `__str__()`, `to_data()`, `from_data()`.

### Specialist — специалист

- атрибуты: `id`, `name`, `specialization`, `rate`;
- методы: `is_suitable_for(service)`, `__str__()`, `to_data()`,
  `from_data()`, статический `validate_rate()`.

### Service — услуга

- атрибуты: `id`, `name`, `required_specialization`, `hours`;
- методы: `calculate_cost(rate)`, `__str__()`, `to_data()`,
  `from_data()`, статический `validate_hours()`.

### RepairRequest — заявка

- атрибуты: `id`, `client`, `specialist`, `service`, `request_date`,
  `is_cancelled`;
- свойство `status` («новая» / «отменена»);
- методы: `cancel()`, `__str__()`, `to_data()`, `from_data()`.

## Взаимодействие объектов

```text
Client --создаёт--> RepairRequest --назначена--> Specialist
                          |
                          +--относится к--> Service
```

`RepairRequest` хранит ссылки на объекты `Client`, `Specialist`
и `Service`, а не только их идентификаторы. Функции модулей работают
с коллекциями `list[Client]`, `list[Specialist]`, `list[Service]`,
`list[RepairRequest]`.

## Хранение данных

Данные хранятся в `data/clients.json`, `data/specialists.json`,
`data/services.json`, `data/requests.json`. При загрузке JSON
преобразуется в объекты, при сохранении объекты преобразуются
в данные. В `requests.json` записываются идентификаторы
`client_id`, `specialist_id`, `service_id`. Формат файлов из ПР2
читается автоматически.

## Структура проекта

```text
repair_service/
├── README.md
├── requirements.txt
├── .gitignore
├── conftest.py
├── main.py
├── storage.py
├── utils.py
├── models/
│   ├── __init__.py
│   ├── clients.py
│   ├── specialists.py
│   ├── services.py
│   └── repair_requests.py
├── data/
└── tests/
    ├── test_clients.py
    ├── test_specialists.py
    ├── test_services.py
    ├── test_repair_requests.py
    └── test_storage.py
```

## Требования

- Python 3.10+;
- pytest;
- flake8.

## Установка зависимостей

```text
pip install -r requirements.txt
```

## Запуск

```text
python main.py
```

## Тестирование

```text
pytest -v
```

## Проверка качества кода

```text
flake8 .
```