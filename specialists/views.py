from django.shortcuts import get_object_or_404, render

from specialists.models import Specialist


def specialist_list(request):
    specialists = Specialist.objects.all()
    return render(request, "specialists/specialist_list.html", {
        "specialists": specialists,
    })


def specialist_search(request):
    specialization = request.GET.get("specialization", "").strip()
    max_rate = request.GET.get("max_rate", "").strip()
    results = Specialist.objects.none()
    error = ""
    if specialization or max_rate:
        try:
            rate_value = float(max_rate) if max_rate else None
            if rate_value is not None and rate_value <= 0:
                raise ValueError
            results = Specialist.objects.all()
            if specialization:
                results = results.filter(
                    specialization__iexact=specialization,
                )
            if rate_value is not None:
                results = results.filter(rate__lte=rate_value)
            results = results.order_by("rate", "id")
        except ValueError:
            error = "Укажите положительную максимальную ставку."
    return render(request, "specialists/specialist_search.html", {
        "specialization": specialization,
        "max_rate": max_rate,
        "specialists": results,
        "error": error,
        "searched": bool(specialization or max_rate),
    })


def specialist_detail(request, specialist_id: int):
    specialist = get_object_or_404(Specialist, pk=specialist_id)
    return render(request, "specialists/specialist_detail.html", {
        "specialist": specialist,
    })
