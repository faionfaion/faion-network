# Quality Attributes Examples

Real-world implementations of quality attribute requirements across different system types.

---

## Example 1: E-commerce Platform

### System Context

- **Type:** B2C e-commerce with payments
- **Users:** 500K monthly active users
- **Peak:** Black Friday (10x normal traffic)
- **Compliance:** PCI-DSS for payment processing

### Quality Attribute Scenarios

#### Performance Scenario

```
Source:        End user
Stimulus:      Searches for products with filters
Environment:   Normal operations (50K concurrent users)
Artifact:      Product Search Service
Response:      Returns filtered product list with pagination
Measure:       p95 latency < 300ms, p99 < 1s
```

**Architectural Tactics Applied:**
- Elasticsearch for search (vs SQL LIKE queries)
- Redis caching for popular searches (1-hour TTL)
- CDN for product images
- Database read replicas for catalog queries
- Async processing for search analytics

**SLI/SLO Definition:**

| SLI | SLO | Error Budget (30 days) |
|-----|-----|------------------------|
| Search latency p95 | < 300ms, 99.5% | 3.6 hours |
| Checkout success rate | 99.9% | 43 minutes |
| API availability | 99.95% | 21 minutes |

#### Availability Scenario

```
Source:        Internal (database failure)
Stimulus:      Primary database becomes unavailable
Environment:   Peak load (Black Friday)
Artifact:      Order Processing System
Response:      Failover to replica, no order loss
Measure:       < 30 seconds failover, 0% data loss
```

**Architectural Tactics Applied:**
- Multi-AZ deployment on AWS
- PostgreSQL with synchronous replication
- Circuit breakers with Resilience4j
- Graceful degradation (read-only mode for catalog)
- Auto-healing with Kubernetes

**Implementation:**

```yaml
# Kubernetes deployment with health checks
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    spec:
      containers:
      - name: order-service
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Security Scenario

```
Source:        External attacker
Stimulus:      Attempts SQL injection on search
Environment:   Normal operations
Artifact:      Product Search API
Response:      Attack blocked, logged, attacker rate-limited
Measure:       0 successful injections, detection < 1s
```

**Architectural Tactics Applied:**
- Parameterized queries (no string concatenation)
- Input validation with JSON Schema
- WAF rules for common attack patterns
- Rate limiting (100 requests/minute per IP)
- Security headers (CSP, X-Frame-Options)

**Implementation:**

```python
# Input validation with Pydantic
from pydantic import BaseModel, Field, validator
import re

class SearchQuery(BaseModel):
    query: str = Field(max_length=200)
    category: str | None = Field(max_length=50)
    min_price: float | None = Field(ge=0, le=1000000)
    max_price: float | None = Field(ge=0, le=1000000)

    @validator('query')
    def sanitize_query(cls, v):
        # Remove potential SQL injection patterns
        if re.search(r'[;\'"\\]|--', v):
            raise ValueError('Invalid characters in search query')
        return v.strip()
```

### Trade-off Decisions

| Trade-off | Decision | Rationale |
|-----------|----------|-----------|
| Consistency vs Availability | Availability for catalog, Consistency for orders | Users tolerate stale product info, not duplicate orders |
| Performance vs Security | Accept 50ms overhead for encryption | PCI-DSS compliance required |
| Cost vs Scalability | Reserved instances + auto-scaling | 70% base load on reserved, scale up for peaks |

---

## Example 2: Real-time Analytics Dashboard

### System Context

- **Type:** B2B SaaS analytics platform
- **Users:** 10K enterprise customers
- **Data:** 1B events/day ingestion
- **Freshness:** < 5 minutes data latency

### Quality Attribute Scenarios

#### Scalability Scenario

```
Source:        Business growth
Stimulus:      Data volume increases 3x over 6 months
Environment:   Normal operations
Artifact:      Data Ingestion Pipeline
Response:      System scales without architecture changes
Measure:       Linear cost increase, no latency degradation
```

**Architectural Tactics Applied:**
- Kafka for event streaming (partitioned by customer)
- ClickHouse for OLAP queries (columnar storage)
- Kubernetes HPA for auto-scaling workers
- Data partitioning by time and customer
- Tiered storage (hot: SSD, warm: HDD, cold: S3)

**Implementation:**

```yaml
# Kafka topic configuration for scalability
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: analytics-events
spec:
  partitions: 100  # Scale with customers
  replicas: 3
  config:
    retention.ms: 604800000  # 7 days
    segment.bytes: 1073741824  # 1GB
    cleanup.policy: delete
