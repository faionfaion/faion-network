# Django Decision Examples

Real-world decision examples with context, trade-offs, and outcomes.

---

## Example 1: E-Commerce Platform

### Context

- **Project**: B2C e-commerce platform
- **Team**: 5 developers (3 Django experienced)
- **Timeline**: 6 months to MVP
- **Users**: Expected 10k daily active users
- **Budget**: Mid-range startup budget

### Decisions Made

#### Framework Selection

**Decision**: Django with Django REST Framework

**Reasoning**:
- Need admin panel for product/order management
- Team has Django experience
- Complex business logic (pricing, inventory, promotions)
- Need both web templates and API (mobile app planned)

**Alternative Considered**: FastAPI
- Rejected: Would need to build admin from scratch, lose ORM benefits

#### API Framework

**Decision**: Django REST Framework

**Reasoning**:
- Complex nested serializers (orders with items, variants)
- Need ViewSets for standard CRUD operations
- Extensive ecosystem (pagination, filtering, throttling)
- Team already knows DRF

**Alternative Considered**: Django Ninja
- Rejected: Less mature ecosystem for complex serialization

#### Architecture

**Decision**: Service Layer Pattern

**Reasoning**:
- Complex business logic (pricing rules, inventory management)
- Multiple entry points (web, API, admin actions)
- Medium project size (8 apps estimated)

**Structure**:
```
apps/
  products/
    models.py
    services.py      # Product business logic
    views.py
    serializers.py
  orders/
    models.py
    services.py      # Order business logic
    views.py
    serializers.py
  payments/
    services.py      # Payment orchestration
    integrations/    # Stripe, PayPal
```

#### Database

**Decision**: PostgreSQL

**Reasoning**:
- Production-ready from day one
- Need JSONB for product attributes
- Full-text search for product catalog
- Strong Django integration

#### Deployment

**Decision**: DigitalOcean App Platform (PaaS)

**Reasoning**:
- Quick setup, managed PostgreSQL
- Auto-scaling for sales spikes
- Team can focus on features, not infrastructure
- Reasonable cost for traffic level

### Code Organization Example

```python
# apps/orders/services.py
from django.db import transaction
from apps.products import services as product_services
from apps.payments import services as payment_services


@transaction.atomic
def create_order(user, cart_items, shipping_address, payment_method):
    """
    Service function - orchestrates order creation.
    Contains business logic, multiple DB writes.
    """
    # Validate inventory
    for item in cart_items:
        product_services.validate_stock(item.product_id, item.quantity)

    # Create order
    order = Order.objects.create(
        user=user,
        shipping_address=shipping_address,
        status=OrderStatus.PENDING
    )

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.current_price
        )
        product_services.reserve_stock(item.product_id, item.quantity)

    # Process payment
    payment = payment_services.create_payment(
        order=order,
        method=payment_method
    )

    return order
```

### Outcome

- MVP delivered in 5 months
- Successfully handling 15k daily users
- Easy to add new features (subscriptions, gift cards)
- Smooth mobile API integration

---

## Example 2: SaaS Analytics Dashboard

### Context

- **Project**: B2B analytics SaaS
- **Team**: 2 developers (full-stack)
- **Timeline**: 3 months to MVP
- **Users**: 500 business accounts, 5k users
- **Requirements**: Real-time charts, API for integrations

### Decisions Made

#### Framework Selection

**Decision**: Django with Django Ninja

**Reasoning**:
- Need admin for account management
- API-heavy (dashboard fetches data via API)
- Small team values developer experience
- Performance matters for data-heavy endpoints

#### API Framework

**Decision**: Django Ninja

**Reasoning**:
- Type hints catch errors early
- Auto-generated OpenAPI docs for customer API
- Simpler than DRF for this use case
- Better performance for data aggregation endpoints

**Alternative Considered**: DRF
- Rejected: Overkill for mostly read-only API

#### Architecture

**Decision**: Simple (Fat Models) with Query Optimization

**Reasoning**:
- Small project (4 apps)
- Mostly read operations
- 2-person team, need to move fast

**Structure**:
```
apps/
  accounts/
    models.py       # Account, User, Subscription
    views.py        # Admin views
    api.py          # Ninja endpoints
  analytics/
    models.py       # Events, Metrics
    queries.py      # Complex aggregation queries
    api.py          # Data endpoints
  integrations/
    webhooks.py     # Incoming data
```

