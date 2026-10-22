from django.shortcuts import render

from db.database import get_connection
from models.repair_requests import find_request_by_id
from storage import (
    load_clients,
    load_requests,
    load_services,
    load_specialists,
)


def _load_domain_requests():
    clients = load_clients()
    specialists = load_specialists()
    services = load_services()
    return load_requests(clients, specialists, services)


def request_list(request):
    with get_connection() as connection:
        items = connection.execute(
            "SELECT r.id, r.request_date, r.is_cancelled, "
            "c.name AS client_name, sp.name AS specialist_name, "
            "sv.name AS service_name, sp.rate, sv.hours "
            "FROM repair_requests AS r "
            "JOIN clients AS c ON c.id = r.client_id "
            "JOIN specialists AS sp ON sp.id = r.specialist_id "
            "JOIN services AS sv ON sv.id = r.service_id "
            "ORDER BY r.request_date DESC"
        ).fetchall()
    return render(request, "repair_requests/request_list.html", {
        "requests": items,
    })


def request_statistics(request):
    with get_connection() as connection:
        status_counts = connection.execute(
            "SELECT is_cancelled, COUNT(*) AS request_count "
            "FROM repair_requests GROUP BY is_cancelled"
        ).fetchall()
        specialist_counts = connection.execute(
            "SELECT sp.name AS specialist_name, "
            "COUNT(r.id) AS request_count "
            "FROM specialists AS sp "
            "LEFT JOIN repair_requests AS r ON r.specialist_id = sp.id "
            "GROUP BY sp.id, sp.name ORDER BY request_count DESC, sp.name"
        ).fetchall()
        totals = connection.execute(
            "SELECT COUNT(*) AS total, "
            "SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS active "
            "FROM repair_requests"
        ).fetchone()
    return render(request, "repair_requests/statistics.html", {
        "status_counts": status_counts,
        "specialist_counts": specialist_counts,
        "totals": totals,
    })


def request_detail(request, request_id: int):
    item = find_request_by_id(_load_domain_requests(), request_id)
    if item is None:
        return render(request, "repair_requests/not_found.html", status=404)
    cost = item.service.calculate_cost(item.specialist.rate)
    return render(request, "repair_requests/request_detail.html", {
        "item": item,
        "cost": cost,
    })
