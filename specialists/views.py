from django.shortcuts import render

from models.specialists import find_specialist_by_id, sort_specialists_by_rate
from storage import load_specialists


def specialist_list(request):
    return render(request, "specialists/specialist_list.html", {
        "specialists": sort_specialists_by_rate(load_specialists()),
    })


def specialist_detail(request, specialist_id: int):
    specialist = find_specialist_by_id(load_specialists(), specialist_id)
    if specialist is None:
        return render(request, "specialists/not_found.html", status=404)
    return render(request, "specialists/specialist_detail.html", {
        "specialist": specialist,
    })
