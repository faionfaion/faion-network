# Agent Integration — Caching Strategy

## When to use
- Hot read paths (read:write ratio ≥ 10:1) where origin latency or load is hurting SLOs.
- Expensive computations (joined queries, ML inference, third-party API calls) with stable inputs.
- Session state, rate limits, idempotency keys, and short-lived counters — Redis fits naturally.
- Static / semi-static content served at the edge (CDN) — biggest latency wins per dollar.
- Read-replica relief: cache the top N% of queries to keep replicas from melting under traffic spikes.

## When NOT to use
- Strong-consistency reads (financial balances, "I just wrote this and must see it"). Cache + eventual consistency means stale answers.
- Low traffic / high cardinality (each key hit once) — cache hit rate will be near zero, just adds latency and ops cost.
- Sensitive data without TTL + eviction discipline — caches become a parallel data store and a compliance footgun.
- Anywhere the cost of cache misses is unbounded (cache stampede on a slow origin); without a stampede guard you make incidents worse.

## Where it fails / limitations
- The README's `cache_aside` decorator builds keys from `args + kwargs` repr — non-deterministic ordering, mutable defaults, and `dict` repr drift across Python versions. Force `key_builder=`.
- Decorator's `invalidate` uses a glob (`f"{key_prefix}:*"`) when no key_builder is provided — Redis `KEYS *` is O(N) and blocks; agents ship this without realizing.
- Write-through example writes to DB then re-reads — under concurrent writers the cache can hold a stale view for the time between write and re-read.
- Write-behind loses durability on crash; agents reach for it for "performance" without acknowledging the data-loss window.
- Cache stampede ("thundering herd") on TTL expiry: 1000 requests hit origin simultaneously. The README has no `SET NX` or single-flight pattern.
- TTL drift: agent sets one TTL on a hot key and a different TTL on its dependency; reads see a half-stale view.

## Agentic workflow
Caching changes look small but break consistency in subtle ways. Have one agent design the invalidation rules (write paths → keys to invalidate, TTL ladder, stampede guard) as a Markdown table BEFORE writing any code. A second agent implements; a reviewer agent (Opus) walks every write path and verifies the corresponding cache key is invalidated. Always add a hit-rate metric and a stampede log line — without them, the caching layer is invisible until it fails.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → impl → review; quality gates should require a hit-rate test.
- A custom `cache-invalidation-auditor` (Opus, read-only) — given the diff, lists every write path and pairs it with the cache key invalidation; flags missing pairs.
- `password-scrubber-agent` — Redis URLs and TLS cert blobs sometimes leak into config files.

### Prompt pattern
```
Add a cache layer for <function/endpoint>.
Inputs: read QPS, write QPS, freshness budget (seconds), cardinality estimate.
Output: (1) key schema (Markdown table), (2) TTL + jitter, (3) stampede guard (singleflight or SETNX lock), (4) write-path → invalidation table, (5) implementation, (6) Prometheus metrics (hit/miss/stale/error counters).
Forbid: KEYS *, SCAN inside hot path, unbounded keys, missing TTL.
```

```
Review diff. For every write to <table>, find the cache key that must be invalidated. Output JSON: {writes: [{file:line, table, mutated_columns, expected_keys[], found_keys[]}]}. Reject if any writes have empty found_keys.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redis-cli` | Inspect keys, MEMORY USAGE, latency monitor, MONITOR | https://redis.io/docs/connect/cli/ |
| `redis-cli --bigkeys` / `--memkeys` | Find oversized or hot keys | https://redis.io/docs/management/optimization/memory-optimization/ |
| `redis-cli --latency` / `--latency-history` | Live tail of operation latency | builtin |
| `memcached-tool` | Inspect slab usage | https://github.com/memcached/memcached |
| `varnishadm` / `varnishlog` / `varnishstat` | HTTP cache mgmt + observability | https://varnish-cache.org/docs/ |
| `wrk` / `vegeta` / `k6` | Load test cache hit rate before/after | https://github.com/wg/wrk · https://k6.io |
| `cloudflare wrangler` / `aws cloudfront` | Edge cache invalidation | https://developers.cloudflare.com/workers/wrangler/ |
| `pgbench` + `pg_stat_statements` | Confirm DB load reduction post-caching | https://www.postgresql.org/docs/current/pgbench.html |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Redis (OSS / Stack / Enterprise) | OSS / SaaS | Yes | Default L3. Modules: RedisJSON, RediSearch, RedisBloom expand patterns. |
| Valkey | OSS | Yes | Drop-in Redis replacement (post-license-change fork). |
| KeyDB / Dragonfly | OSS | Yes | Multi-threaded Redis-compatible. Test agent code against Dragonfly's command differences. |
| Memcached | OSS | Yes | Simpler than Redis; agent code must not assume data structures beyond key→bytes. |
| Cloudflare Workers KV / Cache | SaaS | Yes | API-driven invalidation; agents can purge by tag. |
| Fastly | SaaS | Yes | Surrogate keys → tag-based invalidation; powerful for content-heavy sites. |
| AWS ElastiCache / MemoryDB | SaaS | Yes | MemoryDB gives durable Redis (no write-loss); use when "cache" is also source of truth. |
| Varnish | OSS | Partial | VCL config is a small DSL — agents can edit but should run `varnishtest`. |
| Caffeine (JVM) / Ristretto (Go) / `cachetools` (Py) | OSS | Yes | In-process L2 with TinyLFU; pair with Redis L3 for multi-level. |

