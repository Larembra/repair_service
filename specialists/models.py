from django.core.validators import MinValueValidator
from django.db import models


class Specialist(models.Model):
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=120, db_index=True)
    rate = models.FloatField(validators=[MinValueValidator(0.01)])

    class Meta:
        ordering = ["rate", "id"]

    def __str__(self):
        return f"{self.name} — {self.specialization}"
