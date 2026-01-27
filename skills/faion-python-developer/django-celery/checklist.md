# Django Celery Integration Checklist

Step-by-step guide for integrating Celery with Django projects.

## Phase 1: Installation and Setup

### 1.1 Install Dependencies

```bash
# Core packages
pip install celery[redis]  # or celery[rabbitmq]
pip install django-celery-beat  # Periodic tasks
pip install django-celery-results  # Store results in DB
pip install flower  # Monitoring

# Add to requirements.txt
celery[redis]>=5.4.0
django-celery-beat>=2.6.0
django-celery-results>=2.5.0
flower>=2.0.0
redis>=5.0.0  # or kombu[rabbitmq] for RabbitMQ
```

- [ ] Install celery with broker support
- [ ] Install django-celery-beat for periodic tasks
- [ ] Install django-celery-results (optional, for DB results)
- [ ] Install flower for monitoring
- [ ] Pin versions in requirements.txt

### 1.2 Django Settings

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'django_celery_beat',
    'django_celery_results',  # Optional
]

# Celery Configuration
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/1')

# Task settings
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'  # Match Django TIME_ZONE if different

# Reliability settings
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

# Result expiration (1 hour)
CELERY_RESULT_EXPIRES = 3600

# Track task started state
CELERY_TASK_TRACK_STARTED = True

# Beat scheduler (use database)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
```

- [ ] Add celery apps to INSTALLED_APPS
- [ ] Configure broker URL
- [ ] Configure result backend
- [ ] Set serialization settings
- [ ] Configure reliability options
- [ ] Set result expiration

### 1.3 Create Celery App

```python
# config/celery.py (or project_name/celery.py)
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')  # Match your project name

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Test task for debugging."""
    print(f'Request: {self.request!r}')
```

- [ ] Create celery.py in project directory
- [ ] Set DJANGO_SETTINGS_MODULE
- [ ] Configure namespace for settings
- [ ] Enable autodiscover_tasks()

### 1.4 Update __init__.py

```python
# config/__init__.py (or project_name/__init__.py)
from .celery import app as celery_app

__all__ = ('celery_app',)
```

- [ ] Import celery_app in __init__.py
- [ ] Export in __all__

### 1.5 Run Migrations

```bash
python manage.py migrate django_celery_beat
python manage.py migrate django_celery_results  # If using
```

- [ ] Run migrations for django_celery_beat
- [ ] Run migrations for django_celery_results (if used)

## Phase 2: Task Development

### 2.1 Create First Task

```python
# apps/orders/tasks.py
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name='orders.process_order',
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_backoff_max=600,
    soft_time_limit=300,
    time_limit=360,
)
def process_order(self, order_id: int) -> dict:
    """Process an order asynchronously.

    Args:
        order_id: The order ID to process

    Returns:
        dict: Processing result with status
    """
    from apps.orders.models import Order

    try:
        order = Order.objects.get(pk=order_id)
        # Processing logic here...
        logger.info(f"Processed order {order_id}")
        return {'status': 'success', 'order_id': order_id}
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
        return {'status': 'error', 'reason': 'not_found'}
```

- [ ] Create tasks.py in app directory
- [ ] Use @shared_task decorator
- [ ] Add explicit task name
- [ ] Configure retry settings
- [ ] Set time limits
- [ ] Import models inside function (avoid circular imports)
- [ ] Add proper logging
- [ ] Return meaningful results

### 2.2 Configure Task Routing (Optional)

```python
# settings.py
CELERY_TASK_ROUTES = {
    'orders.*': {'queue': 'orders'},
    'emails.*': {'queue': 'emails'},
    'reports.*': {'queue': 'reports'},
    '*.slow_task': {'queue': 'slow'},
}

# Or in celery.py
app.conf.task_routes = {
    'orders.*': {'queue': 'orders'},
    'emails.*': {'queue': 'emails'},
}
```

- [ ] Define queue mapping for task patterns
- [ ] Separate critical from background tasks
- [ ] Consider CPU vs I/O bound separation

### 2.3 Call Tasks from Views

```python
# apps/orders/views.py
from django.db import transaction
from .tasks import process_order


class OrderCreateView(CreateView):
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            # Use delay_on_commit for safety in transactions
            process_order.delay_on_commit(self.object.id)
        return redirect(self.get_success_url())


# Or without transaction
def create_order(request):
    order = Order.objects.create(...)
    # Simple async call
    process_order.delay(order.id)
    # With countdown (delay in seconds)
    process_order.apply_async(args=[order.id], countdown=60)
    # With ETA
    process_order.apply_async(args=[order.id], eta=datetime.now() + timedelta(hours=1))
```

- [ ] Use delay() for simple async calls
- [ ] Use delay_on_commit() inside transactions
- [ ] Use apply_async() for countdown/ETA
- [ ] Pass IDs, not objects (serialization)

## Phase 3: Periodic Tasks (Celery Beat)

### 3.1 Define Periodic Tasks in Code

```python
# config/celery.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    'daily-report': {
        'task': 'reports.generate_daily_report',
        'schedule': crontab(hour=6, minute=0),
        'kwargs': {'report_type': 'daily'},
    },
    'cleanup-every-hour': {
        'task': 'maintenance.cleanup_old_records',
        'schedule': crontab(minute=0),  # Every hour
    },
    'check-payments-every-5-min': {
        'task': 'payments.check_pending',
        'schedule': 300.0,  # Every 5 minutes (seconds)
    },
}
```

- [ ] Define beat_schedule in celery.py
- [ ] Use crontab for specific times
- [ ] Use float for interval (seconds)
- [ ] Set appropriate schedule for each task

### 3.2 Define Periodic Tasks via Admin

```python
# Use Django Admin to manage:
# - IntervalSchedule: Every X seconds/minutes/hours/days
# - CrontabSchedule: Cron-like expressions
# - ClockedSchedule: One-time execution at specific datetime
# - PeriodicTask: Links task to schedule
```

- [ ] Create schedules in Admin
- [ ] Create PeriodicTask linking task to schedule
- [ ] Test schedule with short interval first
- [ ] Monitor execution in Flower

### 3.3 Programmatic Schedule Management

```python
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
import json


def create_periodic_task(name, task, minutes=10, kwargs=None):
    """Create or update a periodic task."""
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=minutes,
        period=IntervalSchedule.MINUTES,
    )

    PeriodicTask.objects.update_or_create(
        name=name,
        defaults={
            'interval': schedule,
            'task': task,
            'kwargs': json.dumps(kwargs or {}),
            'enabled': True,
        }
    )


def create_crontab_task(name, task, hour='6', minute='0', day_of_week='*'):
    """Create a crontab-based periodic task."""
    schedule, _ = CrontabSchedule.objects.get_or_create(
        hour=hour,
        minute=minute,
        day_of_week=day_of_week,
        timezone='UTC',
    )

    PeriodicTask.objects.update_or_create(
        name=name,
        defaults={
            'crontab': schedule,
            'task': task,
            'enabled': True,
        }
    )
```

- [ ] Use update_or_create for idempotency
- [ ] Set timezone explicitly
- [ ] Enable/disable via Admin or code

## Phase 4: Testing

### 4.1 Unit Tests with Mocking

```python
# tests/test_tasks.py
import pytest
from unittest.mock import patch, MagicMock
from apps.orders.tasks import process_order


class TestProcessOrder:
    @patch('apps.orders.tasks.Order.objects.get')
    def test_process_order_success(self, mock_get):
        """Test successful order processing."""
        mock_order = MagicMock()
        mock_order.id = 1
        mock_get.return_value = mock_order

        result = process_order(order_id=1)

        assert result['status'] == 'success'
        mock_get.assert_called_once_with(pk=1)

    @patch('apps.orders.tasks.Order.objects.get')
    def test_process_order_not_found(self, mock_get):
        """Test order not found handling."""
        from django.core.exceptions import ObjectDoesNotExist
        mock_get.side_effect = ObjectDoesNotExist

        result = process_order(order_id=999)

        assert result['status'] == 'error'
```

- [ ] Mock external dependencies
- [ ] Test task logic directly (call function)
- [ ] Test success and failure paths
- [ ] Test retry behavior

### 4.2 Integration Tests with Fixtures

```python
# conftest.py
import pytest


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'memory://',
        'result_backend': 'rpc://',
        'task_always_eager': False,
    }


@pytest.fixture(scope='session')
def celery_worker_parameters():
    return {
        'perform_ping_check': False,
    }


@pytest.fixture
def celery_task_eager(settings):
    """Run tasks synchronously in tests."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
    yield
