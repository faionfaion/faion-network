# Agent Integration — Caching Architecture

## When to use
- Read-heavy workloads with measured DB or upstream pressure (>30% of latency budget on data fetch).
- Hot, repeatable read paths: profiles, catalogues, configuration, feature flags, auth lookups.
- Cost reduction efforts where compute/IO cost is dominated by repeated queries.
- CDN/edge work for static assets, public APIs, marketing pages, image variants.
- Building cache layer for an LLM-powered app (prompt cache, embedding cache, tool-result cache).

## When NOT to use
- Strong-consistency-critical paths (ledger balances, inventory at checkout) without a write-through or distributed-lock pattern.
- Personalized data with a hit-rate ceiling below ~30% — the cache adds latency without paying back.
- Premature optimization: skip until profiling shows a hot key/query.
- Writes-dominated workloads — caches become invalidation sinks.

## Where it fails / limitations
- Cache invalidation is a distributed-systems hard problem: TTL is the safe default, event-driven invalidation only works with reliable change-data capture.
- Stampedes on cold start (thundering herd) — single-flight or request coalescing is mandatory at scale.
- Hot-key skew can pin a single Redis shard; sharding by composite key or local L1 cache is the fix.
- Stale negatives (cached "not found") cause user-visible bugs after a write — choose carefully whether to cache misses.
- LLM-generated cache code often forgets jitter on TTL, leading to synchronized expirations.

## Agentic workflow
Use a designer agent to map cache layers (CDN → gateway → app → DB) and pick a pattern per data type, a code-author agent to wire the chosen client (Redis/Memcached/Varnish/CDN), and a critic agent to attack invalidation, stampedes, and consistency. Always gather two metrics before/after: cache hit ratio and p95 latency on the cached path. Run a "negative test" subagent that intentionally writes-then-reads to surface stale data.

### Recommended subagents
- `brainstorm` — diverge over cache placement and pattern choice (cache-aside vs read-through vs write-through vs write-behind).
- `sdd-execution` — produce spec/design including invalidation events and TTL policy, with explicit test cases for staleness.
- `improver` — post-deploy audit of hit ratio, eviction rate, p99 tail.

### Prompt pattern
```
For each entity in <model>, output a row:
| entity | access pattern | volatility | strategy | layer | TTL | invalidation trigger | stampede control |
Reject any row where invalidation = "manual" without an event source.
```

```
Critique this cache design for: stampedes, hot keys, stale-after-write,
negative caching, multi-region replication lag, and TTL synchronization.
Suggest concrete code changes (single-flight, jitter, request coalescing).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| redis-cli | Inspect keys, TTLs, INFO stats | bundled with Redis |
| memcached-tool | Stats, dump | bundled with Memcached |
| valkey-cli | Redis-compatible alternative | https://valkey.io/ |
| keydb-cli | Multi-threaded Redis fork | https://keydb.dev/ |
| dragonfly | Modern Redis-compatible cache | https://www.dragonflydb.io/ |
| varnishstat / varnishncsa | Edge cache analytics | bundled with Varnish |
| nginx -T | Inspect proxy_cache config | bundled with nginx |
| wrk / vegeta / k6 | Validate hit ratio under load | per-tool |
| RedisInsight | GUI for keyspace analysis | https://redis.io/insight/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Redis Cloud / ElastiCache / MemoryDB | SaaS | Yes — Terraform/CLI | Managed Redis with HA |
| Upstash Redis | SaaS | Yes — REST API | Serverless, agent-friendly per-call billing |
| Cloudflare Cache / Workers KV | SaaS | Yes — wrangler CLI | Edge cache, KV for small hot data |
| Fastly | SaaS | Yes — VCL is text | Powerful edge logic, agent-readable VCL |
| AWS CloudFront | SaaS | Yes — CDK/Terraform | Standard CDN |
| Varnish Cache | OSS | Partial | VCL is unique syntax; pin agent to docs |
| Memcached | OSS | Yes | Use only for ephemeral key-value |
| Hazelcast / Apache Ignite | OSS | Partial | Distributed in-memory; complex to agent-drive |

## Templates & scripts
See `templates.md` for Redis client, Django cache, FastAPI middleware, and CDN configs. Inline single-flight helper:

```python
# single_flight.py — collapse concurrent cache misses for the same key.
import asyncio, time
from typing import Awaitable, Callable

class SingleFlight:
    def __init__(self) -> None:
        self._inflight: dict[str, asyncio.Future] = {}
        self._lock = asyncio.Lock()

    async def do(self, key: str, fn: Callable[[], Awaitable]) -> object:
        async with self._lock:
            fut = self._inflight.get(key)
            if fut is None:
                fut = asyncio.get_event_loop().create_future()
                self._inflight[key] = fut
                owner = True
            else:
                owner = False
        if owner:
            try:
                fut.set_result(await fn())
            except Exception as e:
                fut.set_exception(e)
            finally:
                async with self._lock:
                    self._inflight.pop(key, None)
        return await fut

# usage: await sf.do(f"user:{uid}", lambda: load_user(uid))
```

## Best practices
- Always add jitter to TTLs (`base * (1 + rand(-0.1, 0.1))`) to avoid synchronized expiry storms.
- Cache the *result of an expensive computation*, not the *raw row* — survives schema changes better.
- Set explicit eviction policy (`maxmemory-policy allkeys-lru` or `volatile-ttl`) and alert on eviction rate, not just memory.
- Track hit ratio per key prefix; an aggregate hit ratio masks dead caches.
- Use idempotent keys; never include unstable attributes (timestamps, request IDs) in keys.
- Prefer `SETNX` + TTL for distributed locks during cache fill, not application-level mutexes that don't survive process restarts.
- For LLM apps, always measure cache value with a tracing tool — agents tend to over-cache prompt fragments that change every call.

## AI-agent gotchas
- Agents will cache user-specific data with a global key — always require the prompt to spell out the cache key formula (`user:{uid}:profile:v1`).
- Agents forget to bump cache version when schema changes; require a `v<N>` suffix in keys and have a critic check schema↔key version coupling.
- Don't let agents cache 404s without an explicit policy — silent stale negatives cause "ghost user" bugs.
- LLM-generated Redis pipelines often lack `await` boundaries; pin the prompt to specific async patterns of the client lib.
- Human-in-loop gates: TTL policy approval (per data class), invalidation strategy review for any write path, post-deploy hit-ratio review.

## References
- https://redis.io/docs/manual/patterns/
- https://martinfowler.com/bliki/TwoHardThings.html
- https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
- https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/welcome.html
- https://www.cloudflare.com/learning/cdn/what-is-caching/
- https://www.varnish-software.com/developers/tutorials/
