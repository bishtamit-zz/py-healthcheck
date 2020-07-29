from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Service(models.Model):
    class ServiceChoice(models.TextChoices):
        old = "init", _("init.d")
        new = "systemctl", _("systemctl")

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_on_stop = models.BooleanField(default=True)
    _type = models.CharField(
        choices=ServiceChoice.choices, default=ServiceChoice.new, max_length=10
    )

    def __str__(self):
        return self.name

    def show_desc(self):
        return self.description
