-- Клиенты сервиса
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);

-- Специалисты сервиса
CREATE TABLE IF NOT EXISTS specialists (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    rate REAL NOT NULL CHECK (rate > 0)
);

-- Каталог услуг
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    required_specialization TEXT NOT NULL,
    hours REAL NOT NULL CHECK (hours > 0)
);

-- Заявки связывают клиента, специалиста и услугу
CREATE TABLE IF NOT EXISTS repair_requests (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    specialist_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    request_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0 CHECK (is_cancelled IN (0, 1)),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (specialist_id) REFERENCES specialists(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);
