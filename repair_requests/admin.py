from django.contrib import admin, messages
from django.db.models import Count, F

from repair_requests.models import RepairRequest, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "required_specialization",
        "hours",
        "request_count",
    )
    list_display_links = ("name",)
    search_fields = ("name", "required_specialization")
    list_filter = ("required_specialization",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(request_count=Count("repair_requests"))

    @admin.display(description="Заявок", ordering="request_count")
    def request_count(self, obj):
        return obj.request_count


@admin.action(description="Отменить выбранные заявки")
def cancel_requests(modeladmin, request, queryset):
    updated = queryset.filter(is_cancelled=False).update(is_cancelled=True)
    modeladmin.message_user(
        request,
        f"Отменено заявок: {updated}.",
        messages.SUCCESS,
    )


@admin.action(description="Восстановить выбранные заявки")
def restore_requests(modeladmin, request, queryset):
    updated = queryset.filter(is_cancelled=True).update(is_cancelled=False)
    modeladmin.message_user(
        request,
        f"Восстановлено заявок: {updated}.",
        messages.SUCCESS,
    )


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "specialist",
        "service",
        "specialist_rate",
        "service_hours",
        "request_date",
        "is_cancelled",
        "estimated_cost",
    )
    list_display_links = ("id",)
    search_fields = (
        "client__name",
        "client__phone",
        "specialist__name",
        "service__name",
    )
    list_filter = (
        "request_date",
        "is_cancelled",
        "specialist__specialization",
        "service",
    )
    ordering = ("-request_date", "-id")
    list_per_page = 20
    list_select_related = ("client", "specialist", "service")
    readonly_fields = ("id", "estimated_cost")
    actions = (cancel_requests, restore_requests)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            specialist_rate_value=F("specialist__rate"),
            service_hours_value=F("service__hours"),
        )

    @admin.display(
        description="Ставка специалиста",
        ordering="specialist_rate_value",
    )
    def specialist_rate(self, obj):
        return obj.specialist_rate_value

    @admin.display(
        description="Длительность услуги, ч",
        ordering="service_hours_value",
    )
    def service_hours(self, obj):
        return obj.service_hours_value

    @admin.display(description="Стоимость", ordering="service__hours")
    def estimated_cost(self, obj):
        return obj.estimated_cost
