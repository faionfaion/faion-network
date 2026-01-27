# Caching Architecture

Comprehensive guide to designing and implementing caching strategies for high-performance applications.

## Why Cache?

| Benefit | Impact |
|---------|--------|
| Reduce latency | Memory access ~100ns vs disk ~10ms vs network ~100ms |
| Reduce database load | 70-90% fewer queries with proper caching |
| Cost savings | Less compute, fewer database replicas needed |
| Improve availability | Serve stale data when backend is down |
| Handle traffic spikes | Absorb load without scaling backend |

## Cache Layers

```
Client --> CDN --> API Gateway --> Application --> Database
         (edge)   (nginx/Kong)    (Redis)        (query cache)
```

| Layer | What to Cache | Tools | TTL Range |
|-------|---------------|-------|-----------|
| Browser | Static assets, API responses | HTTP headers, Service Worker | 1h - 1y |
| CDN/Edge | Static files, HTML, API responses | Cloudflare, CloudFront, Fastly | 5m - 24h |
| API Gateway | Full responses, rate limiting | Kong, nginx, Envoy | 1m - 1h |
| Application | Objects, queries, sessions | Redis, Memcached, in-memory | 1m - 24h |
| Database | Query results, prepared statements | Built-in query cache | Auto |

## Caching Patterns Overview

### 1. Cache-Aside (Lazy Loading)

Application manages cache explicitly. Most common pattern.

```
Read: App --> Cache (miss) --> DB --> Cache (store) --> App
Write: App --> DB --> Cache (invalidate)
```

**Best for:** Read-heavy workloads, data that can tolerate staleness
**Avoid for:** Write-heavy workloads, real-time consistency requirements

### 2. Read-Through

Cache handles fetching from database transparently.

```
Read: App --> Cache (miss) --> Cache fetches from DB --> App
```

**Best for:** Simpler application code, consistent caching logic
**Avoid for:** Complex invalidation requirements

### 3. Write-Through

Write to cache and database synchronously.

```
Write: App --> Cache --> DB (sync)
```

**Best for:** Data consistency critical, frequently read after write
**Avoid for:** Write-heavy workloads (latency penalty)

### 4. Write-Behind (Write-Back)

Write to cache, async persist to database.

```
Write: App --> Cache --> Queue --> DB (async)
```

**Best for:** High write throughput, eventual consistency acceptable
**Avoid for:** Critical data (risk of loss), strong consistency needs

### 5. Write-Around

Write directly to database, bypass cache.

```
Write: App --> DB (cache not updated)
Read: Standard cache-aside pattern
```

**Best for:** Write-once/read-rarely data, large objects
**Avoid for:** Frequently accessed after write

## Pattern Selection Matrix

| Scenario | Pattern | Reason |
|----------|---------|--------|
| User profiles | Cache-Aside + TTL | Read-heavy, tolerate staleness |
| Shopping cart | Write-Through | Consistency critical |
| Analytics events | Write-Behind | High volume, eventual OK |
| File uploads | Write-Around | Large, rarely re-read |
| Session data | Read-Through | Transparent management |
| Leaderboards | Cache-Aside + Event | Frequent reads, periodic updates |

## Cache Invalidation Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| TTL (Time-To-Live) | Auto-expire after duration | Most common, simple |
| Event-Based | Invalidate on data change | Real-time consistency |
| Version-Based | Change key version to invalidate | Schema changes, bulk updates |
| Tag-Based | Group keys, invalidate by tag | Related data invalidation |
| Purge/Ban | Explicit removal by pattern | CDN, emergency updates |

## Key Concepts

### Cache Key Design

```
# Hierarchical, predictable keys
user:{user_id}
user:{user_id}:profile
user:{user_id}:orders:page:{page}
product:{product_id}:reviews:sort:{sort}:page:{page}

# Include version for schema changes
user:{user_id}:v2

# Hash for complex parameters
search:{md5(query_params)}
```

### TTL Guidelines

| Data Type | TTL | Rationale |
|-----------|-----|-----------|
| Static assets (CSS/JS) | 1 year | Versioned filenames |
| Product catalog | 5-15 min | Moderate change frequency |
| User profiles | 1-5 min | Personal, changes occasionally |
| Session data | 30 min - 24h | Security vs UX balance |
| Search results | 1-5 min | Freshness important |
| Configuration | 1-5 min | Rarely changes |
| Real-time data | 10-60 sec | Near real-time needs |

### Cache Hit Ratio Targets

| Application Type | Target Hit Ratio | Notes |
|------------------|------------------|-------|
| CDN static assets | >95% | Highly cacheable |
| API responses | >70% | Good baseline |
| Database queries | >80% | Significant load reduction |
| Session data | >90% | User-specific |

## Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| Cache Stampede | Locking, probabilistic early expiration |
| Hot Keys | Replication, local caching, sharding |
| Cold Start | Cache warming, gradual rollout |
| Stale Data | Event invalidation, shorter TTL |
| Memory Pressure | Eviction policies (LRU/LFU), tiered caching |
| Inconsistency | Write-through, version keys |

## Technology Selection

### In-Memory Caches

| Tool | Best For | Limitations |
|------|----------|-------------|
| Redis | General purpose, data structures | Single-threaded (use cluster) |
| Memcached | Simple key-value, high throughput | No persistence, no data types |
| Dragonfly | Redis-compatible, multi-threaded | Newer, smaller community |

### CDN Providers

| Provider | Strengths | Best For |
|----------|-----------|----------|
| Cloudflare | Free tier, Workers, security | Most projects |
| CloudFront | AWS integration, Lambda@Edge | AWS-heavy stacks |
| Fastly | Real-time purge, VCL | Advanced edge logic |
| Akamai | Enterprise, global reach | Large enterprises |

### Application-Level

| Framework | Built-in Caching | Redis Integration |
|-----------|------------------|-------------------|
| Django | django.core.cache | django-redis |
| FastAPI | None built-in | fastapi-cache, aiocache |
| Express | None built-in | ioredis, node-cache |
| Spring | Spring Cache | spring-data-redis |

## LLM Usage Tips

When discussing caching with LLMs:

1. **Specify the layer** - "CDN caching" vs "application caching" vs "database caching"
2. **Describe the workload** - Read/write ratio, data size, consistency needs
3. **Mention the stack** - Redis version, framework, cloud provider
4. **Define success metrics** - Target hit ratio, latency requirements
5. **Include constraints** - Memory limits, cost budget, existing infrastructure

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step caching design checklist |
| [examples.md](examples.md) | Real-world case studies and implementations |
| [templates.md](templates.md) | Copy-paste templates for configurations |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted design |

## External Resources

### Official Documentation
- [Redis Caching Solutions](https://redis.io/solutions/caching/)
- [AWS Caching Best Practices](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
- [Cloudflare Cache Documentation](https://developers.cloudflare.com/cache/)
- [CloudFront Caching Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ConfiguringCaching.html)

### Research Papers
- [Optimal Probabilistic Cache Stampede Prevention](https://cseweb.ucsd.edu/~avattani/papers/cache_stampede.pdf) - Mathematical foundation for early expiration

### Guides and Tutorials
- [Azure Caching Guidance](https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching)
- [Cloudflare: Lock-free Probabilistic Caching](https://blog.cloudflare.com/sometimes-i-cache/)

## Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [performance-architecture](../performance-architecture/) | Performance optimization context |
| [database-selection](../database-selection/) | Database and caching tool selection |
| [system-design-process](../system-design-process/) | System design with caching layer |
| [microservices-architecture](../microservices-architecture/) | Distributed caching patterns |
