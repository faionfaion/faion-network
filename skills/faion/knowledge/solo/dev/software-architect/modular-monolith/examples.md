# Modular Monolith Examples

Real-world case studies, architecture patterns, and implementation examples.

## Industry Case Studies

### Shopify: The Modular Monolith Pioneer

**Context:** One of the largest e-commerce platforms, handling millions of merchants.

**Architecture Evolution:**
1. Started as a Ruby on Rails monolith
2. Evolved into a modular monolith (still mostly monolithic core)
3. Extracted specific services only when necessary (checkout, fraud detection)

**Key Decisions:**
- Maintain monolithic core for rapid development
- Extract only when clear scaling needs arise
- Use microservices for isolated high-load components

**Lessons:**
- Don't over-engineer from the start
- Modular monolith scales further than expected
- Extract services based on data, not assumptions

### GitHub: Ruby Monolith at Scale

**Context:** Millions of developers, billions of requests daily.

**Architecture:**
- Core application remains a Ruby on Rails monolith
- Internal modularization without full microservices
- Some services extracted for specific needs

**Key Practices:**
- Feature flags for gradual rollouts
- Strong code ownership
- Automated testing at scale

**Lessons:**
- Monoliths can scale to massive scale
- Team organization matters more than architecture
- Keep things simple when possible

### Basecamp: Majestic Monolith Philosophy

**Context:** Project management SaaS serving millions of users.

**Architecture:**
- Single Ruby on Rails application
- Minimal external services
- Focus on developer productivity

**Philosophy:**
- "Majestic Monolith" - intentionally monolithic
- Microservices add complexity without proportional benefit
- Single codebase enables faster iteration

**Lessons:**
- Microservices are not always the answer
- Developer experience matters
- Simplicity enables speed

### Amazon Prime Video: Back to Monolith

**Context:** Streaming service quality monitoring tool.

**Migration:**
- Started with microservices architecture
- Moved back to monolithic approach
- Achieved 90% cost reduction

**Reasons:**
- Excessive inter-service communication
- High operational overhead
- No real benefit from distribution

**Lessons:**
- Microservices have real costs
- Evaluate actual needs, not theoretical benefits
- It's okay to go back to simpler architecture

### Kraken Technologies (Octopus Energy): Large Python Monolith

**Context:** Energy platform with ~28,000 Python modules, 400+ developers.

**Architecture:**
- Single Django application
- Strict layering with import-linter
- Modular organization within monolith

**Key Practices:**
- Layered architecture enforced by tooling
- Domain-based module organization
- Continuous boundary enforcement

**Lessons:**
- Tooling is essential at scale
- Layering prevents tangled dependencies
- Large monoliths can work with discipline

## Example 1: E-Commerce Platform (Python/Django)

### Domain Model

```
Bounded Contexts:
├── Users        - Authentication, profiles, addresses
├── Catalog      - Products, categories, search
├── Orders       - Cart, checkout, order management
├── Payments     - Transactions, refunds, payment methods
├── Inventory    - Stock levels, warehouses
└── Notifications - Email, SMS, push notifications
```

### Project Structure

```
ecommerce/
├── shared/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── events.py           # Event bus abstraction
│   └── utils.py
│
├── users/
│   ├── __init__.py         # Public exports
│   ├── api.py              # UserService, UserDTO
│   ├── models.py           # User, Address
│   ├── services.py         # Business logic
│   ├── repository.py       # Data access
│   └── tests/
│
├── catalog/
│   ├── __init__.py
│   ├── api.py              # CatalogService, ProductDTO
│   ├── models.py           # Product, Category
│   ├── search.py           # Search functionality
│   ├── services.py
│   ├── repository.py
│   └── tests/
│
├── orders/
│   ├── __init__.py
│   ├── api.py              # OrderService, OrderDTO
│   ├── models.py           # Order, OrderItem, Cart
│   ├── services.py
│   ├── events.py           # OrderCreated, OrderCompleted
│   ├── handlers.py         # Event handlers
│   ├── repository.py
│   └── tests/
│
├── payments/
│   ├── __init__.py
│   ├── api.py              # PaymentService, PaymentDTO
│   ├── models.py           # Transaction, PaymentMethod
│   ├── services.py
│   ├── gateways/           # Stripe, PayPal adapters
│   ├── handlers.py         # Handle OrderCreated
│   ├── repository.py
│   └── tests/
│
├── inventory/
│   ├── __init__.py
│   ├── api.py
│   ├── models.py           # Stock, Warehouse
│   ├── services.py
│   ├── handlers.py         # Handle OrderCompleted
│   ├── repository.py
│   └── tests/
│
├── notifications/
│   ├── __init__.py
│   ├── api.py
│   ├── services.py
│   ├── channels/           # Email, SMS, Push
│   ├── handlers.py         # Handle various events
│   └── tests/
│
├── config/
│   └── settings.py
│
└── main.py
```