```

```sql
-- ClickHouse table with partitioning
CREATE TABLE events (
    event_id UUID,
    customer_id UInt64,
    event_type String,
    event_data String,
    created_at DateTime
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(created_at)
ORDER BY (customer_id, created_at)
TTL created_at + INTERVAL 2 YEAR;
```

#### Performance Scenario

```
Source:        Dashboard user
Stimulus:      Requests weekly metrics aggregation
Environment:   Peak hours (9-11 AM)
Artifact:      Query Engine
Response:      Returns aggregated data with visualizations
Measure:       p95 < 2s for 90-day queries, p95 < 500ms for 7-day
```

**Architectural Tactics Applied:**
- Pre-aggregated materialized views
- Query result caching (Redis, 5-minute TTL)
- Query timeout enforcement (30 seconds)
- Query cost estimation before execution
- Async query execution for heavy reports

**Implementation:**

```sql
-- ClickHouse materialized view for pre-aggregation
CREATE MATERIALIZED VIEW daily_metrics
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (customer_id, date, metric_name)
AS SELECT
    customer_id,
    toDate(created_at) as date,
    event_type as metric_name,
    count() as count,
    sum(value) as total
FROM events
GROUP BY customer_id, date, event_type;
```

#### Reliability Scenario

```
Source:        Infrastructure
Stimulus:      Kafka broker failure
Environment:   Normal operations
Artifact:      Event Processing Pipeline
Response:      Continue processing without data loss
Measure:       < 1 minute recovery, 0 events lost
```

**Architectural Tactics Applied:**
- Kafka replication factor 3
- Consumer group rebalancing
- Exactly-once processing semantics
- Dead letter queue for failed events
- Idempotent event processing

### SLI/SLO Summary

| Component | SLI | SLO |
|-----------|-----|-----|
| Data Ingestion | Events processed/minute | 99.9% within 5 minutes |
| Query Latency | p95 response time | < 2s for 99% of queries |
| Dashboard Availability | Successful page loads | 99.9% uptime |
| Data Freshness | Lag from event to query | < 5 minutes for 99.5% |

---

## Example 3: Healthcare Patient Portal

### System Context

- **Type:** Patient-facing healthcare portal
- **Users:** 2M registered patients
- **Compliance:** HIPAA, HL7 FHIR
- **Criticality:** Medium (non-emergency use)

### Quality Attribute Scenarios

#### Security Scenario (Authentication)

```
Source:        Patient
Stimulus:      Attempts to access medical records
Environment:   Normal operations
Artifact:      Authentication Service
Response:      Verify identity with MFA, grant access
Measure:       Zero unauthorized access, MFA success > 95%
```

**Architectural Tactics Applied:**
- OAuth 2.0 with PKCE for mobile
- MFA via SMS or authenticator app
- Session timeout (15 minutes idle)
- Biometric authentication option
- Device fingerprinting

**Implementation:**

```python
# HIPAA-compliant session management
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict):
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {
            **data,
            "exp": expires,
            "iat": datetime.utcnow(),
            "type": "access"
        },
        PRIVATE_KEY,
        algorithm=ALGORITHM
    )

async def verify_mfa(user_id: str, code: str) -> bool:
    """Verify MFA code with rate limiting"""
    attempts = await redis.incr(f"mfa_attempts:{user_id}")
    await redis.expire(f"mfa_attempts:{user_id}", 300)

    if attempts > 5:
        raise HTTPException(status_code=429, detail="Too many attempts")

    return await mfa_service.verify(user_id, code)
