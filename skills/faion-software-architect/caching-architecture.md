# Caching Architecture

Strategies for caching to improve performance.

## Why Cache?

- **Reduce latency** - Memory vs disk/network
- **Reduce load** - Fewer database queries
- **Cost savings** - Less compute needed
- **Improve availability** - Serve stale if backend down

## Cache Layers

```
Client ─▶ CDN ─▶ API Cache ─▶ App Cache ─▶ DB Cache ─▶ DB
         (edge)  (gateway)    (Redis)      (query)
```

| Layer | What to Cache | Tools |
|-------|---------------|-------|
| Browser | Static assets, API responses | HTTP headers |
| CDN | Static files, some dynamic | Cloudflare, CloudFront |
| API Gateway | Full responses | Kong, nginx |
| Application | Objects, queries | Redis, Memcached |
| Database | Query results | Built-in query cache |

## Caching Patterns

### Cache-Aside (Lazy Loading)

App manages cache explicitly.

```python
def get_user(user_id):
    # Check cache first
    user = cache.get(f"user:{user_id}")
    if user:
        return user

    # Cache miss - fetch from DB
    user = db.get_user(user_id)

    # Store in cache
    cache.set(f"user:{user_id}", user, ttl=3600)
    return user
```

**Pros:** Simple, cache only what's needed
**Cons:** Cache miss penalty, possible stale data

### Write-Through

Write to cache and DB together.

```python
def update_user(user_id, data):
    # Update DB
    db.update_user(user_id, data)

    # Update cache
    cache.set(f"user:{user_id}", data)
```

**Pros:** Cache always consistent
**Cons:** Write latency, cache pollution

### Write-Behind (Write-Back)

Write to cache, async to DB.

```python
def update_user(user_id, data):
    # Write to cache immediately
    cache.set(f"user:{user_id}", data)

    # Queue async write to DB
    queue.push({"user_id": user_id, "data": data})
```

**Pros:** Fast writes
**Cons:** Data loss risk, complexity

### Read-Through

Cache handles fetching from DB.

```python
# Cache client configured with loader
cache = Cache(
    loader=lambda key: db.get(key)
)

# Automatically fetches on miss
user = cache.get(f"user:{user_id}")
```

## Cache Invalidation

> "There are only two hard things in CS: cache invalidation and naming things."

### TTL (Time-To-Live)

```python
cache.set("key", value, ttl=3600)  # Expires in 1 hour
```

**Simple but may serve stale data.**

### Event-Based Invalidation

```python
def update_user(user_id, data):
    db.update_user(user_id, data)
    cache.delete(f"user:{user_id}")  # Invalidate
    event_bus.publish(f"user:{user_id}:updated")
```

### Versioned Keys

```python
version = get_version("user")  # e.g., from DB
key = f"user:{user_id}:v{version}"

# Bump version to invalidate all
def invalidate_user_cache():
    increment_version("user")
```

## Cache Key Design

```python
# Good: Predictable, hierarchical
"user:123"
"user:123:orders"
"product:456:reviews:page:1"

# Include relevant parameters
"search:query=laptop:page=1:sort=price"

# Version for schema changes
"user:123:v2"
```

## Distributed Caching

### Redis Cluster

```
           ┌─────────────┐
           │   Client    │
           └──────┬──────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───┴───┐    ┌───┴───┐    ┌───┴───┐
│Node 1 │    │Node 2 │    │Node 3 │
│Slots  │    │Slots  │    │Slots  │
│0-5460 │    │5461-  │    │10923- │
│       │    │10922  │    │16383  │
└───────┘    └───────┘    └───────┘
```

### Cache Consistency Patterns

| Pattern | Consistency | Performance |
|---------|-------------|-------------|
| Write-through | Strong | Slower writes |
| Write-behind | Eventual | Fast writes |
| Cache-aside | Eventual | Flexible |

## HTTP Caching

### Cache-Control Header

```http
# Cache for 1 hour
Cache-Control: public, max-age=3600

# Don't cache
Cache-Control: no-store

# Cache but revalidate
Cache-Control: no-cache

# Stale while revalidate
Cache-Control: max-age=60, stale-while-revalidate=30
```

### ETag (Conditional Requests)

```http
# Response
ETag: "abc123"

# Subsequent request
If-None-Match: "abc123"

# If unchanged: 304 Not Modified
```

## Common Issues

### Cache Stampede
Many requests hit DB when cache expires.

**Solution:** Lock, probabilistic refresh
```python
def get_with_lock(key):
    value = cache.get(key)
    if value is None:
        with cache.lock(f"{key}:lock"):
            value = cache.get(key)  # Check again
            if value is None:
                value = fetch_from_db()
                cache.set(key, value)
    return value
```

### Hot Keys
Single key gets too many requests.

**Solution:** Replicate to multiple keys, local cache

### Cold Start
Cache empty after restart.

**Solution:** Cache warming, gradual rollout

## Related

- [performance-architecture.md](performance-architecture.md) - Performance overall
- [database-selection.md](database-selection.md) - Database context
