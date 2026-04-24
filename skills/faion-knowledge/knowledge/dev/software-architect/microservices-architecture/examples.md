# Microservices Architecture Examples

Real-world architecture examples demonstrating microservices patterns.

## Example 1: E-Commerce Platform

### Context

Online retail platform handling:
- 100K+ daily active users
- 10K+ products
- Peak traffic during sales events

### Service Decomposition

```
┌─────────────────────────────────────────────────────────────┐
│                       API Gateway                            │
│                  (Kong / AWS API Gateway)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────────────────┼───────────────────────┐
    │                       │                       │
    ↓                       ↓                       ↓
┌─────────┐           ┌─────────┐           ┌─────────────┐
│ Product │           │  Order  │           │    User     │
│ Service │           │ Service │           │   Service   │
│ (Catalog)│          │         │           │ (Auth/Profile)│
└────┬────┘           └────┬────┘           └──────┬──────┘
     │                     │                       │
     DB                    │                       DB
  (Postgres)          ┌────┴────┐               (Postgres)
                      │         │
                      ↓         ↓
               ┌─────────┐ ┌─────────┐
               │ Payment │ │Inventory│
               │ Service │ │ Service │
               └────┬────┘ └────┬────┘
                    │           │
                    DB          DB
                 (Postgres)  (Redis + Postgres)
```

### Service Responsibilities

| Service | Responsibility | Database | Communication |
|---------|---------------|----------|---------------|
| Product | Catalog, search, categories | PostgreSQL + Elasticsearch | REST (read-heavy) |
| Order | Order lifecycle, cart | PostgreSQL | REST + Events |
| User | Authentication, profiles | PostgreSQL | REST |
| Payment | Transactions, refunds | PostgreSQL | REST + Events |
| Inventory | Stock management | PostgreSQL + Redis | Events (real-time) |
| Notification | Email, SMS, push | - (stateless) | Events only |

### Event Flow: Order Placement

```
1. User places order
   │
   ↓
2. Order Service
   ├── Creates order (status: PENDING)
   ├── Publishes: OrderCreated event
   │
   ↓
3. Payment Service (subscribes to OrderCreated)
   ├── Processes payment
   ├── Publishes: PaymentSucceeded or PaymentFailed
   │
   ↓
4. Inventory Service (subscribes to PaymentSucceeded)
   ├── Reserves stock
   ├── Publishes: InventoryReserved or InventoryInsufficient
   │
   ↓
5. Order Service (subscribes to InventoryReserved)
   ├── Updates order (status: CONFIRMED)
   ├── Publishes: OrderConfirmed
   │
   ↓
6. Notification Service (subscribes to OrderConfirmed)
   └── Sends confirmation email
```

### Saga: Compensation on Failure

```
If InventoryInsufficient:
  │
  ├── Order Service receives event
  ├── Updates order (status: FAILED)
  ├── Publishes: OrderCancelled
  │
  ↓
Payment Service (subscribes to OrderCancelled)
  └── Initiates refund
```

### Technology Stack

| Component | Technology |
|-----------|------------|
| API Gateway | Kong on Kubernetes |
| Service Runtime | Go (high-performance services), Node.js (BFF) |
| Database | PostgreSQL (ACID), Redis (cache) |
| Message Broker | Apache Kafka |
| Search | Elasticsearch |
| Container Orchestration | Kubernetes (EKS) |
| Service Mesh | Linkerd |
| Observability | Prometheus + Grafana + Jaeger |

---

## Example 2: Social Media Platform

### Context

Social platform with:
- 1M+ users
- Real-time feed
- Media uploads
- Notifications

### Service Decomposition

```
                    ┌──────────────┐
                    │ API Gateway  │
                    │   (GraphQL)  │
                    └──────┬───────┘
                           │
    ┌──────────┬───────────┼───────────┬──────────┐
    │          │           │           │          │
    ↓          ↓           ↓           ↓          ↓
┌──────┐  ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
│ User │  │ Post │   │ Feed │   │Media │   │Notif │
│ Svc  │  │ Svc  │   │ Svc  │   │ Svc  │   │ Svc  │
└──┬───┘  └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘
   │         │          │          │          │
   DB        DB      Cache+DB      S3       Redis
(Postgres) (Cassandra) (Redis)           (Pub/Sub)
```

### Feed Generation Pattern

**Fan-out on Write (for users with < 10K followers):**

```
User posts content
       │
       ↓
Post Service creates post
       │
       ├── Stores in Post DB
       └── Publishes: PostCreated
              │
              ↓
Feed Service receives event
       │
       └── Fan-out to follower feeds
           (write to Redis sorted sets)
```

**Fan-out on Read (for celebrities with 10K+ followers):**

```
User requests feed
       │
       ↓
Feed Service
       │
       ├── Gets pre-computed feed (regular users)
       └── Merges with celebrity posts (on-demand)
```

### Notification System

