from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=32)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return self.name


urlpatterns = []
