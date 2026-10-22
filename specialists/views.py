from django.shortcuts import render

from db.database import get_connection
from models.specialists import find_specialist_by_id
from storage import load_specialists


def specialist_list(request):
    with get_connection() as connection:
        specialists = connection.execute(
            "SELECT id, name, specialization, rate "
            "FROM specialists ORDER BY rate"
        ).fetchall()
    return render(request, "specialists/specialist_list.html", {
        "specialists": specialists,
    })


def specialist_search(request):
    specialization = request.GET.get("specialization", "").strip()
    max_rate = request.GET.get("max_rate", "").strip()
    results = []
    error = ""
    if specialization or max_rate:
        query = (
            "SELECT id, name, specialization, rate FROM specialists "
            "WHERE (? = '' OR specialization = ? COLLATE NOCASE) "
            "AND (? = '' OR rate <= ?) ORDER BY rate"
        )
        try:
            rate_value = float(max_rate) if max_rate else None
            if rate_value is not None and rate_value <= 0:
                raise ValueError
            with get_connection() as connection:
                results = connection.execute(
                    query, (specialization, specialization, max_rate,
                            rate_value),
                ).fetchall()
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
    specialist = find_specialist_by_id(load_specialists(), specialist_id)
    if specialist is None:
        return render(request, "specialists/not_found.html", status=404)
    return render(request, "specialists/specialist_detail.html", {
        "specialist": specialist,
    })