```
Event Sources          Message Queue         Notification Service
─────────────          ─────────────         ────────────────────
PostLiked      ───┐
PostCommented  ───┼──→   Kafka    ───→  Priority Router
UserFollowed   ───┤                           │
PostShared     ───┘                     ┌─────┼─────┐
                                        ↓     ↓     ↓
                                      Push  Email  SMS
                                      (FCM) (SES)  (Twilio)
```

### Technology Stack

| Component | Technology | Reason |
|-----------|------------|--------|
| API Layer | GraphQL (Apollo Federation) | Flexible queries, reduce round trips |
| User Service | PostgreSQL | ACID for user data |
| Post Service | Cassandra | High write throughput, time-series |
| Feed Service | Redis Cluster | Fast sorted set operations |
| Media Service | S3 + CDN | Scalable blob storage |
| Message Broker | Kafka | Event replay, high throughput |
| Real-time | WebSocket (Socket.io) | Live notifications |

---

## Example 3: Fintech Payment System

### Context

Payment processing platform:
- PCI-DSS compliance required
- 99.99% availability SLA
- Sub-second transaction latency

### Service Decomposition

```
                    ┌────────────────────┐
                    │    API Gateway     │
                    │ (Rate Limit + Auth)│
                    └─────────┬──────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ↓                    ↓                    ↓
   ┌───────────┐       ┌───────────┐       ┌───────────┐
   │  Account  │       │Transaction│       │  Ledger   │
   │  Service  │       │  Service  │       │  Service  │
   └─────┬─────┘       └─────┬─────┘       └─────┬─────┘
         │                   │                   │
         DB               Saga                   DB
      (Postgres)       Orchestrator          (Postgres)
                             │                Event Store
                    ┌────────┴────────┐
                    │                 │
                    ↓                 ↓
             ┌───────────┐     ┌───────────┐
             │  Fraud    │     │  External │
             │ Detection │     │ Processor │
             └───────────┘     │  Gateway  │
                               └───────────┘
```

### Transaction Flow (Orchestration Saga)

```
1. Transaction Service receives transfer request
   │
   ↓
2. Saga Orchestrator starts
   │
   ├── Step 1: Fraud Detection Service
   │   └── Validates transaction (ML model)
   │
   ├── Step 2: Account Service
   │   └── Validates balance, places hold
   │
   ├── Step 3: External Processor Gateway
   │   └── Processes with bank/card network
   │
   ├── Step 4: Account Service
   │   └── Commits debit/credit
   │
   └── Step 5: Ledger Service
       └── Records double-entry
```

### Idempotency Pattern

```
Request with idempotency_key
           │
           ↓
    ┌──────────────┐
    │ Check Redis  │
    │ for key      │
    └──────┬───────┘
           │
    ┌──────┴──────┐
    │             │
   Found      Not Found
    │             │
    ↓             ↓
 Return       Process
 cached       transaction
 result            │
                   ↓
              Store result
              in Redis
              (TTL: 24h)
```

### Compliance Architecture

```
┌────────────────────────────────────────────────────────┐
│                   PCI-DSS Boundary                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Cardholder Data Env                 │   │
│  │   ┌──────────┐     ┌──────────────────────┐     │   │
│  │   │  Token   │     │  Card Processor      │     │   │
│  │   │  Vault   │     │  Integration         │     │   │
│  │   └──────────┘     └──────────────────────┘     │   │
│  └─────────────────────────────────────────────────┘   │
│                           │                             │
│                      Tokenized                          │
│                       Access                            │
│                           │                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Non-CDE Services                    │   │
│  │   Transaction, Account, Ledger, Fraud           │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Reason |
|-----------|------------|--------|
| Database | PostgreSQL with synchronous replication | ACID, durability |
| Event Store | EventStoreDB | Event sourcing for audit |
| Saga | Temporal.io | Durable workflow orchestration |
| Caching | Redis Cluster | Idempotency, rate limiting |
| Service Mesh | Istio | mTLS, fine-grained access control |
| Secrets | HashiCorp Vault | PCI-compliant secrets management |

---

## Example 4: Streaming Platform

### Context

Video streaming service:
- Live and on-demand content
- Adaptive bitrate streaming
- Personalized recommendations

### Service Decomposition

```
                         ┌───────────────┐
                         │   CDN Edge    │
                         │  (CloudFront) │
                         └───────┬───────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ↓            ↓            ↓
             ┌───────────┐ ┌─────────┐ ┌───────────┐
             │  Content  │ │  User   │ │  Playback │
             │  Service  │ │ Service │ │  Service  │
             └─────┬─────┘ └────┬────┘ └─────┬─────┘
                   │            │            │
                   │            │            │
    ┌──────────────┼────────────┼────────────┼──────────────┐
    │              │            │            │              │
    ↓              ↓            ↓            ↓              ↓
┌──────┐    ┌──────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐
│Encode│    │  Search  │  │  Reco   │  │Analytics│  │Subscription│
│ Svc  │    │  Service │  │ Service │  │ Service │  │  Service  │
└──┬───┘    └────┬─────┘  └────┬────┘  └────┬────┘  └─────┬────┘
   │             │             │            │             │
 S3 +       Elasticsearch   ML Model    ClickHouse    Stripe