```

```python
# test_integration.py
import pytest
from apps.orders.tasks import process_order


@pytest.mark.usefixtures('celery_session_app', 'celery_session_worker')
class TestCeleryIntegration:
    def test_task_execution(self, db):
        """Test actual task execution."""
        order = Order.objects.create(...)
        result = process_order.delay(order.id)

        assert result.get(timeout=10)['status'] == 'success'
```

- [ ] Configure test fixtures
- [ ] Use memory:// broker for isolation
- [ ] Test async execution with celery_worker
- [ ] Use eager mode for simpler tests

### 4.3 Test Task Retries

```python
@patch('apps.orders.tasks.external_api_call')
def test_task_retry_on_connection_error(self, mock_api):
    """Test task retries on connection error."""
    mock_api.side_effect = ConnectionError('API down')

    task = process_order.s(order_id=1)

    with pytest.raises(ConnectionError):
        task.apply().get()

    # Verify retry was attempted
    assert mock_api.call_count == 4  # 1 initial + 3 retries
```

- [ ] Test retry mechanism
- [ ] Verify retry count
- [ ] Test retry delay/backoff

## Phase 5: Monitoring Setup

### 5.1 Flower Dashboard

```bash
# Development
celery -A config flower --port=5555

# Production (with auth)
celery -A config flower \
    --basic_auth=admin:password \
    --port=5555 \
    --persistent=True \
    --db=/var/flower/flower.db
