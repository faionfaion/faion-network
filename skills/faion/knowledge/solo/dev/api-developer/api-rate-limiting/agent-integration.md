# Agent Integration — API Rate Limiting

## When to use
- Public APIs where abuse, scraping, or unintentional client loops can degrade service for paying customers — rate limiting is mandatory before launch.
- Tiered SaaS pricing models that gate value by request volume (free / plus / pro / enterprise) and need per-key quotas.
- Cost-sensitive endpoints fronting paid third-party services (LLM inference, geocoding, SMS) where one runaway client triggers real financial loss.
- Auth and password-reset endpoints where rate limiting + lockout deters credential-stuffing and enumeration attacks.
- Distributed multi-instance services that must share counters; a Redis / Valkey-backed sliding window is the standard.

## When NOT to use
- Internal-only RPC between trusted services with stable load profiles — circuit breakers and concurrency limits are more useful than per-key rate limits.
- Pure static asset delivery (CDN handles abuse upstream).
- Workflows already gated by quotas at a different layer (DB connection pool, job queue concurrency) where adding HTTP rate limits hides the real bottleneck.
- Endpoints that must process every event (webhooks, IoT telemetry) — back-pressure with 503 + queues, not 429.

## Where it fails / limitations
- **Fixed-window thundering herd.** All clients reset at minute boundary; spike at `:00`. Mitigation: sliding window or token bucket.
- **Per-IP only.** NAT'd corporate networks share an IP; one customer blocks the rest. Mitigation: prefer API key / user ID; fall back to IP only for unauth.
- **In-memory counters in distributed deploy.** Counters per pod allow N×limit traffic. Mitigation: Redis / Valkey with `INCR`/`ZADD` Lua script.
- **Race conditions.** Naive `GET counter; INCR if < limit; SET counter` allows over-limit. Use atomic Redis pipelines or `INCR` with TTL.
- **No `Retry-After`.** Clients hammer endpoints in tight loops; bandwidth + log spam. Always set the header.
- **Hidden tier mismatches.** Free user hits a "pro" endpoint; gets 429 with no upgrade prompt. Surface tier limit + upgrade URL in response.
- **Bucket pollution.** Sliding-window ZSET grows unbounded if `EXPIRE` missing; memory leak. Always set TTL.
- **Distributed clock skew.** Token-bucket math assumes synchronized time; large skew over-credits or starves. Use Redis time as authoritative.
- **Burst handling.** Token bucket with no burst capacity rejects valid bursts (UI page-load fanout). Set bucket > steady-state limit.
- **Weighted endpoints.** All endpoints cost 1 token even though some are 100× heavier. Use cost-per-call or per-endpoint limits.
- **Header inconsistency.** Mixing `X-RateLimit-*` and IETF `RateLimit-*` confuses SDKs. Pick the IETF draft (`RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`) going forward.
- **Bypass via authenticated proxies.** Internal services share a key; one misbehaving service drains the limit. Mitigation: per-service keys.

## Agentic workflow
Drive rate-limit work in four stages: (1) a **policy-author** subagent encodes the limit matrix (tier × endpoint group → algorithm + limit + burst + window) in a single config file referenced by gateway + app middleware; (2) a **middleware-author** subagent generates ASGI / Express / Gin middleware that reads the policy, talks to Redis, sets `RateLimit-*` and `Retry-After` headers, and returns Problem Details on 429; (3) a **load-tester** subagent runs k6 / hey / locust against staging to verify limits hold under burst and steady load; (4) a **dashboard-builder** subagent emits Grafana panels for `429 rate`, `consumed budget per tier`, `top abusers`. `faion-sdd-executor-agent` runs the standard quality gate. Always lift limits behind a feature flag for gradual rollouts.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs lint/build/test plus integration tests against a Redis fixture.
- A purpose-built **policy-author** — emits `rate-limits.yaml` with per-tier per-endpoint groups; refuses unbounded endpoints.
- A **load-test-runner** — generates k6 scripts that ramp to 1.5× limit and assert 429 + `Retry-After` distribution.
- A **redis-script-curator** — ships `INCR-with-TTL` and `ZADD-sliding-window` Lua scripts as canonical primitives; agents must reuse, not reinvent.
- A **header-auditor** — verifies every successful response from rate-limited endpoints includes `RateLimit-*`; every 429 includes `Retry-After`.
- A **bypass-detector** — scans middleware for `if internal:` paths that disable limits; flags missing scope guards.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — catches keys / IPs in tests / logs.