Transcoder                  (Reco)      (Analytics)
```

### Video Ingestion Pipeline

```
Upload Request
      │
      ↓
Content Service
      │
      ├── Stores metadata
      └── Triggers: VideoUploaded event
                         │
                         ↓
              Encode Service (async)
                         │
            ┌────────────┼────────────┐
            │            │            │
            ↓            ↓            ↓
         1080p         720p         480p
        H.264         H.264        H.264
            │            │            │
            └────────────┼────────────┘
                         │
                         ↓
                   HLS Packaging
                         │
                         ↓
                   Upload to S3
                         │
                         ↓
              Publishes: VideoReady event
                         │
                         ↓
              Content Service updates status
```

### Recommendation System

```
User Activity               Real-time Pipeline         ML Service
────────────────           ─────────────────          ──────────
Watch events      ───→     Kafka Streams      ───→   Feature Store
Search queries    ───→     (aggregation)      ───→   (Redis)
Likes/Ratings     ───→                                    │
                                                          ↓
                                               ┌─────────────────┐
                                               │ Recommendation  │
                                               │    Model        │
                                               │ (TensorFlow)    │
                                               └────────┬────────┘
                                                        │
                                                        ↓
                                               Personalized Feed
```

### CDN Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Request                        │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ↓
                    ┌───────────────────────┐
                    │   CDN Edge Location   │
                    │   (Cache Check)       │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                  HIT                     MISS
                    │                       │
                    ↓                       ↓
              Return Video           Origin Shield
              Segment                      │
                                           ↓
                                    ┌──────────────┐
                                    │   S3 Origin  │
                                    └──────────────┘
```

---

## Example 5: SaaS Multi-Tenant Platform

### Context

B2B SaaS application:
- Multi-tenant architecture
- Tenant isolation
- Usage-based billing

### Tenancy Patterns

**Pool Model (Small Tenants):**

```
┌──────────────────────────────────────┐
│           Shared Services            │
├──────────────────────────────────────┤
│  Tenant A  │  Tenant B  │  Tenant C  │
│   (data)   │   (data)   │   (data)   │
└──────────────────────────────────────┘
          Shared Database
       (tenant_id column)
```

**Silo Model (Enterprise Tenants):**

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Tenant X    │  │  Tenant Y    │  │  Tenant Z    │
│  (dedicated) │  │  (dedicated) │  │  (dedicated) │
├──────────────┤  ├──────────────┤  ├──────────────┤
│   Database   │  │   Database   │  │   Database   │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Service Architecture

```
                    ┌────────────────────┐
                    │    API Gateway     │
                    │ (Tenant Resolution)│
                    └─────────┬──────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Tenant Context  │
                    │    Middleware     │
                    └─────────┬─────────┘
                              │
    ┌─────────────────────────┼─────────────────────────┐
    │                         │                         │
    ↓                         ↓                         ↓
┌─────────┐             ┌─────────┐             ┌─────────┐
│  Core   │             │ Billing │             │  Admin  │
│ Service │             │ Service │             │ Service │
└────┬────┘             └────┬────┘             └────┬────┘
     │                       │                       │
     ↓                       ↓                       ↓
  Tenant                 Stripe +                 Tenant
  Data DB               Usage DB                Config DB
```

### Tenant Routing

```
Request: api.saas.com/v1/projects
Headers: X-Tenant-ID: tenant-123 (or from JWT)
         │
         ↓
┌──────────────────────────────┐
│      API Gateway             │
│  1. Extract tenant context   │
│  2. Validate tenant          │
│  3. Route to appropriate     │
│     service/database         │
└──────────────────────────────┘
         │
         ├── Pool tenant → Shared DB (WHERE tenant_id = ?)
         └── Silo tenant → Dedicated DB (connection string)
```

### Usage-Based Billing

```
User Action                Metering Service         Billing Service
───────────                ────────────────         ───────────────
API Call      ───→         Log to Kafka     ───→   Aggregate
Storage Use   ───→         (real-time)             (hourly)
Compute Time  ───→                                     │
                                                       ↓
                                               ┌──────────────┐
                                               │ Usage Record │
                                               │   Database   │
                                               └──────┬───────┘
                                                      │
                                               End of billing
                                                  period
                                                      │
                                                      ↓
                                               Generate Invoice
                                               (Stripe Integration)
```

---

## Key Patterns Summary

| Pattern | Used In | Purpose |
|---------|---------|---------|
| Event-driven saga | E-commerce, Fintech | Distributed transactions |
| Fan-out | Social media | Feed generation |
| CQRS | All examples | Scale reads/writes independently |
| Sidecar | All examples | Cross-cutting concerns |
| Idempotency | Fintech | Exactly-once processing |
| Multi-tenancy | SaaS | Tenant isolation |
| CDN + Origin Shield | Streaming | Global content delivery |

## Related Files

- [README.md](README.md) - Architecture overview
- [checklist.md](checklist.md) - Implementation checklist
- [templates.md](templates.md) - Code templates
- [llm-prompts.md](llm-prompts.md) - Design prompts
