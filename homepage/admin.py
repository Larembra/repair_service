from django.contrib import admin
from django.db.models import Count

from homepage.models import Client
from repair_requests.models import RepairRequest


class RepairRequestInline(admin.TabularInline):
    model = RepairRequest
    fields = ("specialist", "service", "request_date", "is_cancelled")
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "request_count")
    list_display_links = ("name",)
    search_fields = ("name", "phone")
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (RepairRequestInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(request_count=Count("repair_requests"))

    @admin.display(description="Заявок", ordering="request_count")
    def request_count(self, obj):
        return obj.request_count
