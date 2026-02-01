# Development Methodologies - Architecture

Backend architecture patterns and best practices.

## Database Patterns

### Database Migration Patterns

**Problem:** Manual database changes.

**Framework:**
```sql
-- Up migration
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Down migration
DROP TABLE users;
```

**Agent:** faion-code-agent

### SQL Query Optimization

**Problem:** Slow database queries.

**Framework:**
1. Add appropriate indexes
2. Use EXPLAIN ANALYZE
3. Avoid SELECT *
4. Use query pagination
5. Consider read replicas

**Agent:** faion-code-agent

### ORM Best Practices

**Problem:** N+1 queries, memory issues.

**Framework:**
```python
# Bad: N+1 queries
users = User.objects.all()
for user in users:
    print(user.orders.count())  # New query each iteration

# Good: Prefetch
users = User.objects.prefetch_related('orders').all()
for user in users:
    print(len(user.orders.all()))  # Uses prefetched data
```

**Agent:** faion-code-agent

### Database HA Setup

**Problem:** Single point of failure.

**Framework:**
```
Primary (write)
    │
    ├─► Replica 1 (read)
    └─► Replica 2 (read)

Auto-failover: Primary fails → Replica promoted
```

**Agent:** faion-devops-agent

---

## API Patterns

### API Response Patterns

**Problem:** Inconsistent API responses.

**Framework:**
```json
// Success
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [{ "field": "email", "error": "invalid_format" }]
  }
}
```

**Agent:** faion-code-agent

### Authentication Patterns

**Problem:** Insecure auth implementation.

**Framework:**

| Pattern | Use Case |
|---------|----------|
| JWT | Stateless API auth |
| Session | Server-side state |
| OAuth2 | Third-party login |
| API Keys | Server-to-server |

**Agent:** faion-code-agent

---

## Performance Patterns

### Caching Strategies

**Problem:** High database load.

**Framework:**

| Strategy | Use Case |
|----------|----------|
| Cache-aside | Read-heavy workloads |
| Write-through | Write consistency |
| Write-behind | Write performance |
| Read-through | Automatic cache population |

**Agent:** faion-code-agent

### Queue/Background Jobs

**Problem:** Blocking operations in requests.

**Framework:**
```python
# Celery example
@celery_app.task
def send_welcome_email(user_id: int):
    user = User.objects.get(id=user_id)
    email_service.send(user.email, "Welcome!")

# Usage
send_welcome_email.delay(user.id)
```

**Agent:** faion-code-agent

---

## Observability Patterns

### Logging Best Practices

**Problem:** No structured logging.

**Framework:**
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "user_created",
    user_id=user.id,
    email=user.email,
    source="api"
)
```

**Agent:** faion-code-agent

---

*Architecture Methodologies - 10 Patterns*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement dev-methodologies-architecture pattern | haiku | Straightforward implementation |
| Review dev-methodologies-architecture implementation | sonnet | Requires code analysis |
| Optimize dev-methodologies-architecture design | opus | Complex trade-offs |