```

```yaml
# docker-compose.yml
flower:
  image: mher/flower:latest
  command: celery --broker=${CELERY_BROKER_URL} flower --port=5555
  ports:
    - "5555:5555"
  environment:
    - CELERY_BROKER_URL=${CELERY_BROKER_URL}
    - FLOWER_BASIC_AUTH=admin:${FLOWER_PASSWORD}
  depends_on:
    - redis
    - worker
```

- [ ] Enable basic auth in production
- [ ] Configure persistent storage
- [ ] Set up behind reverse proxy with HTTPS
- [ ] Add to docker-compose

### 5.2 Prometheus Metrics

```bash
# Start Flower with Prometheus exporter
celery -A config flower --prometheus_metrics
```

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'celery'
    static_configs:
      - targets: ['flower:5555']
```

- [ ] Enable --prometheus_metrics flag
- [ ] Configure Prometheus scraping
- [ ] Create Grafana dashboard

### 5.3 Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'celery': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'celery': {
            'handlers': ['celery'],
            'level': 'INFO',
        },
        'celery.task': {
            'handlers': ['celery'],
            'level': 'INFO',
        },
    },
}
```

- [ ] Configure celery logger
- [ ] Set appropriate log levels
- [ ] Route logs to centralized system

## Phase 6: Production Deployment

### 6.1 Worker Configuration

```bash
# CPU-bound tasks (image processing, calculations)
celery -A config worker \
    --pool=prefork \
    --concurrency=4 \
    --max-tasks-per-child=1000 \
    --loglevel=INFO \
    -Q default,orders

# I/O-bound tasks (API calls, emails)
celery -A config worker \
    --pool=gevent \
    --concurrency=100 \
    --loglevel=INFO \
    -Q emails,notifications
```

- [ ] Choose appropriate pool (prefork vs gevent)
- [ ] Set concurrency based on workload
- [ ] Enable max-tasks-per-child for memory management
- [ ] Assign workers to specific queues

### 6.2 Beat Scheduler

```bash
# Run Beat separately from workers
celery -A config beat \
    --scheduler django_celery_beat.schedulers:DatabaseScheduler \
    --loglevel=INFO
```

- [ ] Run Beat as separate process
- [ ] Use DatabaseScheduler for admin control
- [ ] Ensure only ONE Beat instance runs

### 6.3 Systemd Services

```ini
# /etc/systemd/system/celery.service
[Unit]
Description=Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
EnvironmentFile=/etc/default/celery
WorkingDirectory=/var/www/project
ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} multi start ${CELERYD_NODES} \
    --pidfile=${CELERYD_PID_FILE} \
    --logfile=${CELERYD_LOG_FILE} \
    --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
    --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
    --pidfile=${CELERYD_PID_FILE} \
    --logfile=${CELERYD_LOG_FILE} \
    --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
Restart=always

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/celerybeat.service
[Unit]
Description=Celery Beat
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
EnvironmentFile=/etc/default/celery
WorkingDirectory=/var/www/project
ExecStart=${CELERY_BIN} -A ${CELERY_APP} beat \
    --scheduler django_celery_beat.schedulers:DatabaseScheduler \
    --loglevel=${CELERYD_LOG_LEVEL}
Restart=always

[Install]
WantedBy=multi-user.target
```

- [ ] Create systemd service files
- [ ] Configure environment file
- [ ] Enable services on boot
- [ ] Test restart behavior

### 6.4 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    depends_on:
      - redis
      - db

  worker:
    build: .
    command: celery -A config worker --pool=prefork --concurrency=4 --loglevel=INFO
    depends_on:
      - redis
      - db
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0

  worker-io:
    build: .
    command: celery -A config worker --pool=gevent --concurrency=100 -Q emails,notifications --loglevel=INFO
    depends_on:
      - redis
      - db
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0

  beat:
    build: .
    command: celery -A config beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=INFO
    depends_on:
      - redis
      - db
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0

  flower:
    build: .
    command: celery -A config flower --port=5555
    ports:
      - "5555:5555"
    depends_on:
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0

volumes:
  redis_data:
```

- [ ] Configure worker container
- [ ] Configure beat container (single instance)
- [ ] Configure flower container
- [ ] Set proper dependencies
- [ ] Configure health checks

## Phase 7: Verification Checklist

### Development

- [ ] Worker starts without errors
- [ ] Beat scheduler starts
- [ ] Tasks appear in Flower
- [ ] Tasks execute successfully
- [ ] Retries work correctly
- [ ] Periodic tasks trigger

### Staging/Production

- [ ] Workers connect to broker
- [ ] Results stored correctly
- [ ] Monitoring accessible
- [ ] Logs captured
- [ ] Alerts configured
- [ ] Load tested

### Security

- [ ] Broker requires authentication
- [ ] Result backend secured
- [ ] Flower behind HTTPS
- [ ] No secrets in task arguments
- [ ] Pickle serialization disabled

---

*Celery 5.4+ | Django 5.x*
