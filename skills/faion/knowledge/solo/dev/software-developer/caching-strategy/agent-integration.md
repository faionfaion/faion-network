# Agent Integration — Caching Strategy

## When to use
- Read-heavy endpoints with bounded staleness tolerance (product catalog, user profile, settings).
- Expensive computations whose inputs repeat (LLM responses, image transforms, search aggregations).
- Reducing DB load when query plans are tuned but still slow under sustained traffic.
- Static or near-static API responses behind a CDN / edge cache (faion.net, dev.faion.net).
- Session storage, OAuth token cache, rate-limit counters — natural Redis fit.
- Aggregation/dashboard responses where 30-60s freshness is acceptable.
- Idempotency: cache request hashes to deduplicate retries.

## When NOT to use
- Highly volatile data (current bid prices, live counts) where staleness is unacceptable.
- Per-user data with no reuse pattern (cache hit ratio < 50% — wasted memory).
- Strong-consistency requirements (financial ledger, inventory hold).
- Small datasets that fit in app memory anyway (just use a dict).
- Without a measurement plan — caching without hit-rate monitoring is dead weight.
- When cache invalidation logic is more complex than the underlying query.

## Where it fails / limitations
- Cache stampede (thundering herd): N processes miss simultaneously, all hit DB. Mitigations: SWR, request coalescing, probabilistic refresh.
- Stale data after writes if invalidation is missed; double-source-of-truth bugs.
- Memory pressure: TTL too long → unbounded growth; too short → low hit rate.
- Multi-region cache divergence; eventually-consistent stores leak stale reads.
- Negative caching (cache nulls) without TTL → app stuck believing entity doesn't exist.
- Cache key collisions across services without strict namespacing.
- Hot key problem: one Redis key serving all traffic (homepage feature flag) saturates a single Redis shard.
- Cache-aside on write-heavy data thrashes: read → miss → fetch → set, then immediate write invalidates.

## Agentic workflow
Drive caching as: (1) measure baseline (RPS, DB query p95, hot endpoints), (2) classify each endpoint by read/write ratio + staleness tolerance, (3) pick layer (CDN, app, Redis) per class, (4) implement chosen pattern (cache-aside / write-through / write-behind / read-through), (5) emit hit-rate dashboard + alarm on hit < threshold, (6) run before/after load test. Treat cache invalidation as an explicit design decision documented per cache key — TTL, event-based, version-based.

### Recommended subagents
- `faion-software-architect-agent` — owns cache topology + invalidation strategy.
- `faion-api-agent` — implements decorator-based cache around endpoints.
- `faion-sdd-executor-agent` — wraps changes under SDD with hit-rate gates.

### Prompt pattern
```
Audit endpoints in <api-dir>. For each, output JSON:
{path, read_write_ratio, avg_db_latency_ms, staleness_tolerance_s,
 cache_recommendation (none|cdn|app|redis|multi-layer),
 pattern (aside|through|behind|swr), key_template, ttl_s,
 invalidation_trigger (ttl|event|version)}.
Stop. Wait for human review of staleness/TTL choices.
```

```
Implement cache-aside for /api/products/{id} per approved plan.
Use Redis sliding TTL=1800. Add metrics: cache_hit_total{key},
cache_miss_total{key}, cache_set_duration_seconds. Add invalidation
hook in update_product. Add stampede protection via 'singleflight'
pattern. Tests: hit, miss, invalidate, concurrent miss.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redis-cli` / `valkey-cli` | INFO, MONITOR, --latency, MEMORY USAGE | apt install redis-tools |
| `redis-cli --bigkeys` | Find oversized keys | bundled |
| `redis-cli --hotkeys` | Detect hot keys (LFU mode) | bundled |
| `nginx`/`varnish` | Edge HTTP caching | apt install varnish |
| `cf-cli` (Cloudflare) | Purge zone, configure cache rules | npm i -g wrangler |
| `cachegrind`/`memcached-tool` | Memcached stats | bundled |
| `redis-rdb-tools` | RDB memory analysis | pip install rdbtools |
| `prometheus` + node_exporter | Metrics for hit rate, eviction | https://prometheus.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Redis Cloud / Upstash | SaaS | yes (REST + RESP) | Upstash REST is great for serverless; pay-per-request. |
| Valkey | OSS | yes | Linux Foundation Redis fork; faion-net runs `valkey-server` already. |
| AWS ElastiCache (Redis/Memcached) | SaaS | yes (boto3) | Managed clusters with fail-over. |
| Memcached | OSS | yes | Simpler than Redis; only KV + LRU. |
| Cloudflare Cache + Workers KV | SaaS | yes (Wrangler) | Edge HTTP cache; faion.net DNS already on CF. |
| Fastly | SaaS | yes (API) | VCL-driven edge cache; very flexible. |
| Vercel Edge Cache | SaaS | yes | Tied to Next.js/static; faion-cli starter friendly. |
| Cloudfront | SaaS | yes (CDK/CLI) | AWS-native CDN; cache invalidation API. |
| Bunny.net | SaaS | yes | Cheap CDN with origin shield. |
| Varnish | OSS | yes (VCL files) | Self-hosted reverse cache. |
| Dragonfly | OSS | yes | Drop-in Redis-compatible, multi-threaded. |

