from django.core.validators import MinValueValidator
from django.db import models

from homepage.models import Client
from specialists.models import Specialist


class Service(models.Model):
    name = models.CharField(max_length=200)
    required_specialization = models.CharField(max_length=120, db_index=True)
    hours = models.FloatField(validators=[MinValueValidator(0.01)])

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return self.name


class RepairRequest(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="repair_requests",
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.PROTECT,
        related_name="repair_requests",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="repair_requests",
    )
    request_date = models.DateField(db_index=True)
    is_cancelled = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-request_date", "-id"]

    @property
    def status(self):
        return "отменена" if self.is_cancelled else "новая"

    @property
    def estimated_cost(self):
        return round(self.specialist.rate * self.service.hours, 2)

    def __str__(self):
        return f"Заявка №{self.pk} — {self.status}"