## Templates & scripts
See `templates.md` for cache-aside, write-through, write-behind, and refresh-ahead patterns. Stampede-safe wrapper (≤40 lines) the agent should use as default:

```python
# scripts/cache_aside_safe.py
import time, json, secrets
import redis
r = redis.Redis(decode_responses=True)

def cached(key, ttl, fetch, lock_ttl=10, jitter=0.1):
    val = r.get(key)
    if val is not None:
        return json.loads(val)

    lock_key = f"lock:{key}"
    token = secrets.token_hex(8)
    if r.set(lock_key, token, nx=True, ex=lock_ttl):
        try:
            fresh = fetch()
            ttl_jitter = int(ttl * (1 + jitter * (secrets.randbelow(200) - 100) / 100))
            r.set(key, json.dumps(fresh), ex=ttl_jitter)
            return fresh
        finally:
            # Release lock only if we still own it.
            if r.get(lock_key) == token:
                r.delete(lock_key)

    # Lost the race; wait briefly and read.
    for _ in range(20):
        time.sleep(0.05)
        val = r.get(key)
        if val is not None:
            return json.loads(val)
    return fetch()  # Fallback: do the work ourselves.
```

## Best practices
- Pick a strategy per dataset, not per service. Document it: `users` → cache-aside, `sessions` → write-through, `feed` → refresh-ahead.
- Always set TTL + jitter. Synchronized expiries cause synchronized stampedes; ±10–20% jitter spreads them.
- Use a stampede guard (single-flight, mutex, `SET NX EX`) on every cache miss path that hits an expensive origin.
- Track these metrics on every cache: `hit_total`, `miss_total`, `stale_served_total`, `error_total`, `latency_seconds`, `key_count`. Alert on hit-rate drop and miss spike.
- Treat the cache as untrusted: app must function (degraded) when Redis is down. Use `circuit breaker → origin` fallback.
- Namespace keys with a version (`user:v3:{id}`) so deploys can invalidate atomically by bumping the version.
- For multi-level caches, write-through to all levels but invalidate top-down.

## AI-agent gotchas
- Agents pick TTL by gut feel ("3600 sounds fine") with no link to freshness budget. Force a justification comment per TTL.
- LLMs forget invalidation on write paths — they cache reads but never wire `cache.delete(...)` into the update RPC. Reviewer agent must close this loop.
- The default `cache_aside` decorator hashes `args + kwargs` — agents pass mutable objects (lists, dicts) and produce different keys for equivalent inputs. Force a typed `key_builder`.
- Agents conflate idempotency keys, rate limits, and caches; all live in Redis but have different invalidation semantics. Keep separate prefixes and TTL discipline.
- `Redis.scan_iter` over millions of keys looks innocuous in code; in production it's expensive and stalls. Block any non-O(1) Redis op in hot paths.
- Human-in-loop checkpoint: any new key prefix or TTL change in production needs reviewer approval. The agent must produce hit-rate projection + worst-case stale window.

## References
- Caching patterns — https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside
- Redis best practices — https://redis.io/docs/manual/patterns/
- "Designing Data-Intensive Applications" (Kleppmann) — chapters 5, 9.
- Cache stampede / dogpile — https://en.wikipedia.org/wiki/Cache_stampede
- TinyLFU paper — https://arxiv.org/abs/1512.00727
- Cloudflare cache tags — https://developers.cloudflare.com/cache/how-to/purge-cache/purge-cache-tags/