## Templates & scripts
See `templates.md` for cache-aside / write-through / write-behind. Inline stampede protection (singleflight):

```python
# scripts/cache_singleflight.py
import asyncio
import json
import hashlib
import redis.asyncio as aioredis

class CacheSingleflight:
    """Cache-aside with thundering-herd protection.
    On miss, only one coroutine fetches; others await result.
    """
    def __init__(self, redis: aioredis.Redis, ttl: int = 600, lock_ttl: int = 30):
        self.r = redis
        self.ttl = ttl
        self.lock_ttl = lock_ttl

    async def get_or_set(self, key: str, loader):
        cached = await self.r.get(key)
        if cached is not None:
            return json.loads(cached)

        lock_key = f"lock:{key}"
        # NX SET acts as mutex; only one wins
        won = await self.r.set(lock_key, "1", nx=True, ex=self.lock_ttl)
        if won:
            try:
                value = await loader()
                await self.r.set(key, json.dumps(value), ex=self.ttl)
                return value
            finally:
                await self.r.delete(lock_key)
        else:
            # Wait for the winner; bounded retry
            for _ in range(50):
                await asyncio.sleep(0.05)
                cached = await self.r.get(key)
                if cached is not None:
                    return json.loads(cached)
            # Fallback: load anyway (winner crashed)
            return await loader()

# usage: await sf.get_or_set("user:123", lambda: db.fetch_user(123))
```

## Best practices
- Set a TTL on every key — without TTL Redis becomes append-only memory.
- Choose namespace convention: `{service}:{entity}:{id}:{version}`. Enforce in code review.
- Negative caching: cache misses with shorter TTL (e.g. 60s) to avoid hammering DB on bad inputs, but never permanent.
- Stampede protection: singleflight (above), probabilistic early refresh, or `stale-while-revalidate`.
- Always implement explicit invalidation alongside writes; don't rely on TTL for correctness-critical data.
- Use ETag + `If-None-Match` for HTTP-layer caching; saves payload not just compute.
- Surface metrics: `cache_hit_total`, `cache_miss_total`, `cache_evictions`, `cache_size_bytes` to Prometheus/Grafana.
- Plan for cache outage: app must function (degraded but functional) when Redis is down.
- Cache invalidation by tag/group beats wildcard `KEYS *` (which is O(N) and blocks).
- Use `Cache-Control: stale-while-revalidate=N` to mask backend latency at CDN.
- Pin Redis version + maxmemory-policy (`allkeys-lru` for cache; `noeviction` for queue/session).
- For multi-region: read-local-write-global, accept eventual consistency, document it.

## AI-agent gotchas
- LLMs produce cache layers without invalidation paths — add prompt rule: every cache write must have a documented invalidator.
- Agents pick TTL=86400 by default — too long for most data. Force them to compute TTL from staleness tolerance.
- Negative caching agents forget shorter TTL — they cache `None` for 1 day; bad data flows for hours.
- Cache key includes mutable args (timestamps, request IDs) — every call misses. Always hash on canonical inputs.
- Pickle/JSON in Redis: agents pickle untrusted data → RCE risk. Force JSON or msgpack with schema validation.
- Decorators that swallow exceptions: agents wrap `loader()` in try/except, return cache hit silently — masks DB outage. Surface errors, log, fall through.
- Async + sync redis client mix-up: agents import `redis.Redis` in async code. Pin to `redis.asyncio.Redis` for FastAPI.
- LLMs implement write-through but call DB after Redis (wrong order) — race window where cache shows new, DB still old.
- Agents add cache without measurement: no Prometheus, no hit-rate. Require metrics in the same PR.
- Human-in-loop checkpoint: TTL + invalidation policy per key — these are correctness decisions; agent suggests, human approves.
- Stampede: agents implement basic cache-aside; under load, one DB-killing event traces back to thundering herd. Always include singleflight/SWR for >100 RPS endpoints.

## References
- Redis caching patterns — https://redis.io/docs/manual/patterns/
- HTTP caching (MDN) — https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching
- "Stale-while-revalidate" RFC 5861 — https://datatracker.ietf.org/doc/html/rfc5861
- Cloudflare cache rules — https://developers.cloudflare.com/cache/
- AWS ElastiCache best practices — https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/BestPractices.html
- "Caching at Netflix" (EVCache) — https://netflixtechblog.com/caching-for-a-global-netflix-7bcc457012f1
- Singleflight (Go std-lib pattern) — https://pkg.go.dev/golang.org/x/sync/singleflight
- Dragonfly engine — https://www.dragonflydb.io