```

#### Security Scenario (Data Protection)

```
Source:        Database administrator
Stimulus:      Attempts to view patient data directly
Environment:   Database maintenance
Artifact:      Patient Records Database
Response:      Data encrypted, access logged, admin cannot read
Measure:       100% of PHI encrypted, all access logged
```

**Architectural Tactics Applied:**
- AES-256 encryption at rest
- TLS 1.3 in transit
- Column-level encryption for PHI
- Key rotation every 90 days
- Audit logging for all data access

**Implementation:**

```sql
-- PostgreSQL with column encryption
CREATE EXTENSION pgcrypto;

-- Encrypted patient data
CREATE TABLE patient_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    -- PHI columns encrypted
    diagnosis BYTEA NOT NULL,  -- pgp_sym_encrypt
    notes BYTEA,
    -- Metadata not encrypted
    record_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    created_by UUID NOT NULL
);

-- Encryption function
CREATE OR REPLACE FUNCTION encrypt_phi(data TEXT, key TEXT)
RETURNS BYTEA AS $$
    SELECT pgp_sym_encrypt(data, key, 'cipher-algo=aes256')
$$ LANGUAGE SQL;

-- Audit trigger
CREATE OR REPLACE FUNCTION audit_phi_access()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO phi_audit_log (
        table_name, record_id, action, user_id, accessed_at
    ) VALUES (
        TG_TABLE_NAME, NEW.id, TG_OP, current_user, NOW()
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

#### Availability Scenario

```
Source:        Patient
Stimulus:      Accesses portal during EHR system maintenance
Environment:   Degraded (EHR unavailable)
Artifact:      Patient Portal
Response:      Display cached data with "last updated" timestamp
Measure:       Portal available 99.9%, clear degradation notice
```

**Architectural Tactics Applied:**
- Graceful degradation to cached data
- Clear user messaging about limitations
- Separate availability for viewing vs updates
- Background sync when EHR returns

### Compliance Mapping

| HIPAA Requirement | Quality Attribute | Implementation |
|-------------------|-------------------|----------------|
| Access Control | Security (AuthZ) | RBAC with patient consent |
| Audit Logging | Observability | Immutable audit trail |
| Data Encryption | Security (Confidentiality) | AES-256 at rest, TLS in transit |
| Minimum Necessary | Security (AuthZ) | Field-level access control |
| Breach Notification | Reliability | Automated detection and alerting |

---

## Example 4: API Gateway for Microservices

### System Context

- **Type:** Internal API gateway
- **Services:** 50 microservices
- **Traffic:** 100K requests/second peak
- **Teams:** 15 development teams

### Quality Attribute Scenarios

#### Performance Scenario

```
Source:        Internal service
Stimulus:      API request through gateway
Environment:   Peak load (100K RPS)
Artifact:      API Gateway
Response:      Route to appropriate service
Measure:       < 5ms gateway overhead, < 0.01% errors
```

**Architectural Tactics Applied:**
- Kong Gateway with DB-less mode
- Connection pooling per upstream
- Request/response streaming
- Rate limiting per service/consumer
- Request timeout enforcement

**Implementation:**

```yaml
# Kong declarative configuration
_format_version: "3.0"

services:
  - name: order-service
    url: http://order-service.default.svc:8080
    connect_timeout: 5000
    write_timeout: 60000
    read_timeout: 60000
    retries: 3
    routes:
      - name: order-routes
        paths:
          - /api/v1/orders
        strip_path: false

plugins:
  - name: rate-limiting
    config:
      minute: 1000
      policy: redis
      redis_host: redis.default.svc

  - name: prometheus
    config:
      per_consumer: true

  - name: correlation-id
    config:
      header_name: X-Request-ID
      generator: uuid
```

#### Maintainability Scenario

```
Source:        Development team
Stimulus:      Deploys new API version
Environment:   Production
Artifact:      API Gateway routing
Response:      Canary rollout with traffic splitting
Measure:       0 downtime, rollback < 1 minute
```

**Architectural Tactics Applied:**
- API versioning in URL (/v1, /v2)
- Canary deployments (1% -> 10% -> 100%)
- Feature flags for new endpoints
- Backward compatibility enforcement
- Consumer contract testing

**Implementation:**

```yaml
# Kubernetes canary deployment
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: order-service
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  progressDeadlineSeconds: 600
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 1m
```

#### Observability Scenario

```
Source:        Operations team
Stimulus:      Latency spike detected
Environment:   Production
Artifact:      Distributed tracing
Response:      Identify bottleneck service within 5 minutes
Measure:       100% trace coverage, < 5 minute MTTD
```

**Architectural Tactics Applied:**
- OpenTelemetry instrumentation
- Trace ID propagation (W3C Trace Context)
- Span correlation across services
- Service dependency mapping
- Automated anomaly detection

### SLI/SLO for Gateway

| SLI | Target | Alert Threshold |
|-----|--------|-----------------|
| Availability | 99.99% | < 99.9% over 5 min |
| Latency p50 | < 2ms | > 5ms over 5 min |
| Latency p99 | < 10ms | > 20ms over 5 min |
| Error rate | < 0.01% | > 0.1% over 1 min |

---

## Example 5: Multi-tenant SaaS Platform

### System Context

- **Type:** B2B SaaS project management
- **Tenants:** 5,000 organizations
- **Users:** 500K total users
- **Data isolation:** Required per tenant

### Quality Attribute Scenarios

#### Scalability Scenario (Multi-tenancy)

```
Source:        Large enterprise tenant
Stimulus:      Onboards 10,000 users
Environment:   Normal operations
Artifact:      Tenant provisioning
Response:      Scale resources for tenant without affecting others
Measure:       No noisy neighbor impact, linear cost scaling
```

**Architectural Tactics Applied:**
- Tenant-per-schema database isolation
- Per-tenant connection pools
- Per-tenant rate limiting
- Tenant-aware caching (Redis namespaces)
- Horizontal pod autoscaling per tenant tier

**Implementation:**

```python
# Multi-tenant database routing
from contextvars import ContextVar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

tenant_context: ContextVar[str] = ContextVar('tenant_id')

class TenantAwareSession:
    def __init__(self):
        self.engines = {}

    def get_engine(self, tenant_id: str):
        if tenant_id not in self.engines:
            # Each tenant has own schema
            db_url = f"postgresql://user:pass@db/{tenant_id}"
            self.engines[tenant_id] = create_engine(
                db_url,
                pool_size=20,
                max_overflow=10,
                pool_pre_ping=True
            )
        return self.engines[tenant_id]

    def get_session(self):
        tenant_id = tenant_context.get()
        engine = self.get_engine(tenant_id)
        Session = sessionmaker(bind=engine)
        return Session()
```

#### Security Scenario (Data Isolation)

```
Source:        Tenant A user
Stimulus:      Attempts to access Tenant B data
Environment:   Normal operations
Artifact:      Data access layer
Response:      Request denied, security event logged
Measure:       0 cross-tenant data access
```

**Architectural Tactics Applied:**
- Row-level security (RLS) in PostgreSQL
- Tenant ID in JWT claims
- Automatic tenant filtering in queries
- Separate encryption keys per tenant

**Implementation:**

```sql
-- PostgreSQL Row Level Security
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON projects
    USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Set tenant context on connection
CREATE OR REPLACE FUNCTION set_tenant_context(p_tenant_id uuid)
RETURNS void AS $$
BEGIN
    PERFORM set_config('app.current_tenant', p_tenant_id::text, false);
END;
$$ LANGUAGE plpgsql;
```

### Tenant Tier SLOs

| Tier | Availability | Support | Features |
|------|--------------|---------|----------|
| Free | 99.5% | Community | Limited |
| Pro | 99.9% | Email | Full |
| Enterprise | 99.99% | 24/7 | Full + SSO |

---

## Quality Attributes Summary Matrix

| System | Key QA | Primary Tactics |
|--------|--------|-----------------|
| E-commerce | Availability, Security | Multi-AZ, Circuit breakers, WAF |
| Analytics | Scalability, Performance | Kafka, ClickHouse, Caching |
| Healthcare | Security, Compliance | Encryption, Audit logs, MFA |
| API Gateway | Performance, Observability | Connection pooling, Tracing |
| SaaS | Multi-tenancy, Isolation | Schema per tenant, RLS |

---

*Part of [quality-attributes](README.md) | [faion-software-architect](../CLAUDE.md)*