### Prompt pattern
Policy authoring:
```
Add rate limits for the new /api/exports endpoint group.
Plans: free=10/h burst 2; plus=100/h burst 10; pro=1000/h burst 50.
Algorithm: sliding window via Redis ZSET.
Output a diff to rate-limits.yaml only; do not edit middleware.
Reject configs without burst or without TTL.
```

Middleware generation:
```
Generate FastAPI middleware reading rate-limits.yaml.
Per request:
- Identify principal: api_key from Authorization header,
  fallback to X-API-Key, fallback to client IP.
- Look up tier from key store; default = "free".
- Apply policy for endpoint group via Redis sliding window.
- On allow: set RateLimit-Limit/-Remaining/-Reset (IETF draft).
- On deny: 429 + RFC 9457 Problem Details type
  https://api.example.com/errors/rate-limit-exceeded + Retry-After.
- Skip /health and /metrics.
- Whitelist principals tagged "internal" via key store flag.
Add an integration test using fakeredis covering burst + steady-state.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redis-cli` / `valkey-cli` | Inspect counters and ZSETs in dev | https://redis.io/docs/latest/operate/oss_and_stack/management/cli/ |
| `k6` | Scriptable load testing for limit verification | https://k6.io |
| `hey` | Simple HTTP load tester | https://github.com/rakyll/hey |
| `locust` | Python-based load testing | https://locust.io |
| `wrk` | Low-overhead benchmarking | https://github.com/wg/wrk |
| `slowapi` | Rate-limit middleware for FastAPI / Starlette | https://github.com/laurentS/slowapi |
| `express-rate-limit` | Express rate-limit middleware | https://github.com/express-rate-limit/express-rate-limit |
| `tollbooth` | Go rate-limit middleware | https://github.com/didip/tollbooth |
| `node-ratelimit` (`@upstash/ratelimit`) | Edge-friendly | https://github.com/upstash/ratelimit |
| `envoy` | L7 proxy with global rate-limit service | https://www.envoyproxy.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cloudflare Rate Limiting / WAF | SaaS | yes | Edge limit before origin; configurable via API/Terraform. |
| AWS API Gateway Usage Plans | SaaS | yes | Per-API-key quotas + throttling. |
| Kong Rate-Limiting plugin | OSS / SaaS | yes | Local + Redis policies; agent-friendly via `kong.yml`. |
| Envoy Rate Limit Service | OSS | yes | Centralized RL for service mesh. |
| Upstash Ratelimit | SaaS | yes | Serverless Redis-backed RL. |
| Redis / Valkey | OSS | yes | Self-hosted backbone for atomic counters. |
| Stripe / GitHub | reference | n/a | Public best-practice limits + headers. |

## Templates & scripts
See `templates.md` for `slowapi` and Express middleware templates plus k6 burst test. Atomic Redis sliding-window primitive (under 50 lines):

```python
# rate_limit_sliding_window.py
import time
from redis.asyncio import Redis

LUA_SCRIPT = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
local count = redis.call('ZCARD', key)
if count >= limit then
  local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
  local retry_after = math.ceil(((tonumber(oldest[2]) or now) + window) - now)
  return {0, count, retry_after}
end
redis.call('ZADD', key, now, now .. ':' .. math.random())
redis.call('EXPIRE', key, window)
return {1, count + 1, 0}
"""

class SlidingWindow:
    def __init__(self, redis: Redis):
        self.redis = redis
        self._sha = None

    async def _load(self) -> str:
        if self._sha is None:
            self._sha = await self.redis.script_load(LUA_SCRIPT)
        return self._sha

    async def hit(self, key: str, window_s: float, limit: int):
        sha = await self._load()
        now = time.time()
        allowed, count, retry_after = await self.redis.evalsha(
            sha, 1, key, now, window_s, limit
        )
        return bool(allowed), int(count), int(retry_after)
```

