# Monolith Architecture Examples

Real-world examples of monolith architectures across different scales and domains.

## Example 1: E-Commerce Platform (Small Team)

**Context:** 5-person startup building an e-commerce MVP.

### Requirements

- Product catalog (10K products)
- User accounts and authentication
- Shopping cart and checkout
- Order management
- Basic inventory tracking
- Admin dashboard

### Architecture Decision

**Choice:** Traditional monolith with vertical slices

**Rationale:**
- Small team needs to move fast
- Domain is well-understood
- No need for independent scaling
- Simple deployment requirements

### Directory Structure (Django)

```
ecommerce/
    apps/
        users/
            models.py           # User, Address
            views.py            # Registration, profile
            services.py         # User business logic
            tests/

        products/
            models.py           # Product, Category, Variant
            views.py            # Catalog, search
            services.py         # Product management
            tests/

        cart/
            models.py           # Cart, CartItem
            views.py            # Add, remove, update
            services.py         # Cart calculations
            tests/

        orders/
            models.py           # Order, OrderItem
            views.py            # Checkout, order history
            services.py         # Order processing
            events.py           # OrderPlaced, OrderShipped
            tests/

        inventory/
            models.py           # Stock, Warehouse
            views.py            # Stock management
            services.py         # Stock updates
            tests/

        admin/
            views.py            # Admin dashboard
            reports.py          # Sales reports

    core/
        settings/
            base.py
            local.py
            production.py
        urls.py
        middleware.py

    shared/
        utils.py
        exceptions.py
        email.py
```

### Database Schema

```sql
-- Single database, logical grouping by app
CREATE TABLE users_user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products_product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INTEGER REFERENCES products_category(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders_order (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users_user(id),
    status VARCHAR(50) DEFAULT 'pending',
    total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_products_category ON products_product(category_id);
CREATE INDEX idx_orders_user ON orders_order(user_id);
CREATE INDEX idx_orders_status ON orders_order(status);
```

### Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/ecommerce
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7

  celery:
    build: .
    command: celery -A core worker -l info
    depends_on:
      - redis
```

### Scaling Path

1. **Current (1K orders/day):** Single server, PostgreSQL
2. **Growth (10K orders/day):** Add Redis caching, read replica
3. **Scale (100K orders/day):** Horizontal scaling with load balancer

---

## Example 2: SaaS Platform (Medium Team)

**Context:** 20-person company building B2B SaaS for project management.

### Requirements

- Multi-tenant architecture
- Team workspaces
- Projects and tasks
- Real-time collaboration
- Integrations (Slack, GitHub)
- Billing and subscriptions

### Architecture Decision

**Choice:** Modular monolith

**Rationale:**
- Growing team needs clear boundaries
- Future extraction likely for billing
- Some teams work independently
- Still want single deployment simplicity

### Module Structure

```
saas_platform/
    modules/
        identity/                    # Authentication, users, teams
            __init__.py              # Public API
            public/
                api.py               # get_user, create_team, etc.
                events.py            # UserCreated, TeamCreated
                types.py             # UserDTO, TeamDTO
            internal/
                models.py
                services.py
                repository.py
            tests/

        tenancy/                     # Multi-tenant logic
            public/
                api.py               # get_tenant, switch_tenant
                middleware.py        # TenantMiddleware
            internal/
                models.py
                services.py
            tests/

        projects/                    # Core domain
            public/
                api.py
                events.py
            internal/
                models.py
                services.py
                repository.py
            tests/

        billing/                     # Subscription, payments
            public/
                api.py               # create_subscription, process_payment
                webhooks.py          # Stripe webhooks
            internal/
                models.py
                services.py
                stripe_client.py
            tests/

        integrations/                # External services
            public/
                api.py
            internal/
                slack/
                    client.py
                    handlers.py
                github/
                    client.py
                    handlers.py
            tests/

        notifications/               # Email, push, in-app
            public/
                api.py               # send_notification
            internal/
                models.py
                services.py
                channels/
                    email.py
                    push.py
                    websocket.py
            tests/

    infrastructure/
        database.py
        cache.py
        queue.py
        event_bus.py

    api/                             # External API layer
        v1/
            projects.py
            tasks.py
            users.py
        graphql/
            schema.py
