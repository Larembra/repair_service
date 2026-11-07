from django.core.validators import MinValueValidator
from django.db import models

from homepage.models import Client
from specialists.models import Specialist


class Service(models.Model):
    name = models.CharField("Название услуги", max_length=200)
    required_specialization = models.CharField(
        "Требуемая специализация",
        max_length=120,
        db_index=True,
    )
    hours = models.FloatField(
        "Ориентировочная длительность, ч",
        validators=[MinValueValidator(0.01)],
    )

    class Meta:
        ordering = ["name", "id"]
        verbose_name = "услуга"
        verbose_name_plural = "услуги"

    def __str__(self):
        return self.name


class RepairRequest(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="repair_requests",
        verbose_name="Клиент",
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.PROTECT,
        related_name="repair_requests",
        verbose_name="Специалист",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="repair_requests",
        verbose_name="Услуга",
    )
    request_date = models.DateField("Дата заявки", db_index=True)
    is_cancelled = models.BooleanField(
        "Заявка отменена",
        default=False,
        db_index=True,
    )

    class Meta:
        ordering = ["-request_date", "-id"]
        verbose_name = "заявка"
        verbose_name_plural = "заявки"

    @property
    def status(self):
        return "отменена" if self.is_cancelled else "новая"

    @property
    def estimated_cost(self):
        return round(self.specialist.rate * self.service.hours, 2)

    def __str__(self):
        return f"Заявка №{self.pk} — {self.status}"
