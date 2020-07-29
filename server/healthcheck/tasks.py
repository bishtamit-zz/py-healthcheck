from .models import Service


def get_services():
    return Service.objects.filter()
