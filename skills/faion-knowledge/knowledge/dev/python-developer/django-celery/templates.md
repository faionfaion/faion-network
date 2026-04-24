# Django Celery Templates

Copy-paste templates for common Celery patterns.

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Task Templates](#2-task-templates)
3. [Configuration Templates](#3-configuration-templates)
4. [Testing Templates](#4-testing-templates)
5. [Docker Templates](#5-docker-templates)
6. [Monitoring Templates](#6-monitoring-templates)

---

## 1. Project Setup

### 1.1 Celery App Configuration

```python
# config/celery.py
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create Celery app
app = Celery('config')

# Load config from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f'Request: {self.request!r}')
```

### 1.2 Django Settings

```python
# config/settings.py

# =============================================================================
# CELERY CONFIGURATION
# =============================================================================

# Broker (message queue)
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')

# Result backend
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/1')

# Serialization
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

# Timezone
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

# Task execution settings
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes

# Worker settings
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Fair distribution
CELERY_WORKER_CONCURRENCY = 4  # Number of worker processes

# Reliability settings
CELERY_TASK_ACKS_LATE = True  # Acknowledge after task completes
CELERY_TASK_REJECT_ON_WORKER_LOST = True  # Requeue if worker dies

# Result settings
CELERY_RESULT_EXPIRES = 3600  # Results expire after 1 hour
CELERY_RESULT_EXTENDED = True  # Store additional task metadata

# Beat scheduler (periodic tasks)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Task routing (optional)
CELERY_TASK_ROUTES = {
    'apps.orders.*': {'queue': 'orders'},
    'apps.emails.*': {'queue': 'emails'},
    'apps.reports.*': {'queue': 'reports'},
}

# Rate limits (optional)
CELERY_TASK_ANNOTATIONS = {
    'apps.integrations.tasks.call_external_api': {'rate_limit': '10/m'},
}
```

### 1.3 Project __init__.py

```python
# config/__init__.py
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### 1.4 Requirements

```txt
# requirements/base.txt
celery[redis]>=5.4.0
django-celery-beat>=2.6.0
django-celery-results>=2.5.0
flower>=2.0.0
redis>=5.0.0

# For RabbitMQ instead of Redis:
# kombu[rabbitmq]>=5.3.0
```

---

## 2. Task Templates

### 2.1 Basic Task with Retry

```python
# apps/{app_name}/tasks.py
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name='{app_name}.{task_name}',
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def task_name(self, param1: int, param2: str = None) -> dict:
    """Task description.

    Args:
        param1: Description
        param2: Optional description

    Returns:
        dict: Result with status
    """
    try:
        # Task logic here
        result = process_something(param1, param2)

        logger.info(f"Task completed: {param1}")
        return {'status': 'success', 'result': result}

    except Exception as e:
        logger.error(f"Task failed: {e}")
        raise
```

### 2.2 Task with Time Limits

```python
@shared_task(
    name='{app_name}.long_running_task',
    bind=True,
    soft_time_limit=300,  # 5 minutes - raises SoftTimeLimitExceeded
    time_limit=360,       # 6 minutes - terminates task
)
def long_running_task(self, data_id: int) -> dict:
    """Long-running task with time limits."""
    from celery.exceptions import SoftTimeLimitExceeded

    try:
        # Long processing...
        for i in range(1000):
            process_chunk(i)

        return {'status': 'success'}

    except SoftTimeLimitExceeded:
        # Graceful cleanup
        logger.warning(f"Task {self.request.id} soft timeout, cleaning up...")
        cleanup_partial_work()
        return {'status': 'timeout', 'partial': True}
```

### 2.3 Idempotent Task

```python
@shared_task(name='{app_name}.idempotent_task')
def idempotent_task(entity_id: int, action: str) -> dict:
    """Idempotent task - safe to retry.

    Uses database state to ensure action only happens once.
    """
    from apps.entities.models import Entity

    entity = Entity.objects.get(pk=entity_id)

    # Idempotency check
    if entity.action_completed:
        return {'status': 'skipped', 'reason': 'already_completed'}

    # Perform action
    perform_action(entity, action)

    # Mark as completed (atomic update)
    Entity.objects.filter(pk=entity_id, action_completed=False).update(
        action_completed=True,
        action_completed_at=timezone.now(),
    )

    return {'status': 'success', 'entity_id': entity_id}
```

### 2.4 Task with Progress Tracking

```python
@shared_task(name='{app_name}.task_with_progress', bind=True)
def task_with_progress(self, items: list) -> dict:
    """Task that reports progress."""
    total = len(items)
    processed = 0
    errors = 0

    for item in items:
        try:
            process_item(item)
            processed += 1
        except Exception as e:
            errors += 1
            logger.error(f"Error processing {item}: {e}")

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'current': processed + errors,
                'total': total,
                'processed': processed,
                'errors': errors,
                'percent': int((processed + errors) / total * 100),
            }
        )

    return {
        'status': 'completed',
        'processed': processed,
        'errors': errors,
        'total': total,
    }
```

### 2.5 Task with Database Transaction Safety

```python
@shared_task(name='{app_name}.transactional_task')
def transactional_task(order_id: int) -> dict:
    """Task with proper transaction handling."""
    from django.db import transaction
    from apps.orders.models import Order, OrderLog

    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=order_id)

            # Check state
            if order.status != 'pending':
                return {'status': 'skipped', 'reason': f'wrong_status:{order.status}'}

            # Update order
            order.status = 'processing'
            order.save()

            # Create log
            OrderLog.objects.create(
                order=order,
                action='status_change',
                details={'from': 'pending', 'to': 'processing'},
            )

        return {'status': 'success', 'order_id': order_id}

    except Order.DoesNotExist:
        return {'status': 'error', 'reason': 'not_found'}
```

### 2.6 Task with External API Call

```python
@shared_task(
    name='{app_name}.api_call_task',
    bind=True,
    max_retries=3,
    autoretry_for=(requests.exceptions.Timeout, requests.exceptions.ConnectionError),
    retry_backoff=True,
    rate_limit='10/m',
)
def api_call_task(self, endpoint: str, payload: dict) -> dict:
    """Task that calls external API with retry and rate limiting."""
    import requests
    from django.conf import settings

    try:
        response = requests.post(
            f'{settings.API_BASE_URL}/{endpoint}',
            json=payload,
            headers={
                'Authorization': f'Bearer {settings.API_KEY}',
                'Content-Type': 'application/json',
            },
            timeout=30,
        )

        # Handle rate limiting from API
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            raise self.retry(countdown=retry_after)

        response.raise_for_status()
        return {'status': 'success', 'data': response.json()}

    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [400, 401, 403, 404]:
            # Don't retry client errors
            return {'status': 'error', 'code': e.response.status_code}
        raise
```

---

## 3. Configuration Templates

### 3.1 Task Routing Configuration

```python
# config/celery.py
from kombu import Queue

# Define queues
app.conf.task_queues = (
    Queue('default'),
    Queue('high_priority'),
    Queue('low_priority'),
    Queue('emails'),
    Queue('reports'),
    Queue('integrations'),
)

# Default queue
app.conf.task_default_queue = 'default'

# Task routing
app.conf.task_routes = {
    # By task name pattern
    'apps.orders.*': {'queue': 'high_priority'},
    'apps.emails.*': {'queue': 'emails'},
    'apps.reports.*': {'queue': 'low_priority'},
    'apps.integrations.*': {'queue': 'integrations'},

    # By specific task
    'apps.payments.tasks.process_payment': {'queue': 'high_priority'},

    # Wildcard for slow tasks
    '*.generate_report': {'queue': 'reports'},
}
```

### 3.2 Beat Schedule Configuration

```python
# config/celery.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    # Every minute
    'check-pending-orders': {
        'task': 'apps.orders.tasks.check_pending_orders',
        'schedule': 60.0,  # seconds
    },

    # Every hour
    'cleanup-expired-sessions': {
        'task': 'apps.users.tasks.cleanup_sessions',
        'schedule': crontab(minute=0),
    },

    # Daily at 6 AM
    'generate-daily-report': {
        'task': 'apps.reports.tasks.generate_daily_report',
        'schedule': crontab(hour=6, minute=0),
    },

    # Every Monday at 9 AM
    'send-weekly-digest': {
        'task': 'apps.emails.tasks.send_weekly_digest',
        'schedule': crontab(hour=9, minute=0, day_of_week='monday'),
    },

    # First day of month at midnight
    'generate-monthly-report': {
        'task': 'apps.reports.tasks.generate_monthly_report',
        'schedule': crontab(hour=0, minute=0, day_of_month=1),
    },

    # With arguments
    'sync-inventory-hourly': {
        'task': 'apps.inventory.tasks.sync_inventory',
        'schedule': crontab(minute=30),  # Every hour at :30
        'kwargs': {'full_sync': False},
    },
}
```

### 3.3 Production Settings

```python
# config/settings/production.py

# Broker connection pool
CELERY_BROKER_POOL_LIMIT = 10
CELERY_BROKER_CONNECTION_TIMEOUT = 10
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Redis broker specific
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600,  # 1 hour
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
}

