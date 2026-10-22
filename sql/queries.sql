-- 1. Каталог специалистов
SELECT id, name, specialization, rate
FROM specialists
ORDER BY rate;

-- 2. Каталог услуг
SELECT id, name, required_specialization, hours
FROM services
ORDER BY name;

-- 3. Специалисты с верхней границей ставки (WHERE)
SELECT id, name, specialization, rate
FROM specialists
WHERE rate <= ?
ORDER BY rate;

-- 4. Поиск специалистов по специализации (WHERE)
SELECT id, name, specialization, rate
FROM specialists
WHERE specialization = ? COLLATE NOCASE
ORDER BY rate;

-- 5. Заявки со связанными клиентом, специалистом и услугой (JOIN)
SELECT r.id, r.request_date, r.is_cancelled,
       c.name AS client_name, c.phone AS client_phone,
       sp.name AS specialist_name, sp.specialization, sp.rate,
       sv.name AS service_name, sv.hours
FROM repair_requests AS r
JOIN clients AS c ON c.id = r.client_id
JOIN specialists AS sp ON sp.id = r.specialist_id
JOIN services AS sv ON sv.id = r.service_id
ORDER BY r.request_date DESC;

-- 6. Активные заявки со связанными данными (JOIN, WHERE)
SELECT r.id, r.request_date, c.name AS client_name,
       sp.name AS specialist_name, sv.name AS service_name
FROM repair_requests AS r
JOIN clients AS c ON c.id = r.client_id
JOIN specialists AS sp ON sp.id = r.specialist_id
JOIN services AS sv ON sv.id = r.service_id
WHERE r.is_cancelled = 0
ORDER BY r.request_date;

-- 7. Количество специалистов
SELECT COUNT(*) AS specialist_count
FROM specialists;

-- 8. Количество заявок по статусу
SELECT is_cancelled, COUNT(*) AS request_count
FROM repair_requests
GROUP BY is_cancelled;

-- 9. Статистика заявок по специалистам
SELECT sp.id, sp.name AS specialist_name,
       COUNT(r.id) AS request_count
FROM specialists AS sp
LEFT JOIN repair_requests AS r ON r.specialist_id = sp.id
GROUP BY sp.id, sp.name
ORDER BY request_count DESC, sp.name;

-- 10. Специалисты с числом активных заявок выше порога (GROUP BY, HAVING)
SELECT sp.id, sp.name AS specialist_name,
       COUNT(r.id) AS active_request_count
FROM specialists AS sp
JOIN repair_requests AS r ON r.specialist_id = sp.id
WHERE r.is_cancelled = 0
GROUP BY sp.id, sp.name
HAVING COUNT(r.id) > ?
ORDER BY active_request_count DESC;

-- 11. Доступные для услуги специалисты по специализации
SELECT sp.id, sp.name, sp.specialization, sp.rate,
       sv.name AS service_name, sv.hours
FROM specialists AS sp
JOIN services AS sv
  ON sp.specialization = sv.required_specialization COLLATE NOCASE
WHERE sv.id = ?
ORDER BY sp.rate;
