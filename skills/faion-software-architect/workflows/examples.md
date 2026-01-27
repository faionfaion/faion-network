# Architecture Workflow Examples

Real-world examples of architecture workflows in action.

## Table of Contents

1. [System Design: URL Shortener](#1-system-design-url-shortener)
2. [System Design: Real-time Chat System](#2-system-design-real-time-chat-system)
3. [Architecture Review: E-commerce Platform](#3-architecture-review-e-commerce-platform)
4. [ADR: Database Selection](#4-adr-database-selection)
5. [Technology Evaluation: Message Queue](#5-technology-evaluation-message-queue)
6. [ATAM Assessment: FinTech Platform](#6-atam-assessment-fintech-platform)
7. [Migration: Monolith to Microservices](#7-migration-monolith-to-microservices)

---

## 1. System Design: URL Shortener

### Context
Design a URL shortening service like bit.ly.

### Step 1: Requirements Clarification

**Functional Requirements:**
- Shorten long URLs to short links
- Redirect short links to original URLs
- Custom aliases (optional)
- Analytics (click tracking)
- Link expiration (optional)

**Non-Functional Requirements:**
- High availability (99.99%)
- Low latency (<100ms for redirects)
- Eventual consistency acceptable
- 100M URLs created/month
- 10:1 read to write ratio

**Constraints:**
- Short URLs should be 7-8 characters
- Links valid for 5 years by default

### Step 2: Scale Estimation

```
URLs created: 100M/month = ~40/second
Redirects: 40 * 10 = 400/second
Peak: 400 * 5 = 2000 RPS

Storage (5 years):
- 100M * 12 * 5 = 6 billion URLs
- Per record: ~500 bytes (URL + metadata)
- Total: 6B * 500B = 3 TB

Bandwidth:
- Write: 40 * 500B = 20 KB/s
- Read: 400 * 500B = 200 KB/s
```

### Step 3: High-Level Design

```
                    ┌─────────────┐
                    │   Client    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    CDN      │
                    │  (caching)  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    Load     │
                    │  Balancer   │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │   API       │ │   API       │ │   API       │
    │  Server 1   │ │  Server 2   │ │  Server 3   │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    ┌──────▼──────┐
                    │   Cache     │
                    │   (Redis)   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Database   │
                    │ (Cassandra) │
                    └─────────────┘
```

### Step 4: Component Deep Dive

**Key Generation Service:**
```python
# Base62 encoding (a-z, A-Z, 0-9)
# 7 characters = 62^7 = 3.5 trillion combinations

import hashlib
import base64

def generate_short_url(long_url: str, counter: int) -> str:
    """Generate unique short URL using MD5 + counter"""
    hash_input = f"{long_url}:{counter}"
    hash_bytes = hashlib.md5(hash_input.encode()).digest()
    base62 = base64.b64encode(hash_bytes).decode()
    return base62[:7].replace('+', 'a').replace('/', 'b')
```

**Database Schema (Cassandra):**
```sql
CREATE TABLE urls (
    short_url TEXT PRIMARY KEY,
    original_url TEXT,
    user_id UUID,
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    click_count COUNTER
);

CREATE TABLE url_analytics (
    short_url TEXT,
    clicked_at TIMESTAMP,
    user_agent TEXT,
    ip_address TEXT,
    referer TEXT,
    PRIMARY KEY (short_url, clicked_at)
) WITH CLUSTERING ORDER BY (clicked_at DESC);
```

### Step 5: Trade-offs

| Decision | Trade-off |
|----------|-----------|
| Cassandra vs PostgreSQL | Availability over strong consistency |
| Base62 vs UUID | Shorter URLs vs guaranteed uniqueness |
| Counter service vs random | Predictable vs unpredictable |
| Redis cache | Memory cost vs latency reduction |

### Key ADR: Why Cassandra?

**Context:** Need to store 6B URLs with high availability.

**Decision:** Use Cassandra.

**Rationale:**
- Linear scalability
- High write throughput
- Tunable consistency
- Built-in replication

**Consequences:**
- No complex queries
- Eventually consistent reads
- Operational complexity

---

## 2. System Design: Real-time Chat System

### Context
Design a chat system like Slack or Discord.

### Requirements

**Functional:**
- 1:1 messaging
- Group chats (up to 1000 members)
- Online/offline status
- Message history
- Push notifications

**Non-Functional:**
- Real-time delivery (<100ms)
- Message ordering guaranteed
- 99.9% availability
- 50M DAU

### Scale Estimation

```
Messages: 50M DAU * 50 messages/day = 2.5B/day
Peak: 2.5B / 86400 * 5 = ~145K messages/second

Storage:
- 2.5B * 365 * 100B = 91 TB/year
- Keep 2 years = 182 TB

Connections:
- 50M DAU, 20% concurrent = 10M WebSocket connections
```

### High-Level Design

```
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│ Client  │────▶│   Gateway   │────▶│  Chat       │
│         │◀────│  (WebSocket)│◀────│  Service    │
└─────────┘     └─────────────┘     └──────┬──────┘
                                           │
                       ┌───────────────────┼───────────────────┐
                       │                   │                   │
                ┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
                │   Kafka     │     │  User       │     │  Message    │
                │  (messages) │     │  Service    │     │  Store      │
                └─────────────┘     └─────────────┘     └─────────────┘
```

### Message Flow

```
1. User A sends message to Group G
2. Gateway receives via WebSocket
3. Chat Service:
   - Validates user membership
   - Publishes to Kafka topic (group-G)
   - Stores in Message Store
4. Kafka distributes to all Gateway instances
5. Gateways push to connected members of Group G
6. Offline members: Push notification via Firebase/APNs
```

### Key Components

**Connection Manager:**
```python
class ConnectionManager:
    def __init__(self):
        self.user_connections: dict[str, WebSocket] = {}
        self.group_members: dict[str, set[str]] = {}

    async def send_to_group(self, group_id: str, message: dict):
        members = self.group_members.get(group_id, set())
        for user_id in members:
            if user_id in self.user_connections:
                await self.user_connections[user_id].send_json(message)
```

**Message Ordering:**
- Kafka partitions by conversation_id
- Single partition = ordered delivery
- Message ID: timestamp + server_id + sequence

---

## 3. Architecture Review: E-commerce Platform

### Context
Reviewing architecture of a growing e-commerce platform experiencing scaling issues.

### Current Architecture Analysis

**Components Identified:**
- Monolithic Django application
- PostgreSQL database (single primary)
- Redis for sessions
- Celery for async tasks
- Nginx reverse proxy

**Pain Points Reported:**
- Checkout timeouts during sales
- Search is slow (5-10 seconds)
- Deploys take 2 hours
- Database CPU at 90%

### Risk-Storming Results

| Risk | Severity | Area |
|------|----------|------|
| Single database failure | Critical | Database |
| No read replicas | High | Database |
| Monolith scaling | High | Application |
| No caching strategy | Medium | Performance |
| Sync search queries | Medium | Search |

### Quality Attribute Assessment

**Performance:**
- [ ] p95 latency: 2.5s (target: 500ms)
- [ ] Database queries: 50+ per page
- [ ] No query optimization

**Scalability:**
- [ ] Vertical scaling only
- [ ] No horizontal scaling strategy
- [ ] Database is bottleneck

**Availability:**
- [ ] No redundancy
- [ ] Single point of failure (DB)
- [ ] No failover plan

### Recommendations

**Immediate (0-30 days):**
1. Add PostgreSQL read replicas
2. Implement database query caching
3. Add application-level caching (Redis)

**Short-term (1-3 months):**
1. Extract search to Elasticsearch
2. Extract payment processing to separate service
3. Implement proper connection pooling

**Long-term (3-6 months):**
1. Decompose monolith (start with catalog, order, user services)
2. Implement event-driven architecture
3. Add proper observability

### Review Report Summary

```markdown
## Architecture Review: E-commerce Platform
Date: 2025-01-25
Reviewers: Architecture Team

### Overall Assessment: NEEDS IMPROVEMENT

### Critical Issues (Must Fix)
1. Single database is SPOF
2. No horizontal scaling capability
3. Checkout service tightly coupled

### Key Recommendations
1. Database: Add read replicas, implement caching
2. Search: Extract to Elasticsearch
3. Architecture: Begin service extraction

### Risk Summary
- Critical: 1
- High: 2
- Medium: 3

### Follow-up
- Next review: 30 days
- Owner: Platform Team
```

---

## 4. ADR: Database Selection

### ADR-015: Primary Database for User Service

**Status:** Accepted

**Date:** 2025-01-15

**Context:**
We are building a new User Service that will handle authentication, authorization, and user profile management. The service will support:
- 10M users initially, growing to 100M
- 1000 RPS read, 100 RPS write
- Strong consistency for auth operations
- Complex queries for user search

**Decision Drivers:**
- Strong consistency required for auth
- Complex queries needed
- Team has PostgreSQL experience
- Budget constraints

**Considered Options:**

| Option | Pros | Cons |
|--------|------|------|
| PostgreSQL | ACID, rich queries, team experience | Scaling complexity |
| MongoDB | Flexible schema, easy scaling | Weaker consistency |
| CockroachDB | Distributed SQL, strong consistency | Higher cost, complexity |

**Decision:**
PostgreSQL with read replicas.

**Rationale:**
- Team already experienced with PostgreSQL
- Strong consistency for auth operations
- Rich query support for user search
- Read replicas handle read scaling
- Connection pooling (PgBouncer) for write scaling
- Can migrate to CockroachDB later if needed

**Consequences:**

*Positive:*
- Immediate team productivity
- Strong consistency guaranteed
- Rich ecosystem (extensions, tools)

*Negative:*
- Write scaling limited to vertical
- Need to manage read replicas
- May need sharding at 100M+ users

**Compliance:**
- GDPR: Supports encryption at rest
- SOC2: Audit logging available

**Follow-up:**
- Review at 50M users
- Evaluate CockroachDB for migration

---

## 5. Technology Evaluation: Message Queue

### Context
Selecting a message queue for event-driven microservices architecture.

### Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Throughput | 25% | Messages per second |
| Durability | 25% | Message persistence |
| Ordering | 20% | Message order guarantee |
| Operations | 15% | Ease of operation |
| Cost | 15% | Total cost of ownership |

### Candidates Evaluated

1. **Apache Kafka**
2. **RabbitMQ**
3. **Amazon SQS/SNS**
4. **Redis Streams**

### Scoring Matrix

| Criterion | Weight | Kafka | RabbitMQ | SQS/SNS | Redis |
|-----------|--------|-------|----------|---------|-------|
| Throughput | 25% | 5 | 3 | 4 | 4 |
| Durability | 25% | 5 | 4 | 5 | 3 |
| Ordering | 20% | 5 | 4 | 3 | 4 |
| Operations | 15% | 2 | 4 | 5 | 3 |
| Cost | 15% | 3 | 4 | 4 | 5 |
| **Total** | 100% | **4.15** | **3.7** | **4.1** | **3.7** |

### POC Results

**Test Scenario:** 100K messages/second sustained throughput

| System | Achieved | Latency p99 | Notes |
|--------|----------|-------------|-------|
| Kafka | 150K/s | 15ms | Exceeded requirements |
| RabbitMQ | 50K/s | 25ms | Below requirements |
| SQS | 100K/s | 50ms | Met requirements |
| Redis | 200K/s | 5ms | Exceeded, but durability concerns |

### Decision

**Selected: Apache Kafka**

**Rationale:**
- Highest throughput and durability
- Strong ordering guarantees (per partition)
- Replay capability for debugging
- Industry standard for event streaming

**Trade-offs Accepted:**
- Higher operational complexity
- Steeper learning curve
- Need Kafka expertise

**Mitigation:**
- Use managed Kafka (Confluent Cloud) initially
- Train team over 3 months
- Create runbooks for common operations

---

## 6. ATAM Assessment: FinTech Platform

### Context
Formal ATAM assessment of a payment processing platform.

### Business Drivers

1. Process $1B transactions/year
2. 99.99% availability requirement
3. PCI-DSS compliance mandatory
4. Expand to 5 new markets in 12 months

### Quality Attribute Utility Tree

```
Quality Attributes
├── Performance
│   ├── Transaction processing < 200ms (H, H)
│   └── Dashboard queries < 2s (M, M)
├── Availability
│   ├── Core payment: 99.99% (H, H)
│   └── Reporting: 99.9% (M, L)
├── Security
│   ├── PCI-DSS compliance (H, H)
│   └── Fraud detection < 100ms (H, M)
├── Scalability
│   ├── Handle 10x traffic spikes (H, M)
│   └── Add new payment methods (M, H)
└── Modifiability
    ├── Add new market < 2 weeks (H, M)
    └── Update compliance rules < 1 day (M, H)

(Importance, Difficulty)
```

### Sensitivity Points Identified

| ID | Point | Quality Attribute | Description |
|----|-------|-------------------|-------------|
| S1 | Database replication | Availability | Single region DB is SPOF |
| S2 | Payment gateway | Performance | External API latency variable |
| S3 | Encryption overhead | Performance | PCI encryption adds 10ms |

### Trade-off Points Identified

| ID | Trade-off | Attributes | Description |
|----|-----------|------------|-------------|
| T1 | Sync vs Async payment | Performance vs Consistency | Async faster but eventual |
| T2 | Multi-region | Availability vs Cost | 3x infra cost for 99.99% |
| T3 | Real-time fraud | Security vs Performance | ML inference adds latency |

### Risks Identified

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R1 | Single region failure | Critical | Multi-region deployment |
| R2 | Payment gateway timeout | High | Circuit breaker + fallback |
| R3 | Compliance lag | High | Automated compliance testing |

### Recommendations

1. **Multi-region Deployment (Critical)**
   - Deploy to 2+ regions
   - Implement active-active or active-passive
   - Cost: ~$200K/year additional

2. **Circuit Breaker for External APIs (High)**
   - Implement circuit breaker pattern
   - Add fallback payment providers
   - Effort: 2 sprints

3. **Automated Compliance Pipeline (High)**
   - CI/CD compliance checks
   - Automated PCI scanning
   - Effort: 3 sprints

---

## 7. Migration: Monolith to Microservices

### Context
E-commerce monolith (500K LOC, Django) experiencing scaling issues. Using Strangler Fig pattern for incremental migration.

### Current State Assessment

**Monolith Components:**
- User management
- Product catalog
- Shopping cart
- Order processing
- Payment processing
- Inventory management
- Notification service
- Reporting

**Pain Points:**
- Deploy takes 4 hours
- Entire system down during deploys
- Can't scale catalog independently
- Team conflicts on shared codebase

### Migration Priority Matrix

| Component | Business Value | Technical Risk | Dependencies | Priority |
|-----------|---------------|----------------|--------------|----------|
| Notification | Low | Low | None | 1 (First) |
| Product Catalog | High | Medium | Inventory | 2 |
| User Management | High | High | All | 3 |
| Shopping Cart | Medium | Medium | Catalog, User | 4 |
| Order Processing | High | High | Cart, Payment | 5 |
| Payment | High | Critical | Order | 6 (Last) |

### Phase 1: Notification Service (Week 1-4)

**Why Start Here:**
- Low risk (not customer-facing)
- No dependencies
- Good learning opportunity

**Implementation:**

```
Week 1: Setup
- Create notification-service repo
- Set up CI/CD
- Define API contract

Week 2: Build
- Implement email/SMS/push handlers
- Add Kafka consumer
- Write tests

Week 3: Deploy
- Deploy to staging
- Set up routing proxy
- Parallel running with monolith

Week 4: Cutover
- Route 10% traffic to new service
- Monitor metrics
- Gradually increase to 100%
- Decommission monolith notification code
```

**Routing Configuration (Kong):**

```yaml
services:
  - name: notifications
    url: http://notification-service:8000
    routes:
      - name: notifications-route
        paths:
          - /api/v1/notifications
        plugins:
          - name: canary
            config:
              percentage: 10  # Start with 10%
              upstream_host: notification-service:8000
              fallback_host: monolith:8000
```

### Phase 2: Product Catalog (Week 5-12)

**Data Migration Strategy:**

```python
# CDC with Debezium
# 1. Set up Debezium connector for PostgreSQL
# 2. Stream changes to Kafka
# 3. New service consumes and builds its own DB

# Debezium connector config
{
    "name": "products-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": "monolith-db",
        "database.port": "5432",
        "database.user": "debezium",
        "database.password": "${secrets.db_password}",
        "database.dbname": "ecommerce",
        "table.include.list": "public.products,public.categories",
        "topic.prefix": "ecommerce",
        "plugin.name": "pgoutput"
    }
}
```

**Dual-Write Pattern:**

```python
class ProductService:
    def update_product(self, product_id: str, data: dict):
        # Write to both systems during migration

        # 1. Write to monolith (source of truth)
        self.monolith_client.update_product(product_id, data)

        # 2. Write to new service (shadow)
        try:
            self.catalog_service.update_product(product_id, data)
        except Exception as e:
            # Log but don't fail - monolith is still authoritative
            logger.error(f"Shadow write failed: {e}")
            metrics.increment("catalog.shadow_write.failure")
```

### Validation Strategy

**Comparison Testing:**

```python
import asyncio
from dataclasses import dataclass

@dataclass
class ComparisonResult:
    match: bool
    monolith_response: dict
    service_response: dict
    differences: list

async def compare_responses(endpoint: str, params: dict) -> ComparisonResult:
    """Compare responses from monolith and new service"""

    monolith_task = fetch(f"http://monolith{endpoint}", params)
    service_task = fetch(f"http://catalog-service{endpoint}", params)

    monolith_resp, service_resp = await asyncio.gather(
        monolith_task, service_task
    )

    differences = find_differences(monolith_resp, service_resp)

    return ComparisonResult(
        match=len(differences) == 0,
        monolith_response=monolith_resp,
        service_response=service_resp,
        differences=differences
    )
```

### Migration Progress Dashboard

```
┌─────────────────────────────────────────────────────────┐
│           Monolith Migration Progress                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Notification    [████████████████████] 100%  ✓        │
│  Catalog         [██████████░░░░░░░░░░]  50%  →        │
│  User Management [░░░░░░░░░░░░░░░░░░░░]   0%           │
│  Shopping Cart   [░░░░░░░░░░░░░░░░░░░░]   0%           │
│  Order           [░░░░░░░░░░░░░░░░░░░░]   0%           │
│  Payment         [░░░░░░░░░░░░░░░░░░░░]   0%           │
│                                                         │
│  Overall: 25% complete                                  │
│  Estimated completion: Q3 2025                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Lessons Learned

1. **Start with low-risk, low-dependency services**
2. **Invest in observability early**
3. **Dual-write period longer than expected**
4. **Feature flags essential for gradual rollout**
5. **Team needed more training on distributed systems**

---

*Part of faion-software-architect skill*