# Result backend
CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
}

# Worker settings for production
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000  # Prevent memory leaks

# Task settings
CELERY_TASK_ALWAYS_EAGER = False  # Never in production
CELERY_TASK_STORE_ERRORS_EVEN_IF_IGNORED = True

# Logging
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

# Security - disable pickle
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
```

---

## 4. Testing Templates

### 4.1 Pytest Fixtures

```python
# conftest.py
import pytest


@pytest.fixture(scope='session')
def celery_config():
    """Celery configuration for tests."""
    return {
        'broker_url': 'memory://',
        'result_backend': 'rpc://',
        'task_always_eager': False,
        'task_eager_propagates': True,
    }


@pytest.fixture(scope='session')
def celery_worker_parameters():
    """Celery worker parameters for tests."""
    return {
        'perform_ping_check': False,
        'concurrency': 1,
    }


@pytest.fixture(scope='session')
def celery_includes():
    """Tasks to include in test worker."""
    return [
        'apps.orders.tasks',
        'apps.emails.tasks',
    ]


@pytest.fixture
def celery_eager(settings):
    """Run Celery tasks synchronously."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
    yield


@pytest.fixture
def mock_celery_task():
    """Helper to mock Celery tasks."""
    from unittest.mock import patch, MagicMock

    def _mock_task(task_path):
        mock = MagicMock()
        mock.delay.return_value = MagicMock(id='mock-task-id')
        mock.apply_async.return_value = MagicMock(id='mock-task-id')
        return patch(task_path, mock)

    return _mock_task
```

### 4.2 Unit Test Template

```python
# tests/test_tasks.py
import pytest
from unittest.mock import patch, MagicMock


class TestProcessOrderTask:
    """Tests for process_order task."""

    @patch('apps.orders.tasks.Order.objects.get')
    def test_process_order_success(self, mock_get):
        """Test successful order processing."""
        from apps.orders.tasks import process_order

        # Setup mock
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.status = 'pending'
        mock_get.return_value = mock_order

        # Execute task directly (not async)
        result = process_order(order_id=1)

        # Assertions
        assert result['status'] == 'success'
        mock_get.assert_called_once_with(pk=1)
        mock_order.save.assert_called()

    @patch('apps.orders.tasks.Order.objects.get')
    def test_process_order_not_found(self, mock_get):
        """Test order not found handling."""
        from apps.orders.tasks import process_order
        from django.core.exceptions import ObjectDoesNotExist

        mock_get.side_effect = ObjectDoesNotExist

        result = process_order(order_id=999)

        assert result['status'] == 'error'
        assert result['reason'] == 'not_found'

    @patch('apps.orders.tasks.external_api_call')
    def test_process_order_retry(self, mock_api):
        """Test retry on connection error."""
        from apps.orders.tasks import process_order

        mock_api.side_effect = ConnectionError('API down')

        with pytest.raises(ConnectionError):
            process_order.apply(args=[1]).get()
```

### 4.3 Integration Test Template

```python
# tests/test_tasks_integration.py
import pytest
from django.test import TransactionTestCase


@pytest.mark.usefixtures('celery_session_app', 'celery_session_worker')
class TestCeleryIntegration:
    """Integration tests with actual Celery worker."""

    @pytest.mark.django_db(transaction=True)
    def test_task_execution(self, celery_worker):
        """Test actual async task execution."""
        from apps.orders.tasks import process_order
        from apps.orders.models import Order

        # Create test data
        order = Order.objects.create(status='pending', total=100)

        # Execute async
        result = process_order.delay(order.id)

        # Wait for result
        task_result = result.get(timeout=10)

        assert task_result['status'] == 'success'

        # Verify database changes
        order.refresh_from_db()
        assert order.status == 'processed'

    @pytest.mark.django_db
    def test_task_with_eager_mode(self, celery_eager):
        """Test task with eager mode (synchronous)."""
        from apps.orders.tasks import process_order
        from apps.orders.models import Order

        order = Order.objects.create(status='pending', total=100)

        # Runs synchronously due to eager mode
        result = process_order.delay(order.id)

        assert result.get()['status'] == 'success'
```

### 4.4 Mock Task Delay Template

```python
# tests/test_views.py
import pytest
from unittest.mock import patch


class TestOrderViews:
    """Test views that trigger Celery tasks."""

    @patch('apps.orders.views.process_order.delay')
    def test_create_order_triggers_task(self, mock_delay, client, db):
        """Test that order creation triggers async task."""
        mock_delay.return_value = MagicMock(id='task-123')

        response = client.post('/orders/', {'product_id': 1, 'quantity': 2})

        assert response.status_code == 201
        mock_delay.assert_called_once()
        assert 'task_id' in response.json()

    @patch('apps.orders.views.process_order.delay_on_commit')
    def test_create_order_uses_delay_on_commit(self, mock_delay, client, db):
        """Test that task is called with delay_on_commit."""
        response = client.post('/orders/', {'product_id': 1, 'quantity': 2})

        assert response.status_code == 201
        mock_delay.assert_called_once()
```

---

## 5. Docker Templates

### 5.1 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Redis broker
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Django web application
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      redis:
        condition: service_healthy
      db:
        condition: service_healthy

  # Celery worker (CPU-bound tasks)
  worker:
    build: .
    command: celery -A config worker --pool=prefork --concurrency=4 --loglevel=INFO -Q default,high_priority
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      redis:
        condition: service_healthy
      db:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

  # Celery worker (I/O-bound tasks)
  worker-io:
    build: .
    command: celery -A config worker --pool=gevent --concurrency=100 --loglevel=INFO -Q emails,integrations
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      redis:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G

  # Celery Beat scheduler
  beat:
    build: .
    command: celery -A config beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=INFO
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      redis:
        condition: service_healthy
      db:
        condition: service_healthy

  # Flower monitoring
  flower:
    build: .
    command: celery -A config flower --port=5555 --basic_auth=${FLOWER_USER}:${FLOWER_PASSWORD}
    ports:
      - "5555:5555"
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - CELERY_BROKER_URL=redis://redis:6379/0
      - FLOWER_USER=${FLOWER_USER:-admin}
      - FLOWER_PASSWORD=${FLOWER_PASSWORD:-changeme}
    depends_on:
      - redis

  # PostgreSQL database
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  redis_data:
  postgres_data:
```

### 5.2 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Default command
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 5.3 Development Docker Compose

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  worker:
    build: .
    command: celery -A config worker --loglevel=DEBUG --autoscale=4,1
    volumes:
      - .:/app
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.development
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - redis

  beat:
    build: .
    command: celery -A config beat --loglevel=DEBUG
    volumes:
      - .:/app
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.development
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - redis

  flower:
    build: .
    command: celery -A config flower --port=5555
    ports:
      - "5555:5555"
    volumes:
      - .:/app
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - redis
```

---

## 6. Monitoring Templates

### 6.1 Flower with Prometheus

```yaml
# docker-compose.monitoring.yml
services:
  flower:
    image: mher/flower:latest
    command: celery --broker=${CELERY_BROKER_URL} flower --port=5555 --prometheus_metrics
    ports:
      - "5555:5555"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  prometheus_data:
  grafana_data:
```

### 6.2 Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'celery'
    static_configs:
      - targets: ['flower:5555']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

### 6.3 Task Signal Handlers

```python
# apps/core/signals.py
from celery.signals import task_failure, task_success, task_retry
import logging

logger = logging.getLogger('celery.signals')


@task_failure.connect
def handle_task_failure(sender=None, task_id=None, exception=None, traceback=None, **kwargs):
    """Handle task failures globally."""
    logger.error(
        f"Task {sender.name}[{task_id}] failed: {exception}",
        exc_info=(type(exception), exception, traceback),
    )

    # Send alert to monitoring system
    if should_alert(sender.name):
        send_alert(
            title=f"Celery Task Failed: {sender.name}",
            message=str(exception),
            severity='error',
        )


@task_success.connect
def handle_task_success(sender=None, result=None, **kwargs):
    """Handle successful tasks."""
    logger.info(f"Task {sender.name} completed successfully")


@task_retry.connect
def handle_task_retry(sender=None, reason=None, **kwargs):
    """Handle task retries."""
    logger.warning(f"Task {sender.name} retrying: {reason}")


def should_alert(task_name: str) -> bool:
    """Determine if task failure should trigger alert."""
    critical_tasks = [
        'payments.process_payment',
        'orders.fulfill_order',
    ]
    return task_name in critical_tasks
```

### 6.4 Health Check Endpoint

```python
# apps/core/views.py
from django.http import JsonResponse
from celery import current_app


def celery_health_check(request):
    """Health check endpoint for Celery."""
    try:
        # Check broker connection
        current_app.control.ping(timeout=5)

        # Check active workers
        inspect = current_app.control.inspect()
        active = inspect.active()

        if not active:
            return JsonResponse({
                'status': 'degraded',
                'message': 'No active workers',
            }, status=503)

        return JsonResponse({
            'status': 'healthy',
            'workers': list(active.keys()),
        })

    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
        }, status=503)
```

---

## Quick Reference

### Task Decorator Options

```python
@shared_task(
    name='app.task_name',           # Explicit task name
    bind=True,                       # Pass self (task instance)
    max_retries=3,                   # Maximum retry attempts
    default_retry_delay=60,          # Delay between retries (seconds)
    autoretry_for=(Exception,),      # Auto-retry on these exceptions
    retry_backoff=True,              # Exponential backoff
    retry_backoff_max=600,           # Max backoff delay
    retry_jitter=True,               # Add randomness to backoff
    soft_time_limit=300,             # Soft timeout (raises exception)
    time_limit=360,                  # Hard timeout (kills task)
    rate_limit='10/m',               # Rate limit (10 per minute)
    ignore_result=True,              # Don't store result
    acks_late=True,                  # Acknowledge after completion
)
def my_task(self, arg1, arg2):
    pass
```

### Common Commands

```bash
# Start worker
celery -A config worker --loglevel=INFO

# Start worker with specific queues
celery -A config worker -Q default,high_priority --loglevel=INFO

# Start worker with autoscale
celery -A config worker --autoscale=10,3 --loglevel=INFO

# Start Beat scheduler
celery -A config beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Start Flower
celery -A config flower --port=5555

# Purge all tasks from queues
celery -A config purge

# List active workers
celery -A config inspect active

# List scheduled tasks
celery -A config inspect scheduled
```

---

*Celery 5.4+ | Django 5.x*
