from django.shortcuts import render

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
    return render(request, "repair_requests/request_list.html", {
        "requests": _load_domain_requests(),
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