#### Database

**Decision**: PostgreSQL with read replica

**Reasoning**:
- Complex aggregation queries
- Need materialized views for dashboards
- Read replica offloads analytics queries

#### Deployment

**Decision**: Render (PaaS)

**Reasoning**:
- Simple, fast deployment
- Managed PostgreSQL with read replicas
- Good free tier for development
- Easy preview environments for PRs

### Code Organization Example

```python
# apps/analytics/api.py
from ninja import Router
from typing import List
from datetime import date

from .schemas import MetricResponse, TimeRange
from .queries import get_metrics_for_period


router = Router()


@router.get("/metrics", response=List[MetricResponse])
def get_metrics(
    request,
    account_id: int,
    start_date: date,
    end_date: date,
    granularity: str = "day"
):
    """
    Simple endpoint - mostly query execution.
    Business logic is minimal, delegated to optimized queries.
    """
    return get_metrics_for_period(
        account_id=account_id,
        start_date=start_date,
        end_date=end_date,
        granularity=granularity
    )


# apps/analytics/queries.py
from django.db import connection


def get_metrics_for_period(account_id, start_date, end_date, granularity):
    """
    Optimized query function using raw SQL for performance.
    Separated from API layer for testability.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                date_trunc(%s, event_time) as period,
                COUNT(*) as event_count,
                COUNT(DISTINCT user_id) as unique_users
            FROM analytics_event
            WHERE account_id = %s
              AND event_time BETWEEN %s AND %s
            GROUP BY period
            ORDER BY period
        """, [granularity, account_id, start_date, end_date])

        return [
            {"period": row[0], "events": row[1], "users": row[2]}
            for row in cursor.fetchall()
        ]
```

### Outcome

- MVP in 2.5 months
- API documentation loved by integration partners
- Performance excellent (< 200ms for complex queries)
- Easy to maintain with small team

---

## Example 3: Content Management System

### Context

- **Project**: Multi-tenant CMS for agencies
- **Team**: 4 developers
- **Timeline**: 4 months
- **Users**: 50 agencies, 200 content editors
- **Requirements**: Custom content types, workflows, versioning

### Decisions Made

#### Framework Selection

**Decision**: Django with Wagtail

**Reasoning**:
- CMS is core functionality
- Wagtail provides content editing, workflows, versioning
- Extensible for custom needs
- Django admin for system administration

**Alternative Considered**: Headless CMS (Strapi, Contentful)
- Rejected: Need deep customization, prefer Python stack

#### API Framework

**Decision**: Wagtail API + Django Ninja for custom endpoints

**Reasoning**:
- Wagtail provides content API out of box
- Django Ninja for non-content endpoints (user management, analytics)

#### Architecture

**Decision**: Service Layer with Domain Separation

**Reasoning**:
- Multi-tenant complexity
- Clear separation between content and platform

**Structure**:
```
apps/
  platform/           # Platform-level functionality
    tenants/
      models.py
      services.py     # Tenant provisioning
    users/
      models.py
      services.py     # User management
  content/            # Wagtail content apps
    pages/
      models.py       # Page types
    blocks/
      models.py       # Streamfield blocks
    workflows/
      models.py       # Custom workflows
```

#### Database

**Decision**: PostgreSQL with schema-based multi-tenancy

**Reasoning**:
- Strong tenant isolation
- Efficient query patterns
- Easier backup/restore per tenant

### Code Organization Example

```python
# apps/platform/tenants/services.py
from django.db import connection, transaction
from django.contrib.auth import get_user_model

from .models import Tenant


@transaction.atomic
def provision_tenant(name, admin_email, plan):
    """
    Create new tenant with isolated schema.
    Complex business logic requiring service layer.
    """
    # Create tenant record
    tenant = Tenant.objects.create(
        name=name,
        schema_name=slugify(name),
        plan=plan
    )

    # Create schema
    with connection.cursor() as cursor:
        cursor.execute(f'CREATE SCHEMA "{tenant.schema_name}"')

    # Run migrations for tenant schema
    call_command('migrate_schemas', schema_name=tenant.schema_name)

    # Create admin user
    User = get_user_model()
    admin = User.objects.create_superuser(
        email=admin_email,
        tenant=tenant
    )

    # Send welcome email
    send_welcome_email_task.delay(admin.id)

    return tenant


# apps/content/pages/models.py
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from ..blocks.models import ContentBlocks


class ArticlePage(Page):
    """
    Wagtail page model - content structure definition.
    Business logic in model is acceptable for content types.
    """
    body = StreamField(ContentBlocks, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def get_related_articles(self, limit=3):
        """
        Simple query method on model is fine.
        Complex queries would go to queries.py
        """
        return (
            ArticlePage.objects
            .live()
            .exclude(pk=self.pk)
            .order_by('-first_published_at')[:limit]
        )
```