### Module Communication Flow

```
Order Creation Flow:
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Orders  │────>│ Payments │────>│Inventory │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     │ OrderCreated   │ PaymentSuccess │ StockReserved
     │     Event      │     Event      │    Event
     v                v                v
┌──────────────────────────────────────────────┐
│              Notifications Module            │
│  (Sends order confirmation, payment receipt) │
└──────────────────────────────────────────────┘
```

### Database Schema

```sql
-- Each module has its own schema
CREATE SCHEMA users;
CREATE SCHEMA catalog;
CREATE SCHEMA orders;
CREATE SCHEMA payments;
CREATE SCHEMA inventory;

-- Users schema
CREATE TABLE users.accounts (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Orders schema (references user by ID only)
CREATE TABLE orders.orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,  -- No FK to users.accounts
    status VARCHAR(50),
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- No cross-schema foreign keys!
```

## Example 2: SaaS Platform (Go)

### Project Structure

```
saas-platform/
├── cmd/
│   └── main.go              # Application entry point
│
├── internal/
│   ├── shared/
│   │   ├── events/          # Event bus
│   │   ├── errors/          # Common errors
│   │   └── config/          # Configuration
│   │
│   ├── tenants/             # Multi-tenancy module
│   │   ├── api.go           # Public interface
│   │   ├── model.go         # Tenant, Subscription
│   │   ├── service.go       # Business logic
│   │   ├── repository.go    # Data access
│   │   └── handler.go       # HTTP handlers
│   │
│   ├── users/               # User management module
│   │   ├── api.go
│   │   ├── model.go         # User, Role, Permission
│   │   ├── service.go
│   │   ├── repository.go
│   │   └── handler.go
│   │
│   ├── billing/             # Billing module
│   │   ├── api.go
│   │   ├── model.go         # Invoice, Payment
│   │   ├── service.go
│   │   ├── stripe/          # Payment gateway
│   │   ├── events.go        # PaymentReceived, etc.
│   │   ├── repository.go
│   │   └── handler.go
│   │
│   └── analytics/           # Analytics module
│       ├── api.go
│       ├── model.go
│       ├── service.go
│       ├── events.go        # Event handlers
│       ├── repository.go
│       └── handler.go
│
├── pkg/                     # Exportable packages
│   └── client/              # SDK for external use
│
├── migrations/
│   ├── tenants/
│   ├── users/
│   ├── billing/
│   └── analytics/
│
└── docker-compose.yml
```

### Module Interface (Go)

```go
// internal/billing/api.go

package billing

import "context"

// Public interface - what other modules can use
type Service interface {
    CreateInvoice(ctx context.Context, req CreateInvoiceRequest) (*Invoice, error)
    GetInvoice(ctx context.Context, id string) (*Invoice, error)
    ProcessPayment(ctx context.Context, req PaymentRequest) (*PaymentResult, error)
}

// DTOs for cross-module communication
type CreateInvoiceRequest struct {
    TenantID    string
    Amount      int64
    Currency    string
    Description string
}

type Invoice struct {
    ID          string
    TenantID    string
    Amount      int64
    Currency    string
    Status      string
    CreatedAt   time.Time
}

// Events published by this module
type PaymentReceivedEvent struct {
    InvoiceID string
    TenantID  string
    Amount    int64
    Timestamp time.Time
}
```

## Example 3: Financial Platform (Java/Spring)

### Project Structure with Spring Modulith