## Best practices
- **Identify principals consistently:** API key → user ID → IP. Whitelist internal service keys.
- **Sliding window or token bucket** in production; fixed window only for trivial cases.
- **Atomic counters via Redis Lua / pipelines.** Never `GET; check; SET`.
- **TTL on every counter / ZSET** to prevent memory leaks.
- **Per-endpoint group limits.** Heavy endpoints (`/search`, `/export`) need stricter caps than `/users/me`.
- **Cost-per-call** for non-uniform endpoints (LLM tokens, search depth) — limit by points, not request count.
- **Headers always:** IETF `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` on success; `Retry-After` on 429.
- **Problem Details body** on 429 with `code: RATE_LIMIT_EXCEEDED`, tier info, upgrade link.
- **Edge limits** at CDN / WAF for L7 attacks; app-level limits for business quotas.
- **Logs and metrics:** track 429 rate, top consumers, tier saturation; alert on sustained ≥80% utilization.
- **Document limits** prominently in API docs with code examples for backoff (exponential + jitter).
- **Burst capacity** sized to natural UI fanouts (e.g. dashboard with 6 concurrent calls); too tight breaks pages.
- **Soft warnings** — surface `RateLimit-Remaining` < 10% via UI to give end-users runway.
- **Roll out behind feature flags**; run shadow mode first (count would-be limits without enforcing).

## AI-agent gotchas
- **In-process counters in distributed deploys.** Agent picks `slowapi` defaults; counters local; total throughput = N×limit. Force Redis backend.
- **Forgetting TTL on ZSET / hash.** Memory leaks; Redis OOM later. Lint the script; require `EXPIRE` after every counter write.
- **Naive get-then-set.** Race condition over-limits. Reject non-atomic patterns in code review.
- **Missing `Retry-After`.** Clients tight-loop. Header auditor blocks merge.
- **Penalizing all clients on a NAT'd IP.** Agent rate-limits unauthenticated traffic by IP only; one customer takes down the rest. Use API key when present.
- **Hard-coded limits in middleware.** No tier awareness; agent forgets to look up plan. Always read from policy config + key store.
- **429 without Problem Details body.** Loose JSON envelope. Use shared `ProblemDetail.from_code(...)`.
- **Bypass paths.** `/internal/...` skipped by middleware via overly broad regex. Bypass-detector flags.
- **Counter key collisions.** `rate:{user}` collides between endpoint groups. Namespace as `rl:{group}:{principal}`.
- **Time skew.** Agent uses `datetime.now()` per pod for token-bucket math; Redis-time is authoritative.
- **Health check rate-limited.** `/health` blocked under load → liveness probes restart pods. Always exempt.
- **Counter pollution from canaries.** Synthetic monitors share an API key; saturate the limit. Whitelist monitor keys.
- **Scope confusion.** Limit applied per request but cost is per token / per row. Switch to weighted limits.
- **Hot Redis key.** All traffic hashed to one shard; latency spike. Use `{tag}` hash slots or per-region instances.

## References
- IETF draft `RateLimit-*` headers: https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/
- RFC 6585 (429 status): https://datatracker.ietf.org/doc/html/rfc6585
- Stripe Rate Limits: https://stripe.com/docs/rate-limits
- GitHub Rate Limits: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
- Cloudflare Rate Limiting docs: https://developers.cloudflare.com/waf/rate-limiting-rules/
- Redis Rate Limiting Pattern: https://redis.io/glossary/rate-limiting/
- Token Bucket: https://en.wikipedia.org/wiki/Token_bucket
- Sibling methodologies: `solo/dev/api-developer/api-error-handling/`, `solo/dev/api-developer/api-gateway-patterns/`, `solo/dev/api-developer/api-authentication/`.