### Outcome

- Delivered on time with full feature set
- Agencies love the editing experience
- Easy to add new content types
- Clean separation of concerns

---

## Example 4: API-Only Microservice

### Context

- **Project**: Payment processing microservice
- **Team**: 2 backend developers
- **Timeline**: 2 months
- **Requirements**: High reliability, audit logging, multiple payment providers

### Decisions Made

#### Framework Selection

**Decision**: Django (not FastAPI)

**Reasoning**:
- Need Django ORM for transaction records
- Django admin for operations team
- Team prefers Django patterns
- Reliability > raw performance

**Alternative Considered**: FastAPI
- Rejected: Would need to set up ORM, admin, migrations manually

#### API Framework

**Decision**: Django Ninja

**Reasoning**:
- API-only service
- Type hints critical for payment data
- Auto OpenAPI docs for internal documentation
- Performance adequate for payment processing

#### Architecture

**Decision**: Clean Architecture (DDD-inspired)

**Reasoning**:
- Payment processing is complex domain
- Multiple payment providers (Stripe, PayPal, local)
- Need clear boundaries and testability
- Audit requirements demand traceability

**Structure**:
```
apps/
  payments/
    domain/
      entities.py       # Payment, Transaction
      value_objects.py  # Money, Currency
      events.py         # PaymentCreated, PaymentFailed
    application/
      services.py       # ProcessPayment, RefundPayment
      interfaces.py     # PaymentGateway protocol
    infrastructure/
      repositories.py   # PaymentRepository
      gateways/
        stripe.py       # StripeGateway
        paypal.py       # PayPalGateway
    api/
      endpoints.py      # Ninja routes
      schemas.py        # Request/response schemas
```

#### Database

**Decision**: PostgreSQL with strong consistency

**Reasoning**:
- Financial data requires ACID
- Need audit trail
- Complex transaction queries

#### Deployment

**Decision**: Kubernetes (existing company infrastructure)

**Reasoning**:
- Company standard
- Need high availability
- Easy horizontal scaling
- Centralized logging/monitoring

### Code Organization Example

```python
# apps/payments/domain/entities.py
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from datetime import datetime


class PaymentStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


@dataclass
class Payment:
    """Domain entity - pure business logic."""
    id: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    created_at: datetime

    def can_refund(self) -> bool:
        return self.status == PaymentStatus.COMPLETED

    def calculate_refund_amount(self, partial_amount: Decimal | None) -> Decimal:
        if partial_amount and partial_amount < self.amount:
            return partial_amount
        return self.amount


# apps/payments/application/interfaces.py
from typing import Protocol

from ..domain.entities import Payment


class PaymentGateway(Protocol):
    """Interface for payment gateways."""

    def charge(self, amount: Decimal, currency: str, token: str) -> str:
        """Process charge, return gateway transaction ID."""
        ...

    def refund(self, gateway_id: str, amount: Decimal) -> str:
        """Process refund, return gateway refund ID."""
        ...


# apps/payments/application/services.py
from decimal import Decimal
from django.db import transaction

from ..domain.entities import Payment, PaymentStatus
from ..domain.events import PaymentCompleted, PaymentFailed
from .interfaces import PaymentGateway


class PaymentService:
    """Application service - orchestrates payment flow."""

    def __init__(self, gateway: PaymentGateway, repository, event_bus):
        self.gateway = gateway
        self.repository = repository
        self.event_bus = event_bus

    @transaction.atomic
    def process_payment(
        self,
        amount: Decimal,
        currency: str,
        payment_token: str,
        idempotency_key: str
    ) -> Payment:
        # Check idempotency
        existing = self.repository.find_by_idempotency_key(idempotency_key)
        if existing:
            return existing

        # Create payment record
        payment = self.repository.create(
            amount=amount,
            currency=currency,
            status=PaymentStatus.PROCESSING,
            idempotency_key=idempotency_key
        )

        try:
            # Process with gateway
            gateway_id = self.gateway.charge(amount, currency, payment_token)

            # Update payment
            payment = self.repository.update(
                payment.id,
                status=PaymentStatus.COMPLETED,
                gateway_id=gateway_id
            )

            # Emit event
            self.event_bus.publish(PaymentCompleted(payment_id=payment.id))

        except Exception as e:
            payment = self.repository.update(
                payment.id,
                status=PaymentStatus.FAILED,
                error_message=str(e)
            )
            self.event_bus.publish(PaymentFailed(payment_id=payment.id, error=str(e)))
            raise

        return payment
```

