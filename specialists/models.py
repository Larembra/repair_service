from django.core.validators import MinValueValidator
from django.db import models


class Specialist(models.Model):
    name = models.CharField("Имя специалиста", max_length=200)
    specialization = models.CharField(
        "Специализация",
        max_length=120,
        db_index=True,
    )
    rate = models.FloatField(
        "Ставка за час",
        validators=[MinValueValidator(0.01)],
    )

    class Meta:
        ordering = ["rate", "id"]
        verbose_name = "специалист"
        verbose_name_plural = "специалисты"

    def __str__(self):
        return f"{self.name} — {self.specialization}"
