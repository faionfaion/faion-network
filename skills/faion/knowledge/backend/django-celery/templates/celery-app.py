"""
Celery application bootstrap for Django.

Place this file at: config/celery.py
Then add to config/__init__.py:
    from .celery import app as celery_app
    __all__ = ("celery_app",)
"""
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("myproject")

# Load config from Django settings under CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all installed INSTALLED_APPS
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
