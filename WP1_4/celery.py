import os
from celery import Celery
from Main.tasks import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WP1_4.settings")
app = Celery("WP1_4")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
