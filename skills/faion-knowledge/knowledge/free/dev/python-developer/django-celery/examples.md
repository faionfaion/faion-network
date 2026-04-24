# Django Celery Examples

Real-world task implementations and patterns.

## Table of Contents

1. [Email Sending with Retry](#1-email-sending-with-retry)
2. [Report Generation](#2-report-generation)
3. [External API Integration](#3-external-api-integration)
4. [Image Processing](#4-image-processing)
5. [Payment Processing](#5-payment-processing)
6. [Data Synchronization](#6-data-synchronization)
7. [Task Chaining Workflow](#7-task-chaining-workflow)
8. [Parallel Processing with Groups](#8-parallel-processing-with-groups)
9. [Fan-out Notifications](#9-fan-out-notifications)
10. [Rate-Limited API Calls](#10-rate-limited-api-calls)

---

## 1. Email Sending with Retry

### Use Case
Send transactional emails with guaranteed delivery and retry on failure.

### Implementation

```python
# apps/notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name='notifications.send_email',
    bind=True,
    max_retries=5,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    soft_time_limit=30,
    time_limit=60,
)
def send_email_task(
    self,
    recipient_email: str,
    subject: str,
    template_name: str,
    context: dict,
) -> dict:
    """Send email with template rendering.

    Args:
        recipient_email: Recipient email address
        subject: Email subject
        template_name: Path to email template (without extension)
        context: Template context dictionary

    Returns:
        dict: Status and message ID
    """
    try:
        html_content = render_to_string(f'{template_name}.html', context)
        text_content = render_to_string(f'{template_name}.txt', context)

        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_content,
            fail_silently=False,
        )

        logger.info(f"Email sent to {recipient_email}: {subject}")
        return {'status': 'sent', 'recipient': recipient_email}

    except Exception as e:
        logger.error(f"Email failed for {recipient_email}: {e}")
        raise


# Usage with idempotency
@shared_task(name='notifications.send_welcome_email')
def send_welcome_email(user_id: int) -> dict:
    """Send welcome email only once per user."""
    from apps.users.models import User

    user = User.objects.get(pk=user_id)

    # Idempotency check
    if user.welcome_email_sent:
        return {'status': 'skipped', 'reason': 'already_sent'}

    result = send_email_task.delay(
        recipient_email=user.email,
        subject='Welcome to Our Platform!',
        template_name='emails/welcome',
        context={'user': user.get_full_name(), 'login_url': settings.LOGIN_URL},
    )

    # Mark as sent
    user.welcome_email_sent = True
    user.save(update_fields=['welcome_email_sent'])

    return {'status': 'queued', 'task_id': result.id}
```

### Calling from Views

```python
# apps/users/views.py
from django.db import transaction
from apps.notifications.tasks import send_welcome_email


class RegisterView(CreateView):
    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            # Safe within transaction
            send_welcome_email.delay_on_commit(user.id)
        return redirect('registration_complete')
```

---

## 2. Report Generation

### Use Case
Generate large reports asynchronously and notify users when ready.

### Implementation

```python
# apps/reports/tasks.py
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.core.files.base import ContentFile
import csv
import io
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name='reports.generate_sales_report',
    bind=True,
    soft_time_limit=300,  # 5 minutes
    time_limit=360,       # 6 minutes hard limit
)
def generate_sales_report(
    self,
    user_id: int,
    start_date: str,
    end_date: str,
    filters: dict = None,
) -> dict:
    """Generate sales report as CSV.

    Args:
        user_id: User who requested the report
        start_date: Report start date (YYYY-MM-DD)
        end_date: Report end date (YYYY-MM-DD)
        filters: Optional filters (category, region, etc.)

    Returns:
        dict: Report file URL and metadata
    """
    from apps.reports.models import Report
    from apps.orders.models import Order
    from apps.users.models import User
    from datetime import datetime

    try:
        user = User.objects.get(pk=user_id)

        # Create report record
        report = Report.objects.create(
            user=user,
            report_type='sales',
            status='processing',
            parameters={
                'start_date': start_date,
                'end_date': end_date,
                'filters': filters,
            }
        )

        # Update task state for monitoring
        self.update_state(
            state='PROGRESS',
            meta={'report_id': report.id, 'stage': 'querying'}
        )

        # Query data
        queryset = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date,
        )

        if filters:
            if filters.get('category'):
                queryset = queryset.filter(category_id=filters['category'])
            if filters.get('region'):
                queryset = queryset.filter(region=filters['region'])

        # Generate CSV
        self.update_state(
            state='PROGRESS',
            meta={'report_id': report.id, 'stage': 'generating'}
        )

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Order ID', 'Date', 'Customer', 'Amount', 'Status'])

        for order in queryset.select_related('customer').iterator(chunk_size=1000):
            writer.writerow([
                order.id,
                order.created_at.isoformat(),
                order.customer.email,
                str(order.total_amount),
                order.status,
            ])

        # Save file
        filename = f'sales_report_{start_date}_{end_date}.csv'
        report.file.save(filename, ContentFile(output.getvalue().encode('utf-8')))
        report.status = 'completed'
        report.completed_at = datetime.now()
        report.save()

        # Notify user
        from apps.notifications.tasks import send_email_task
        send_email_task.delay(
            recipient_email=user.email,
            subject='Your Sales Report is Ready',
            template_name='emails/report_ready',
            context={
                'report_name': filename,
                'download_url': report.file.url,
            }
        )

        logger.info(f"Report {report.id} generated for user {user_id}")
        return {
            'status': 'completed',
            'report_id': report.id,
            'file_url': report.file.url,
        }

    except SoftTimeLimitExceeded:
        logger.warning(f"Report generation timed out for user {user_id}")
        if report:
            report.status = 'timeout'
            report.save()
        return {'status': 'timeout', 'report_id': report.id if report else None}

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        if report:
            report.status = 'failed'
            report.error_message = str(e)
            report.save()
        raise
```

### Report Model

```python
# apps/reports/models.py
from django.db import models


class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('timeout', 'Timeout'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    parameters = models.JSONField(default=dict)
    file = models.FileField(upload_to='reports/', null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
```

---

## 3. External API Integration

### Use Case
Call external APIs with rate limiting, retries, and circuit breaker pattern.

### Implementation

```python
# apps/integrations/tasks.py
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
import requests
import logging

logger = logging.getLogger(__name__)

# Simple rate limiter using Redis
def check_rate_limit(key: str, max_calls: int, period: int) -> bool:
    """Check if rate limit allows the call."""
    from django.core.cache import cache

    current = cache.get(key, 0)
    if current >= max_calls:
        return False
    cache.set(key, current + 1, timeout=period)
    return True


@shared_task(
    name='integrations.call_payment_gateway',
    bind=True,
    max_retries=3,
    autoretry_for=(requests.exceptions.Timeout, requests.exceptions.ConnectionError),
    retry_backoff=True,
    retry_backoff_max=120,
    retry_jitter=True,
    soft_time_limit=30,
    time_limit=45,
    rate_limit='10/m',  # Max 10 calls per minute
)
def call_payment_gateway(
    self,
    payment_id: int,
    action: str,
    payload: dict,
) -> dict:
    """Call payment gateway API.

    Args:
        payment_id: Internal payment ID
        action: API action (charge, refund, verify)
        payload: Request payload

    Returns:
        dict: Gateway response
    """
    from apps.payments.models import Payment
    from django.conf import settings

    payment = Payment.objects.get(pk=payment_id)

    # Rate limit check
    rate_key = f'payment_gateway_rate_{action}'
    if not check_rate_limit(rate_key, max_calls=100, period=60):
        # Retry later if rate limited
        raise self.retry(countdown=60, exc=Exception('Rate limited'))

    api_url = f'{settings.PAYMENT_GATEWAY_URL}/{action}'

    try:
        response = requests.post(
            api_url,
            json={
                'merchant_id': settings.MERCHANT_ID,
                'payment_reference': payment.external_id,
                **payload,
            },
            headers={
                'Authorization': f'Bearer {settings.PAYMENT_API_KEY}',
                'Content-Type': 'application/json',
            },
            timeout=25,
        )

        if response.status_code == 429:  # Too Many Requests
            retry_after = int(response.headers.get('Retry-After', 60))
            raise self.retry(countdown=retry_after, exc=Exception('Rate limited by gateway'))

        response.raise_for_status()
        result = response.json()

        # Update payment status
        payment.gateway_response = result
        payment.status = result.get('status', 'unknown')
        payment.save()

        logger.info(f"Payment {payment_id} {action}: {result.get('status')}")
        return {'status': 'success', 'gateway_response': result}

    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [400, 401, 403]:
            # Don't retry client errors
            payment.status = 'failed'
            payment.error_message = str(e)
            payment.save()
            logger.error(f"Payment {payment_id} failed: {e}")
            return {'status': 'failed', 'error': str(e)}
        raise

    except MaxRetriesExceededError:
        payment.status = 'failed'
        payment.error_message = 'Max retries exceeded'
        payment.save()
        logger.error(f"Payment {payment_id}: max retries exceeded")
        return {'status': 'failed', 'error': 'max_retries'}
```

---

## 4. Image Processing

### Use Case
Process uploaded images (resize, optimize, generate thumbnails).

### Implementation

```python
# apps/media/tasks.py
from celery import shared_task, group
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

THUMBNAIL_SIZES = {
    'small': (150, 150),
    'medium': (400, 400),
    'large': (800, 800),
}


@shared_task(
    name='media.process_image',
    bind=True,
    soft_time_limit=60,
    time_limit=90,
)
def process_image(self, image_id: int) -> dict:
    """Process uploaded image and generate thumbnails.

    Args:
        image_id: Image record ID

    Returns:
        dict: Processing result with thumbnail URLs
    """
    from apps.media.models import ImageFile
    from django.core.files.base import ContentFile

    try:
        image_record = ImageFile.objects.get(pk=image_id)

        with Image.open(image_record.original.path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Generate thumbnails in parallel
            thumbnail_tasks = []
            for size_name, dimensions in THUMBNAIL_SIZES.items():
                thumbnail_tasks.append(
                    generate_thumbnail.s(image_id, size_name, dimensions)
                )

            # Execute in parallel
            job = group(thumbnail_tasks)
            result = job.apply_async()
            thumbnails = result.get(timeout=60)

            # Optimize original
            optimized = io.BytesIO()
            img.save(optimized, format='JPEG', quality=85, optimize=True)

            image_record.optimized.save(
                f'optimized_{image_record.original.name}',
                ContentFile(optimized.getvalue())
            )
            image_record.status = 'processed'
            image_record.save()

        logger.info(f"Image {image_id} processed with {len(thumbnails)} thumbnails")
        return {
            'status': 'success',
            'thumbnails': thumbnails,
            'optimized_url': image_record.optimized.url,
        }

    except Exception as e:
        logger.error(f"Image processing failed for {image_id}: {e}")
        image_record.status = 'failed'
        image_record.error_message = str(e)
        image_record.save()
        raise


@shared_task(name='media.generate_thumbnail')
def generate_thumbnail(
    image_id: int,
    size_name: str,
    dimensions: tuple,
) -> dict:
    """Generate single thumbnail.

    Args:
        image_id: Image record ID
        size_name: Thumbnail size name (small, medium, large)
        dimensions: (width, height) tuple

    Returns:
        dict: Thumbnail info
    """
    from apps.media.models import ImageFile, Thumbnail
    from django.core.files.base import ContentFile

    image_record = ImageFile.objects.get(pk=image_id)

    with Image.open(image_record.original.path) as img:
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        img.thumbnail(dimensions, Image.Resampling.LANCZOS)

        output = io.BytesIO()
        img.save(output, format='JPEG', quality=80, optimize=True)

        thumbnail = Thumbnail.objects.create(
            image=image_record,
            size_name=size_name,
            width=img.width,
            height=img.height,
        )
        thumbnail.file.save(
            f'{size_name}_{image_record.original.name}',
            ContentFile(output.getvalue())
        )

    return {
        'size': size_name,
        'url': thumbnail.file.url,
        'dimensions': (thumbnail.width, thumbnail.height),
    }
```

---

## 5. Payment Processing

### Use Case
Process payments with exactly-once semantics and status tracking.

### Implementation

```python
# apps/payments/tasks.py
from celery import shared_task
from django.db import transaction
import uuid
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name='payments.process_payment',
    bind=True,
    max_retries=3,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
)
def process_payment(
    self,
    order_id: int,
    payment_method: str,
    idempotency_key: str = None,
) -> dict:
    """Process order payment with idempotency.

    Args:
        order_id: Order ID to process payment for
        payment_method: Payment method (card, paypal, etc.)
        idempotency_key: Unique key for idempotent processing

    Returns:
        dict: Payment result
    """
    from apps.orders.models import Order
    from apps.payments.models import Payment, PaymentLog

    # Generate idempotency key if not provided
    if not idempotency_key:
        idempotency_key = f'payment_{order_id}_{uuid.uuid4()}'

    # Check for existing payment with same idempotency key
    existing = Payment.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        logger.info(f"Idempotent return for payment {existing.id}")
        return {
            'status': existing.status,
            'payment_id': existing.id,
            'idempotent': True,
        }

    with transaction.atomic():
        order = Order.objects.select_for_update().get(pk=order_id)

        # Check if order already paid
        if order.payment_status == 'paid':
            return {'status': 'already_paid', 'order_id': order_id}

        # Create payment record
        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            currency=order.currency,
            payment_method=payment_method,
            idempotency_key=idempotency_key,
            status='pending',
        )

        # Log payment attempt
        PaymentLog.objects.create(
            payment=payment,
            event='created',
            details={'task_id': self.request.id},
        )

    try:
        # Call payment gateway (separate task for isolation)
        from apps.integrations.tasks import call_payment_gateway

        result = call_payment_gateway.apply_async(
            args=[payment.id, 'charge', {'amount': str(payment.amount)}],
        ).get(timeout=45)

        if result['status'] == 'success':
            with transaction.atomic():
                payment.status = 'completed'
                payment.gateway_transaction_id = result['gateway_response'].get('transaction_id')
                payment.save()

                order.payment_status = 'paid'
                order.save()

                PaymentLog.objects.create(
                    payment=payment,
                    event='completed',
                    details=result,
                )

            logger.info(f"Payment {payment.id} completed for order {order_id}")
            return {
                'status': 'success',
                'payment_id': payment.id,
                'transaction_id': payment.gateway_transaction_id,
            }
        else:
            payment.status = 'failed'
            payment.error_message = result.get('error', 'Unknown error')
            payment.save()

            PaymentLog.objects.create(
                payment=payment,
                event='failed',
                details=result,
            )

            return {'status': 'failed', 'payment_id': payment.id, 'error': result.get('error')}

    except Exception as e:
        payment.status = 'error'
        payment.error_message = str(e)
        payment.save()

        PaymentLog.objects.create(
            payment=payment,
            event='error',
            details={'exception': str(e)},
        )

        raise
```

---

## 6. Data Synchronization

### Use Case
Periodic sync of data from external CRM/ERP systems.

### Implementation

```python
# apps/sync/tasks.py
from celery import shared_task
from django.db import transaction
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name='sync.sync_customers_from_crm',
    bind=True,
    soft_time_limit=1800,  # 30 minutes
    time_limit=2100,       # 35 minutes
)
def sync_customers_from_crm(
    self,
    full_sync: bool = False,
    since_hours: int = 24,
) -> dict:
    """Sync customers from external CRM.

    Args:
        full_sync: If True, sync all customers. Otherwise, incremental.
        since_hours: For incremental sync, hours to look back

    Returns:
        dict: Sync statistics
    """
    from apps.customers.models import Customer
    from apps.sync.models import SyncLog
    from apps.integrations.clients import CRMClient

    sync_log = SyncLog.objects.create(
        sync_type='customers',
        status='running',
        started_at=datetime.now(),
    )

    stats = {
        'created': 0,
        'updated': 0,
        'skipped': 0,
        'errors': 0,
    }

    try:
        crm = CRMClient()

        # Get customers to sync
        if full_sync:
            customers = crm.get_all_customers()
        else:
            since = datetime.now() - timedelta(hours=since_hours)
            customers = crm.get_customers_updated_since(since)

        total = len(customers)
        logger.info(f"Syncing {total} customers from CRM")

        for idx, crm_customer in enumerate(customers):
            try:
                # Update progress
                if idx % 100 == 0:
                    self.update_state(
                        state='PROGRESS',
                        meta={
                            'current': idx,
                            'total': total,
                            'stats': stats,
                        }
                    )

                with transaction.atomic():
                    customer, created = Customer.objects.update_or_create(
                        external_id=crm_customer['id'],
                        defaults={
                            'email': crm_customer['email'],
                            'first_name': crm_customer['first_name'],
                            'last_name': crm_customer['last_name'],
                            'phone': crm_customer.get('phone'),
                            'company': crm_customer.get('company'),
                            'crm_synced_at': datetime.now(),
                        }
                    )

                    if created:
                        stats['created'] += 1
                    else:
                        stats['updated'] += 1

            except Exception as e:
                logger.error(f"Error syncing customer {crm_customer['id']}: {e}")
                stats['errors'] += 1

        sync_log.status = 'completed'
        sync_log.completed_at = datetime.now()
        sync_log.stats = stats
        sync_log.save()

        logger.info(f"Customer sync completed: {stats}")
        return {'status': 'completed', 'stats': stats}

    except Exception as e:
        logger.error(f"Customer sync failed: {e}")
        sync_log.status = 'failed'
        sync_log.error_message = str(e)
        sync_log.save()
        raise


# Periodic task configuration
# config/celery.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    'sync-customers-hourly': {
        'task': 'sync.sync_customers_from_crm',
        'schedule': crontab(minute=0),  # Every hour
        'kwargs': {'full_sync': False, 'since_hours': 2},
    },
    'sync-customers-daily-full': {
        'task': 'sync.sync_customers_from_crm',
        'schedule': crontab(hour=3, minute=0),  # 3 AM daily
        'kwargs': {'full_sync': True},
    },
}
```

---

## 7. Task Chaining Workflow

### Use Case
Order processing workflow: validate -> reserve inventory -> charge payment -> send confirmation.

### Implementation

```python
# apps/orders/tasks.py
from celery import shared_task, chain, group


@shared_task(name='orders.validate_order')
def validate_order(order_id: int) -> dict:
    """Validate order data."""
    from apps.orders.models import Order

    order = Order.objects.get(pk=order_id)

    errors = []
    if not order.items.exists():
        errors.append('Order has no items')
    if order.total_amount <= 0:
        errors.append('Invalid total amount')

    if errors:
        order.status = 'validation_failed'
        order.save()
        raise ValueError(f"Validation failed: {errors}")

    order.status = 'validated'
    order.save()
    return {'order_id': order_id, 'status': 'validated'}


@shared_task(name='orders.reserve_inventory')
def reserve_inventory(previous_result: dict) -> dict:
    """Reserve inventory for order items."""
    from apps.orders.models import Order
    from apps.inventory.models import Inventory

    order_id = previous_result['order_id']
    order = Order.objects.get(pk=order_id)

    for item in order.items.all():
        inventory = Inventory.objects.select_for_update().get(product=item.product)
        if inventory.available < item.quantity:
            order.status = 'inventory_failed'
            order.save()
            raise ValueError(f"Insufficient inventory for {item.product.name}")

        inventory.reserved += item.quantity
        inventory.save()

    order.status = 'inventory_reserved'
    order.save()
    return {'order_id': order_id, 'status': 'inventory_reserved'}


@shared_task(name='orders.charge_payment')
def charge_payment(previous_result: dict) -> dict:
    """Process payment for order."""
    from apps.payments.tasks import process_payment

    order_id = previous_result['order_id']
    result = process_payment.apply_async(
        args=[order_id, 'card'],
    ).get(timeout=60)

    if result['status'] != 'success':
        raise ValueError(f"Payment failed: {result.get('error')}")

    return {'order_id': order_id, 'payment_id': result['payment_id'], 'status': 'paid'}


@shared_task(name='orders.send_confirmation')
def send_confirmation(previous_result: dict) -> dict:
    """Send order confirmation email."""
    from apps.orders.models import Order
    from apps.notifications.tasks import send_email_task

    order_id = previous_result['order_id']
    order = Order.objects.get(pk=order_id)

    send_email_task.delay(
        recipient_email=order.customer.email,
        subject=f'Order #{order.number} Confirmed',
        template_name='emails/order_confirmation',
        context={
            'order_number': order.number,
            'total': str(order.total_amount),
            'items': list(order.items.values('product__name', 'quantity', 'price')),
        }
    )

    order.status = 'confirmed'
    order.save()
    return {'order_id': order_id, 'status': 'confirmed'}


@shared_task(name='orders.process_order_workflow')
def process_order_workflow(order_id: int) -> str:
    """Execute full order processing workflow.

    Workflow: validate -> reserve inventory -> charge payment -> send confirmation
    """
    workflow = chain(
        validate_order.s(order_id),
        reserve_inventory.s(),
        charge_payment.s(),
        send_confirmation.s(),
    )

    result = workflow.apply_async()
    return result.id


# Error handling callback
@shared_task(name='orders.handle_workflow_error')
def handle_workflow_error(request, exc, traceback, order_id: int):
    """Handle workflow failures."""
    from apps.orders.models import Order

    order = Order.objects.get(pk=order_id)
    order.status = 'failed'
    order.error_message = str(exc)
    order.save()

    # Notify admin
    logger.error(f"Order {order_id} workflow failed: {exc}")
```

### Calling Workflow

```python
# apps/orders/views.py
def checkout(request, order_id):
    from apps.orders.tasks import process_order_workflow

    # Start async workflow
    task_id = process_order_workflow.delay(order_id)

    return JsonResponse({
        'message': 'Order processing started',
        'task_id': task_id,
    })
```

---

## 8. Parallel Processing with Groups

### Use Case
Process multiple items in parallel and aggregate results.

### Implementation

```python
# apps/analytics/tasks.py
from celery import shared_task, group, chord


@shared_task(name='analytics.calculate_user_metrics')
def calculate_user_metrics(user_id: int) -> dict:
    """Calculate metrics for single user."""
    from apps.users.models import User
    from apps.orders.models import Order
    from django.db.models import Sum, Count

    user = User.objects.get(pk=user_id)

    orders_stats = Order.objects.filter(
        customer=user,
        status='completed',
    ).aggregate(
        total_orders=Count('id'),
        total_spent=Sum('total_amount'),
    )

    return {
        'user_id': user_id,
        'email': user.email,
        'total_orders': orders_stats['total_orders'] or 0,
        'total_spent': float(orders_stats['total_spent'] or 0),
    }


@shared_task(name='analytics.aggregate_user_metrics')
def aggregate_user_metrics(results: list) -> dict:
    """Aggregate metrics from all users."""
    from apps.analytics.models import MetricsSnapshot

    total_revenue = sum(r['total_spent'] for r in results)
    total_orders = sum(r['total_orders'] for r in results)
    active_users = len([r for r in results if r['total_orders'] > 0])

    snapshot = MetricsSnapshot.objects.create(
        total_revenue=total_revenue,
        total_orders=total_orders,
        active_users=active_users,
        user_count=len(results),
    )

    return {
        'snapshot_id': snapshot.id,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'active_users': active_users,
    }


@shared_task(name='analytics.generate_monthly_report')
def generate_monthly_report() -> dict:
    """Generate monthly analytics report using parallel processing."""
    from apps.users.models import User

    # Get all user IDs
    user_ids = list(User.objects.values_list('id', flat=True))

    # Create chord: parallel calculation + aggregation callback
    workflow = chord(
        (calculate_user_metrics.s(user_id) for user_id in user_ids),
        aggregate_user_metrics.s()
    )

    result = workflow.apply_async()
    return {'task_id': result.id, 'user_count': len(user_ids)}
```

---

## 9. Fan-out Notifications

### Use Case
Send notifications to multiple channels (email, SMS, push) in parallel.

### Implementation

```python
# apps/notifications/tasks.py
from celery import shared_task, group


@shared_task(name='notifications.send_email_notification')
def send_email_notification(user_id: int, notification_type: str, data: dict) -> dict:
    """Send email notification."""
    from apps.users.models import User

    user = User.objects.get(pk=user_id)
    if not user.email_notifications_enabled:
        return {'channel': 'email', 'status': 'disabled'}

    # Send email logic...
    return {'channel': 'email', 'status': 'sent'}


@shared_task(name='notifications.send_sms_notification')
def send_sms_notification(user_id: int, notification_type: str, data: dict) -> dict:
    """Send SMS notification."""
    from apps.users.models import User

    user = User.objects.get(pk=user_id)
    if not user.sms_notifications_enabled or not user.phone:
        return {'channel': 'sms', 'status': 'disabled'}

    # Send SMS logic...
    return {'channel': 'sms', 'status': 'sent'}


@shared_task(name='notifications.send_push_notification')
def send_push_notification(user_id: int, notification_type: str, data: dict) -> dict:
    """Send push notification."""
    from apps.users.models import User

    user = User.objects.get(pk=user_id)
    if not user.push_token:
        return {'channel': 'push', 'status': 'no_token'}

    # Send push logic...
    return {'channel': 'push', 'status': 'sent'}


@shared_task(name='notifications.notify_user')
def notify_user(
    user_id: int,
    notification_type: str,
    data: dict,
    channels: list = None,
) -> dict:
    """Send notification to user via all enabled channels.

    Args:
        user_id: User ID
        notification_type: Type of notification (order_confirmed, etc.)
        data: Notification data
        channels: Specific channels to use (default: all)

    Returns:
        dict: Results from each channel
    """
    if channels is None:
        channels = ['email', 'sms', 'push']

    tasks = []

    if 'email' in channels:
        tasks.append(send_email_notification.s(user_id, notification_type, data))
    if 'sms' in channels:
        tasks.append(send_sms_notification.s(user_id, notification_type, data))
    if 'push' in channels:
        tasks.append(send_push_notification.s(user_id, notification_type, data))

    # Execute all in parallel
    job = group(tasks)
    results = job.apply_async().get(timeout=30)

    return {
        'user_id': user_id,
        'notification_type': notification_type,
        'results': results,
    }
```

---

## 10. Rate-Limited API Calls

### Use Case
Call external API with rate limiting to avoid throttling.

### Implementation

```python
# apps/integrations/tasks.py
from celery import shared_task
from celery.exceptions import Retry
import requests
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name='integrations.fetch_product_data',
    bind=True,
    max_retries=5,
    rate_limit='30/m',  # Max 30 tasks per minute
    soft_time_limit=30,
)
def fetch_product_data(self, product_sku: str) -> dict:
    """Fetch product data from external catalog API.

    Rate limited to avoid API throttling.
    """
    from apps.products.models import Product
    from django.conf import settings

    try:
        response = requests.get(
            f'{settings.CATALOG_API_URL}/products/{product_sku}',
            headers={'Authorization': f'Bearer {settings.CATALOG_API_KEY}'},
            timeout=25,
        )

        # Handle rate limiting from API
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            logger.warning(f"Rate limited by API, retrying in {retry_after}s")
            raise self.retry(countdown=retry_after)

        response.raise_for_status()
        data = response.json()

        # Update local product
        Product.objects.filter(sku=product_sku).update(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            external_synced_at=datetime.now(),
        )

        return {'status': 'success', 'sku': product_sku}

    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed for {product_sku}: {e}")
        raise self.retry(exc=e)


@shared_task(name='integrations.sync_all_products')
def sync_all_products() -> dict:
    """Sync all products with rate limiting."""
    from apps.products.models import Product

    skus = list(Product.objects.values_list('sku', flat=True))

    # Queue all tasks - rate_limit will handle throttling
    for sku in skus:
        fetch_product_data.delay(sku)

    return {'status': 'queued', 'count': len(skus)}
```

---

## Summary

| Pattern | Use Case | Key Features |
|---------|----------|--------------|
| **Retry with backoff** | Transient failures | `autoretry_for`, `retry_backoff` |
| **Idempotency** | Duplicate prevention | Check before execute, idempotency keys |
| **Time limits** | Prevent runaway tasks | `soft_time_limit`, `time_limit` |
| **Task chaining** | Sequential workflows | `chain()` primitive |
| **Parallel groups** | Fan-out processing | `group()` primitive |
| **Chords** | Aggregate parallel results | `chord(group, callback)` |
| **Rate limiting** | API throttling | `rate_limit` option |
| **Progress tracking** | Long tasks | `self.update_state()` |

---

*Celery 5.4+ | Django 5.x*
