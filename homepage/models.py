from django.db import models


class Client(models.Model):
    name = models.CharField("Имя клиента", max_length=200)
    phone = models.CharField("Телефон", max_length=32)

    class Meta:
        ordering = ["name", "id"]
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return self.name


urlpatterns = []