```

### Module Communication

```python
# modules/billing/public/api.py
from modules.billing.internal.services import BillingService

_service = BillingService()

def create_subscription(tenant_id: str, plan_id: str) -> SubscriptionDTO:
    """Public API for billing module."""
    return _service.create_subscription(tenant_id, plan_id)

def get_subscription(tenant_id: str) -> SubscriptionDTO:
    """Get current subscription for tenant."""
    return _service.get_subscription(tenant_id)

# modules/projects/internal/services.py
from modules.billing.public.api import get_subscription

class ProjectService:
    def create_project(self, tenant_id: str, name: str) -> Project:
        # Check billing limits via public API
        subscription = get_subscription(tenant_id)
        if subscription.project_limit_reached:
            raise ProjectLimitReached()

        return self._repository.create(tenant_id, name)
```

### Database Schema (Schema-per-Module)

```sql
-- Identity module schema
CREATE SCHEMA identity;

CREATE TABLE identity.users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    tenant_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Projects module schema
CREATE SCHEMA projects;

CREATE TABLE projects.projects (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    owner_id UUID NOT NULL,  -- Reference by ID only, no FK
    created_at TIMESTAMP DEFAULT NOW()
);

-- Billing module schema (candidate for extraction)
CREATE SCHEMA billing;