```
financial-platform/
├── src/main/java/com/example/
│   ├── Application.java
│   │
│   ├── accounts/                    # Accounts module
│   │   ├── package-info.java        # @ApplicationModule
│   │   ├── AccountsApi.java         # Public interface
│   │   ├── internal/
│   │   │   ├── Account.java         # Domain model
│   │   │   ├── AccountService.java  # Business logic
│   │   │   └── AccountRepository.java
│   │   └── AccountsEventPublisher.java
│   │
│   ├── transactions/                # Transactions module
│   │   ├── package-info.java
│   │   ├── TransactionsApi.java
│   │   ├── internal/
│   │   │   ├── Transaction.java
│   │   │   ├── TransactionService.java
│   │   │   └── TransactionRepository.java
│   │   └── TransactionsEventListener.java
│   │
│   ├── risk/                        # Risk assessment module
│   │   ├── package-info.java
│   │   ├── RiskApi.java
│   │   ├── internal/
│   │   │   ├── RiskAssessment.java
│   │   │   ├── RiskService.java
│   │   │   └── FraudDetector.java
│   │   └── RiskEventListener.java
│   │
│   └── notifications/               # Notifications module
│       ├── package-info.java
│       ├── internal/
│       │   ├── NotificationService.java
│       │   └── channels/
│       └── NotificationsEventListener.java
│
└── src/test/java/com/example/
    └── ModularityTests.java         # Verify module boundaries
```

### Spring Modulith Module Definition

```java
// accounts/package-info.java
@org.springframework.modulith.ApplicationModule(
    allowedDependencies = {"shared"}
)
package com.example.accounts;

// accounts/AccountsApi.java
package com.example.accounts;

public interface AccountsApi {
    AccountDto createAccount(CreateAccountRequest request);
    AccountDto getAccount(String accountId);
    void updateBalance(String accountId, BigDecimal amount);
}

// accounts/internal/AccountService.java
package com.example.accounts.internal;

@Service
class AccountService implements AccountsApi {
    // Implementation - not accessible from outside
}
```

### Event-Driven Communication

```java
// accounts/AccountsEventPublisher.java
package com.example.accounts;

@Component
public class AccountsEventPublisher {
    private final ApplicationEventPublisher events;

    public void publishAccountCreated(Account account) {
        events.publishEvent(new AccountCreatedEvent(
            account.getId(),
            account.getOwnerId(),
            Instant.now()
        ));
    }
}

// transactions/TransactionsEventListener.java
package com.example.transactions;

@Component
class TransactionsEventListener {

    @EventListener
    void on(AccountCreatedEvent event) {
        // Initialize transaction history for new account
    }
}
```

## Example 4: Content Platform (Vertical Slice + Modular)

### Combining Vertical Slices with Modules

```
content-platform/
├── shared/
│   ├── mediator/            # MediatR-like request/response
│   └── events/
│
├── articles/                # Articles module
│   ├── __init__.py
│   ├── api.py               # Public API
│   │
│   ├── features/            # Vertical slices
│   │   ├── create_article/
│   │   │   ├── command.py   # CreateArticleCommand
│   │   │   ├── handler.py   # Handle command
│   │   │   ├── validator.py # Validate input
│   │   │   └── endpoint.py  # POST /articles
│   │   │
│   │   ├── get_article/
│   │   │   ├── query.py     # GetArticleQuery
│   │   │   ├── handler.py   # Handle query
│   │   │   └── endpoint.py  # GET /articles/{id}
│   │   │
│   │   ├── publish_article/
│   │   │   ├── command.py
│   │   │   ├── handler.py
│   │   │   └── endpoint.py  # POST /articles/{id}/publish
│   │   │
│   │   └── search_articles/
│   │       ├── query.py
│   │       ├── handler.py
│   │       └── endpoint.py  # GET /articles/search
│   │
│   ├── domain/
│   │   ├── article.py       # Article aggregate
│   │   └── events.py        # ArticlePublished, etc.
│   │
│   └── infrastructure/
│       ├── repository.py
│       └── search_index.py
│
├── authors/                 # Authors module
│   ├── features/
│   │   ├── register_author/
│   │   ├── get_author/
│   │   └── update_profile/
│   ├── domain/
│   └── infrastructure/
│
└── subscriptions/           # Subscriptions module
    ├── features/
    │   ├── subscribe/
    │   ├── unsubscribe/
    │   └── notify_subscribers/
    ├── domain/
    └── infrastructure/
```

### Feature Slice Example

