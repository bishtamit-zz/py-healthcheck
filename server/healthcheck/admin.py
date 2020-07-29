from django.contrib import admin
from .models import Service

# Register your models here.


class ServiceA(admin.ModelAdmin):
    list_display = ("name", "_type", "start_on_stop")


admin.site.site_header = "Health Check customization"
admin.site.register(Service, ServiceA)

