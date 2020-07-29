import os

import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_backend.settings")
django.setup()

from healthcheck.tasks import get_services

print(get_services())

