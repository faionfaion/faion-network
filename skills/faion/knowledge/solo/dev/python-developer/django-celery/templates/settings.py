"""
Django CELERY_* settings block for production reliability.
Add to config/settings.py (or settings/base.py).
"""
import os

# Broker and backend
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

# Serialization — always use JSON; never pickle in production
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

# Timezone
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True

# Reliability
CELERY_TASK_ACKS_LATE = True              # re-queue on worker crash
CELERY_TASK_REJECT_ON_WORKER_LOST = True  # mark FAILURE if worker dies mid-task
CELERY_WORKER_PREFETCH_MULTIPLIER = 1     # one task at a time per worker slot

# Limits — set project-wide defaults; override per-task
CELERY_TASK_SOFT_TIME_LIMIT = 300   # 5 minutes
CELERY_TASK_TIME_LIMIT = 360        # 6 minutes (hard kill)

# Result expiry
CELERY_RESULT_EXPIRES = 3600  # 1 hour

# Routing — define queues; separate long tasks from fast ones
CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_QUEUES = {
    "default": {"exchange": "default", "routing_key": "default"},
    "heavy": {"exchange": "heavy", "routing_key": "heavy"},
}

# Beat scheduler — use django-celery-beat for deploys that survive restarts
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Logging
CELERY_WORKER_HIJACK_ROOT_LOGGER = False  # keep Django's logging config

# Development: do NOT enable ALWAYS_EAGER in production; it hides broker bugs
# CELERY_TASK_ALWAYS_EAGER = True  # only in test when using celery_eager fixture