CREATE TABLE billing.subscriptions (
    id UUID PRIMARY KEY,
    tenant_id UUID UNIQUE NOT NULL,
    plan_id VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    stripe_subscription_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Event-Driven Communication

```python
# infrastructure/event_bus.py
class InMemoryEventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def publish(self, event: DomainEvent):
        for handler in self._handlers.get(event.type, []):
            handler(event)

    def subscribe(self, event_type: str, handler: Callable):
        self._handlers.setdefault(event_type, []).append(handler)

# modules/identity/internal/services.py
class UserService:
    def create_user(self, email: str, password: str) -> User:
        user = User.create(email, password)
        self._repository.save(user)

        # Publish event for other modules
        self._event_bus.publish(UserCreated(
            user_id=user.id,
            email=user.email,
            tenant_id=user.tenant_id
        ))

        return user

# modules/notifications/internal/handlers.py
@event_bus.subscribe("UserCreated")
def on_user_created(event: UserCreated):
    send_notification(
        user_id=event.user_id,
        template="welcome",
        channel="email"
    )
```

---

## Example 3: Fintech Platform (Enterprise)

**Context:** 50-person fintech company with compliance requirements.

### Requirements

- Payment processing
- Account management
- Transaction history
- Compliance and audit logging
- Fraud detection
- Multi-currency support
- High availability (99.99%)

### Architecture Decision

**Choice:** Modular monolith with selective service extraction

**Rationale:**
- Compliance requires audit trails (monolith simplifies)
- Strong consistency for financial transactions
- Fraud detection may need independent scaling
- Team growing, need clear boundaries

### High-Level Architecture

```
                      Load Balancer
                           |
              +------------+------------+
              |                         |
         Main Monolith          Fraud Detection Service
              |                    (extracted for ML scaling)
    +---------+---------+
    |         |         |
 PostgreSQL  Redis    Kafka
 (Primary)  (Cache)  (Events)
    |
 Read Replicas
```

### Module Structure

```
fintech_platform/
    modules/
        accounts/
            public/
                api.py              # create_account, get_balance
                events.py           # AccountCreated, BalanceUpdated
            internal/
                models.py           # Account, Ledger
                services.py
                double_entry.py     # Double-entry bookkeeping

        payments/
            public/
                api.py              # initiate_payment, confirm_payment
                events.py           # PaymentInitiated, PaymentCompleted
            internal/
                models.py           # Payment, PaymentMethod
                services.py
                processors/
                    stripe.py
                    plaid.py

        transactions/
            public/
                api.py              # get_transactions, get_statement
                events.py           # TransactionCreated
            internal/
                models.py           # Transaction, TransactionLine
                services.py
                reporting.py

        compliance/
            public/
                api.py              # check_aml, verify_identity
            internal/
                models.py           # AMLCheck, KYCDocument
                services.py
                providers/
                    jumio.py
                    onfido.py

        audit/
            public/
                api.py              # log_event, get_audit_trail
            internal/
                models.py           # AuditLog
                services.py
                immutable_log.py    # Append-only audit log

        fraud/                      # Extracted to separate service
            public/
                api.py              # check_fraud_risk (calls external service)
            internal/
                client.py           # Fraud service client

    infrastructure/
        database/
            connection.py
            transactions.py         # ACID transaction management
        security/
            encryption.py           # Field-level encryption
            tokenization.py         # PAN tokenization
        compliance/
            pci_dss.py             # PCI DSS utilities
```

### Double-Entry Bookkeeping

```python
# modules/accounts/internal/double_entry.py
from decimal import Decimal
from typing import List
from dataclasses import dataclass

@dataclass
class LedgerEntry:
    account_id: str
    amount: Decimal
    type: str  # 'debit' or 'credit'
    description: str

class DoubleEntryService:
    def transfer(
        self,
        from_account_id: str,
        to_account_id: str,
        amount: Decimal,
        description: str
    ) -> str:
        """Execute double-entry transfer with ACID guarantees."""

        entries = [
            LedgerEntry(from_account_id, amount, 'debit', description),
            LedgerEntry(to_account_id, amount, 'credit', description),
        ]

        # Validate: debits must equal credits
        total_debits = sum(e.amount for e in entries if e.type == 'debit')
        total_credits = sum(e.amount for e in entries if e.type == 'credit')

        if total_debits != total_credits:
            raise BalanceError("Debits must equal credits")

        # Execute in single transaction
        with self._db.transaction():
            transaction_id = self._create_transaction(entries)

            for entry in entries:
                self._update_balance(entry)
                self._record_entry(transaction_id, entry)

            # Audit log (immutable)
            self._audit.log_event(
                event_type="TRANSFER",
                data={"entries": entries, "transaction_id": transaction_id}
            )

        return transaction_id
```

### Audit Logging (Compliance)

```python
# modules/audit/internal/immutable_log.py
import hashlib
import json
from datetime import datetime

class ImmutableAuditLog:
    """Append-only audit log with hash chain for tamper detection."""

    def log_event(
        self,
        event_type: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        data: dict,
        ip_address: str = None
    ) -> AuditEntry:
        # Get previous entry's hash
        previous = self._repository.get_latest()
        previous_hash = previous.hash if previous else "GENESIS"

        # Create new entry
        entry = AuditEntry(
            timestamp=datetime.utcnow(),
            event_type=event_type,
            actor_id=actor_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            data=json.dumps(data),
            ip_address=ip_address,
            previous_hash=previous_hash
        )

        # Calculate hash for chain integrity
        entry.hash = self._calculate_hash(entry)

        # Append only - no updates allowed
        self._repository.append(entry)

        return entry

    def _calculate_hash(self, entry: AuditEntry) -> str:
        content = f"{entry.timestamp}{entry.event_type}{entry.data}{entry.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

    def verify_chain_integrity(self) -> bool:
        """Verify no entries have been tampered with."""
        entries = self._repository.get_all()

        for i, entry in enumerate(entries):
            expected_hash = self._calculate_hash(entry)
            if entry.hash != expected_hash:
                return False

            if i > 0:
                if entry.previous_hash != entries[i-1].hash:
                    return False

        return True
```

---

## Example 4: Content Platform (High Traffic)

**Context:** Media company with 10M monthly active users.

### Requirements

- Article publishing and CMS
- User comments and engagement
- Personalization and recommendations
- High read traffic (100K req/min)
- Moderate write traffic (1K req/min)
- Global audience

### Architecture Decision

**Choice:** Monolith with aggressive caching and CDN

**Rationale:**
- Read-heavy workload perfect for caching
- Content changes infrequently
- Team prefers simplicity
- CDN handles most traffic

### Architecture

```
                        CDN (Cloudflare/CloudFront)
                               |
                        Load Balancer
                               |
              +----------------+----------------+
              |                |                |
          App Server 1    App Server 2    App Server 3
              |                |                |
              +----------------+----------------+
                               |
                         Redis Cluster
                         (Cache Layer)
                               |
                    +----------+----------+
                    |                     |
               PostgreSQL            Elasticsearch
               (Primary)              (Search)
                    |
              Read Replicas
```

### Caching Strategy

```python
# infrastructure/cache.py
class MultiLevelCache:
    """Multi-level caching for high-traffic content platform."""

    def __init__(self, redis_client, local_cache_size=1000):
        self._redis = redis_client
        self._local = LRUCache(local_cache_size)  # In-process cache

    async def get(self, key: str, loader: Callable = None):
        # Level 1: Local in-memory cache
        value = self._local.get(key)
        if value is not None:
            return value

        # Level 2: Redis distributed cache
        value = await self._redis.get(key)
        if value is not None:
            self._local.set(key, value)
            return value

        # Level 3: Database (via loader)
        if loader:
            value = await loader()
            if value is not None:
                await self.set(key, value)
            return value

        return None

    async def set(self, key: str, value: Any, ttl: int = 3600):
        self._local.set(key, value)
        await self._redis.setex(key, ttl, value)

    async def invalidate(self, key: str):
        self._local.delete(key)
        await self._redis.delete(key)

# modules/content/internal/services.py
class ArticleService:
    async def get_article(self, slug: str) -> Article:
        cache_key = f"article:{slug}"

        return await self._cache.get(
            cache_key,
            loader=lambda: self._repository.get_by_slug(slug)
        )

    async def publish_article(self, article_id: str):
        article = await self._repository.get(article_id)
        article.publish()
        await self._repository.save(article)

        # Invalidate caches
        await self._cache.invalidate(f"article:{article.slug}")
        await self._cache.invalidate(f"homepage:articles")

        # Trigger CDN purge
        await self._cdn.purge([
            f"/articles/{article.slug}",
            "/"  # Homepage
        ])
```

### HTTP Caching Headers

```python
# api/articles.py
from fastapi import Response
from fastapi.responses import JSONResponse

@router.get("/articles/{slug}")
async def get_article(slug: str, response: Response):
    article = await article_service.get_article(slug)

    # Cache public content aggressively
    response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=60"
    response.headers["ETag"] = f'"{article.version}"'
    response.headers["Last-Modified"] = article.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT")

    return article

@router.get("/articles/{slug}/comments")
async def get_comments(slug: str, response: Response):
    comments = await comment_service.get_comments(slug)

    # Comments change more frequently
    response.headers["Cache-Control"] = "public, max-age=30"

    return comments
```

---

## Example 5: Internal Business Application

**Context:** Enterprise internal tool for 500 employees.

### Requirements

- Employee directory
- Leave management
- Expense reporting
- Document management
- Approval workflows
- Integration with HR systems

### Architecture Decision

**Choice:** Simple layered monolith

**Rationale:**
- Limited users (500)
- No scaling requirements
- Team wants maintainability
- Budget for enterprise frameworks

### Structure (Spring Boot / Java)

```
internal-app/
    src/main/java/com/company/internal/
        InternalApplication.java

        config/
            SecurityConfig.java
            DatabaseConfig.java
            LdapConfig.java

        employees/
            Employee.java
            EmployeeRepository.java
            EmployeeService.java
            EmployeeController.java
            dto/
                EmployeeDTO.java

        leave/
            LeaveRequest.java
            LeaveBalance.java
            LeaveRepository.java
            LeaveService.java
            LeaveController.java
            workflow/
                LeaveApprovalWorkflow.java

        expenses/
            ExpenseReport.java
            ExpenseLine.java
            ExpenseRepository.java
            ExpenseService.java
            ExpenseController.java
            workflow/
                ExpenseApprovalWorkflow.java

        documents/
            Document.java
            DocumentRepository.java
            DocumentService.java
            DocumentController.java
            storage/
                LocalStorageAdapter.java
                S3StorageAdapter.java

        workflow/
            WorkflowEngine.java
            ApprovalStep.java
            WorkflowDefinition.java

        integration/
            hr/
                HrSystemClient.java
                EmployeeSyncService.java
            ldap/
                LdapAuthenticationProvider.java

        common/
            BaseEntity.java
            AuditListener.java
            exceptions/
                NotFoundException.java
                ValidationException.java
```

### Simple Workflow Engine

```java
// workflow/WorkflowEngine.java
@Service
public class WorkflowEngine {

    public void submitForApproval(Approvable item, WorkflowDefinition workflow) {
        ApprovalStep currentStep = workflow.getFirstStep();

        item.setStatus(ApprovalStatus.PENDING);
        item.setCurrentStep(currentStep);
        item.setApprovers(findApprovers(item, currentStep));

        repository.save(item);

        // Notify approvers
        notificationService.notifyApprovers(
            item.getApprovers(),
            "New item pending approval: " + item.getDescription()
        );
    }

    public void approve(Approvable item, Employee approver, String comment) {
        validateApprover(item, approver);

        ApprovalStep currentStep = item.getCurrentStep();
        item.recordApproval(approver, comment);

        if (currentStep.hasNextStep()) {
            // Move to next step
            ApprovalStep nextStep = currentStep.getNextStep();
            item.setCurrentStep(nextStep);
            item.setApprovers(findApprovers(item, nextStep));

            notificationService.notifyApprovers(item.getApprovers(), "...");
        } else {
            // Workflow complete
            item.setStatus(ApprovalStatus.APPROVED);
            item.complete();

            notificationService.notifyRequester(
                item.getRequester(),
                "Your request has been approved"
            );
        }

        repository.save(item);
    }

    private List<Employee> findApprovers(Approvable item, ApprovalStep step) {
        return switch (step.getApproverType()) {
            case DIRECT_MANAGER -> List.of(item.getRequester().getManager());
            case DEPARTMENT_HEAD -> List.of(item.getRequester().getDepartment().getHead());
            case SPECIFIC_ROLE -> employeeService.findByRole(step.getRequiredRole());
            case CUSTOM -> step.getCustomApproverResolver().resolve(item);
        };
    }
}
```

---

## Anti-Patterns to Avoid

### Big Ball of Mud

**Problem:** No clear structure, everything depends on everything.

```
# BAD: Circular dependencies, no boundaries
from orders import process_order  # orders imports users
from users import get_user        # users imports orders
```

**Solution:** Enforce dependency direction with linting.

### Distributed Monolith

**Problem:** Split into services but still tightly coupled.

```
# BAD: Synchronous calls everywhere, shared database
def create_order(user_id, items):
    user = user_service.get_user(user_id)           # Sync call
    inventory = inventory_service.reserve(items)     # Sync call
    payment = payment_service.charge(user, total)    # Sync call
    # If any fails, complex rollback needed
```

**Solution:** Stay monolith or properly design service boundaries.

### God Module

**Problem:** One module does everything.

```
# BAD: 50 services in one "core" module
core/
    services.py  # 10,000 lines, 50 classes
```

**Solution:** Split by domain, enforce single responsibility.

### Leaky Abstractions

**Problem:** Internal details exposed to other modules.

```python
# BAD: Exposing internal model
from orders.internal.models import Order  # Direct import

# GOOD: Use public API
from orders.public.api import get_order  # Returns DTO
```

---

## Migration Examples

### From Monolith to Modular Monolith

**Before:**
```
app/
    models.py      # All models
    views.py       # All views
    services.py    # All services
```

**After:**
```
app/
    modules/
        users/
            models.py
            views.py
            services.py
        orders/
            models.py
            views.py
            services.py
```

**Steps:**
1. Create module directories
2. Move related code to modules
3. Create public APIs
4. Update imports to use public APIs
5. Add linting rules to enforce boundaries

### From Monolith to Selective Microservices

**Identify extraction candidate:**
- High scaling needs (e.g., image processing)
- Different team ownership
- Technology mismatch (ML in Python, app in Java)

**Strangler fig approach:**
1. Create new service
2. Add API gateway routing
3. Route new traffic to service
4. Gradually migrate existing traffic
5. Remove old code when complete
