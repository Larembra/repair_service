from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from homepage.models import Client
from repair_requests.models import RepairRequest, Service
from specialists.models import Specialist


def request_list(request):
    request_date = request.GET.get("date", "").strip()
    client_id = request.GET.get("client", "").strip()
    specialist_id = request.GET.get("specialist", "").strip()
    service_id = request.GET.get("service", "").strip()
    status = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "date")
    error = ""

    items = RepairRequest.objects.select_related(
        "client", "specialist", "service",
    )
    if request_date:
        try:
            selected_date = datetime.strptime(
                request_date, "%Y-%m-%d",
            ).date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            items = items.filter(request_date=selected_date)
    if client_id.isdigit():
        items = items.filter(client_id=int(client_id))
    if specialist_id.isdigit():
        items = items.filter(specialist_id=int(specialist_id))
    if service_id.isdigit():
        items = items.filter(service_id=int(service_id))
    if status == "active":
        items = items.filter(is_cancelled=False)
    elif status == "cancelled":
        items = items.filter(is_cancelled=True)

    sort_fields = {
        "date": "request_date",
        "client": "client__name",
        "specialist": "specialist__name",
        "service": "service__name",
    }
    items = items.order_by(sort_fields.get(sort, "request_date"), "id")
    paginator = Paginator(items, 5)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "repair_requests/request_list.html", {
        "requests": page_obj,
        "page_obj": page_obj,
        "request_date": request_date,
        "selected_client": client_id,
        "selected_specialist": specialist_id,
        "selected_service": service_id,
        "status": status,
        "sort": sort if sort in sort_fields else "date",
        "clients": Client.objects.order_by("name"),
        "specialists": Specialist.objects.order_by("name"),
        "services": Service.objects.order_by("name"),
        "error": error,
    })


def request_statistics(request):
    status_counts = RepairRequest.objects.values(
        "is_cancelled",
    ).annotate(request_count=Count("id")).order_by("is_cancelled")
    specialist_counts = Specialist.objects.annotate(
        request_count=Count("repair_requests"),
    ).values("name", "request_count").order_by("-request_count", "name")
    totals = {
        "total": RepairRequest.objects.count(),
        "active": RepairRequest.objects.filter(is_cancelled=False).count(),
    }
    return render(request, "repair_requests/statistics.html", {
        "status_counts": status_counts,
        "specialist_counts": specialist_counts,
        "totals": totals,
    })


def request_detail(request, request_id: int):
    requests = RepairRequest.objects.select_related(
        "client", "specialist", "service",
    )
    item = get_object_or_404(requests, pk=request_id)
    cost = item.estimated_cost
    return render(request, "repair_requests/request_detail.html", {
        "item": item,
        "cost": cost,
    })
