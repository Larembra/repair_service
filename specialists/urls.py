from django.urls import path

from . import views

app_name = "specialists"
urlpatterns = [
    path("", views.specialist_list, name="list"),
    path("<int:specialist_id>/", views.specialist_detail, name="detail"),
    path("search/", views.specialist_search, name="search"),
]