```python
# articles/features/create_article/command.py
from dataclasses import dataclass

@dataclass(frozen=True)
class CreateArticleCommand:
    author_id: str
    title: str
    content: str
    tags: list[str]

# articles/features/create_article/handler.py
from articles.domain.article import Article
from articles.domain.events import ArticleCreatedEvent

class CreateArticleHandler:
    def __init__(self, repository, event_bus, authors_api):
        self.repository = repository
        self.event_bus = event_bus
        self.authors_api = authors_api

    def handle(self, command: CreateArticleCommand) -> str:
        # Validate author exists (via public API)
        author = self.authors_api.get_author(command.author_id)
        if not author:
            raise AuthorNotFoundError(command.author_id)

        # Create article
        article = Article.create(
            author_id=command.author_id,
            title=command.title,
            content=command.content,
            tags=command.tags
        )

        # Persist
        self.repository.save(article)

        # Publish event
        self.event_bus.publish(ArticleCreatedEvent(
            article_id=article.id,
            author_id=article.author_id,
            title=article.title
        ))

        return article.id

# articles/features/create_article/endpoint.py
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/articles")
def create_article(
    request: CreateArticleRequest,
    handler: CreateArticleHandler = Depends()
) -> CreateArticleResponse:
    command = CreateArticleCommand(
        author_id=request.author_id,
        title=request.title,
        content=request.content,
        tags=request.tags
    )
    article_id = handler.handle(command)
    return CreateArticleResponse(article_id=article_id)
```

## Architecture Diagrams

### High-Level Module Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    MODULAR MONOLITH                        │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐ │
│  │   Users   │  │  Catalog  │  │  Orders   │  │ Payments │ │
│  │  Module   │  │  Module   │  │  Module   │  │  Module  │ │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └────┬─────┘ │
│        │              │              │              │       │
│        │    Public    │    API       │    Events   │       │
│        │    APIs      │    Calls     │             │       │
│        │              │              │              │       │
│  ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐  ┌────┴─────┐ │
│  │  Schema   │  │  Schema   │  │  Schema   │  │  Schema  │ │
│  │  users    │  │  catalog  │  │  orders   │  │ payments │ │
│  └───────────┘  └───────────┘  └───────────┘  └──────────┘ │
│        └──────────────┼──────────────┼──────────────┘      │
│                       │              │                      │
│                 ┌─────┴──────────────┴─────┐               │
│                 │     PostgreSQL           │               │
│                 │     (single instance)    │               │
│                 └──────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
                    Single Deployment
```

### Event Flow Diagram

```
                        Event Bus (In-Memory)
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        v                     v                     v
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│    Orders     │     │   Payments    │     │  Inventory    │
│    Module     │     │    Module     │     │    Module     │
└───────┬───────┘     └───────┬───────┘     └───────┬───────┘
        │                     │                     │
        │ 1. OrderCreated     │                     │
        ├─────────────────────>                     │
        │                     │                     │
        │              2. Process Payment           │
        │                     │                     │
        │                     │ 3. PaymentSucceeded │
        │                     ├─────────────────────>
        │                     │                     │
        │                     │              4. Reserve Stock
        │                     │                     │
        │ 5. StockReserved    │                     │
        <─────────────────────┼─────────────────────┤
        │                     │                     │
 6. Update Order Status       │                     │
```

### Migration to Microservices

```
Phase 1: Modular Monolith
┌─────────────────────────┐
│    Modular Monolith     │
│  ┌─────┐ ┌─────┐ ┌────┐ │
│  │Users│ │Order│ │Pay │ │
│  └─────┘ └─────┘ └────┘ │
│          Database       │
└─────────────────────────┘

Phase 2: Extract First Service
┌─────────────────────────┐     ┌───────────────┐
│    Modular Monolith     │     │   Payments    │
│  ┌─────┐ ┌─────┐        │     │   Service     │
│  │Users│ │Order│ <──────┼──── │               │
│  └─────┘ └─────┘   API  │     │   Database    │
│          Database       │     └───────────────┘
└─────────────────────────┘

Phase 3: Continue Extraction
┌─────────────────┐  ┌───────────────┐  ┌───────────────┐
│    Monolith     │  │    Orders     │  │   Payments    │
│  ┌─────┐        │  │   Service     │  │   Service     │
│  │Users│ <──────┼──│               │──│               │
│  └─────┘        │  │   Database    │  │   Database    │
│     Database    │  └───────────────┘  └───────────────┘
└─────────────────┘
        │
        │ Message Queue (Kafka/RabbitMQ)
        └──────────────────────────────────────────────>
```

## Common Patterns Summary

| Pattern | Use Case | Example |
|---------|----------|---------|
| API-First | All cross-module communication | `UserService.get_user(id)` |
| Event Sourcing | Audit trail, temporal queries | `OrderCreatedEvent`, `OrderShippedEvent` |
| CQRS | Complex reads vs writes | Separate read/write models |
| Saga | Distributed transactions | Order -> Payment -> Inventory |
| Outbox | Reliable event publishing | Events persisted before sending |
| Anti-Corruption Layer | Legacy integration | Adapter for old system |
