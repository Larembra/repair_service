from django.contrib import admin
from django.db.models import Count, Q

from repair_requests.models import RepairRequest
from specialists.models import Specialist


class RepairRequestInline(admin.TabularInline):
    model = RepairRequest
    fields = ("client", "service", "request_date", "is_cancelled")
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialization", "rate", "request_count")
    list_display_links = ("name",)
    search_fields = ("name", "specialization")
    list_filter = ("specialization",)
    ordering = ("rate", "name")
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (RepairRequestInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            request_count=Count("repair_requests"),
            active_request_count=Count(
                "repair_requests",
                filter=Q(repair_requests__is_cancelled=False),
            ),
        )

    @admin.display(description="Заявок", ordering="request_count")
    def request_count(self, obj):
        return obj.request_count

    @admin.display(
        description="Активных заявок",
        ordering="active_request_count",
    )
    def active_request_count(self, obj):
        return obj.active_request_count
