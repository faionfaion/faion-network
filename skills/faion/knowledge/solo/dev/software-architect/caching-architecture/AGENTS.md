# Caching Architecture

## Summary

Design multi-layer caching strategies (browser → CDN → API gateway → application → database) using the correct pattern per data type: cache-aside, read-through, write-through, write-behind, or write-around. Every cache layer requires explicit TTL with jitter, an invalidation trigger, and stampede control. Always measure hit ratio and p95 latency before and after.

## Why

Proper caching reduces p95 latency by eliminating redundant DB/upstream calls (70-90% fewer queries is typical) and absorbs traffic spikes without scaling the backend. Cache invalidation is the hard part: TTL is the safe default; event-driven invalidation only works with reliable change-data capture. Hot-key skew and stampedes are the most common failure modes at scale.

## When To Use

- Read-heavy workloads with measured DB or upstream pressure (&gt;30% of latency budget on data fetch).
- Hot, repeatable read paths: profiles, catalogues, configuration, feature flags, auth lookups.
- Cost reduction where compute/IO cost is dominated by repeated queries.
- CDN/edge work for static assets, public APIs, marketing pages, image variants.
- LLM-powered apps needing prompt cache, embedding cache, or tool-result cache layers.

## When NOT To Use

- Strong-consistency-critical paths (ledger balances, inventory at checkout) without write-through or distributed-lock pattern.
- Personalized data with hit-rate ceiling below ~30% — the cache adds latency without payback.
- Premature optimization: skip until profiling shows a hot key/query.
- Writes-dominated workloads — caches become invalidation sinks.

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Five caching patterns (cache-aside, read-through, write-through, write-behind, write-around) with use-case and avoidance rules. |
| `content/02-keys-ttl-problems.xml` | Cache key design rules, TTL guidelines per data type, hit-ratio targets, common problems (stampede, hot keys, stale negatives) and solutions. |
| `content/03-technology.xml` | In-memory tool comparison (Redis, Memcached, Dragonfly), CDN provider comparison, framework integration table. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cache-service.py` | Generic Python CacheService with get/set/get-or-set-with-lock, XFetch early-expiration, and pattern invalidation. |
| `templates/redis-config.conf` | Production Redis standalone config with maxmemory, eviction policy, TLS, and persistence disabled. |
| `templates/django-cache-settings.py` | Django CACHES settings for default + sessions with django-redis, KEY_PREFIX, and cache decorators. |
