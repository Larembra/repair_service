from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("specialists/", include("specialists.urls")),
    path("requests/", include("repair_requests.urls")),
]