### Outcome

- Zero payment processing errors in 6 months
- Easy to add new payment providers
- Excellent test coverage (domain logic is pure)
- Clean audit trail for compliance

---

## Example 5: Startup MVP - Quick and Dirty

### Context

- **Project**: Social fitness app MVP
- **Team**: 1 developer (founder)
- **Timeline**: 1 month
- **Users**: 100 beta users
- **Budget**: Minimal (side project)

### Decisions Made

#### Framework Selection

**Decision**: Django with built-in views

**Reasoning**:
- Solo developer, need to move fast
- Django admin is the back-office
- Familiar with Django

#### API Framework

**Decision**: Django Ninja (simple)

**Reasoning**:
- Auto docs for mobile dev
- Simpler than DRF for small API
- Fast to set up

#### Architecture

**Decision**: Simplest possible (Fat Models)

**Reasoning**:
- 1 developer
- 3 models
- Need to validate idea first
- Can refactor later

**Structure**:
```
myapp/
  models.py       # Everything
  views.py        # Web views
  api.py          # Ninja routes
  admin.py        # Django admin
```

#### Database

**Decision**: SQLite

**Reasoning**:
- Development simplicity
- Single server deployment
- Easy backup (copy file)
- Can migrate to PostgreSQL later

#### Deployment

**Decision**: Fly.io (free tier)

**Reasoning**:
- Free tier sufficient
- Simple deployment
- Easy HTTPS
- Can scale later

### Code Organization Example

```python
# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User with fitness profile."""
    bio = models.TextField(blank=True)
    fitness_level = models.CharField(max_length=20, default='beginner')

    def get_recent_workouts(self, limit=10):
        return self.workouts.order_by('-created_at')[:limit]

    def add_workout(self, workout_type, duration, notes=''):
        """Business logic in model - acceptable for MVP."""
        workout = Workout.objects.create(
            user=self,
            workout_type=workout_type,
            duration=duration,
            notes=notes
        )
        self.update_streak()
        return workout

    def update_streak(self):
        # Simple streak calculation
        from datetime import date, timedelta
        yesterday = date.today() - timedelta(days=1)
        if self.workouts.filter(created_at__date=yesterday).exists():
            self.streak_days += 1
        else:
            self.streak_days = 1
        self.save(update_fields=['streak_days'])


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    workout_type = models.CharField(max_length=50)
    duration = models.IntegerField()  # minutes
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# myapp/api.py
from ninja import NinjaAPI
from .models import User, Workout

api = NinjaAPI()


@api.post("/workouts")
def create_workout(request, workout_type: str, duration: int, notes: str = ''):
    """Simple endpoint - calls model method."""
    workout = request.user.add_workout(workout_type, duration, notes)
    return {"id": workout.id, "streak": request.user.streak_days}
```

### Outcome

- MVP live in 3 weeks
- Validated idea with 100 users
- Easy to understand entire codebase
- Ready to refactor when/if needed

---

## Decision Pattern Summary

| Project Type | Framework | API | Architecture | Database | Deployment |
|--------------|-----------|-----|--------------|----------|------------|
| Enterprise E-commerce | Django | DRF | Service Layer | PostgreSQL | K8s/PaaS |
| SaaS Dashboard | Django | Ninja | Simple + Queries | PostgreSQL | PaaS |
| CMS | Django + Wagtail | Wagtail API | Service Layer | PostgreSQL | VPS/PaaS |
| Payment Service | Django | Ninja | Clean/DDD | PostgreSQL | K8s |
| MVP/Prototype | Django | Ninja/Views | Fat Models | SQLite | PaaS Free |

---

*These examples show that context drives decisions. There's no universal "best" architecture.*
