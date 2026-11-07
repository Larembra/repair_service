import sqlite3
from datetime import date

from django.db import transaction

from db.database import DB_PATH
from homepage.models import Client
from repair_requests.models import RepairRequest, Service
from specialists.models import Specialist


def import_sqlite_to_orm():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {DB_PATH}")

    with sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) as connection:
        connection.row_factory = sqlite3.Row
        clients = connection.execute(
            "SELECT id, name, phone FROM clients ORDER BY id",
        ).fetchall()
        specialists = connection.execute(
            "SELECT id, name, specialization, rate "
            "FROM specialists ORDER BY id",
        ).fetchall()
        services = connection.execute(
            "SELECT id, name, required_specialization, hours "
            "FROM services ORDER BY id",
        ).fetchall()
        requests = connection.execute(
            "SELECT id, client_id, specialist_id, service_id, request_date, "
            "is_cancelled FROM repair_requests ORDER BY id",
        ).fetchall()

    with transaction.atomic():
        for row in clients:
            Client.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"], "phone": row["phone"]},
            )
        for row in specialists:
            Specialist.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "specialization": row["specialization"],
                    "rate": row["rate"],
                },
            )
        for row in services:
            Service.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "required_specialization": row["required_specialization"],
                    "hours": row["hours"],
                },
            )
        for row in requests:
            raw_date = row["request_date"]
            request_date = (
                date.fromisoformat(raw_date[:10]) if raw_date else date.today()
            )
            RepairRequest.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "client_id": row["client_id"],
                    "specialist_id": row["specialist_id"],
                    "service_id": row["service_id"],
                    "request_date": request_date,
                    "is_cancelled": bool(row["is_cancelled"]),
                },
            )

    print("Перенос данных завершён.")
    print(f"Клиентов: {Client.objects.count()}")
    print(f"Специалистов: {Specialist.objects.count()}")
    print(f"Услуг: {Service.objects.count()}")
    print(f"Заявок: {RepairRequest.objects.count()}")
