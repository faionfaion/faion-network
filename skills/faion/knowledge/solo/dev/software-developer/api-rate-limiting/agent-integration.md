# Agent Integration — API Rate Limiting

## When to use
- Public API exposed to untrusted callers (free/paid tiers, third-party integrations).
- Backend hosted on a single small VPS where one client can DoS the box (faion-net cx53).
- Endpoints with expensive ops: search, exports, AI calls, mailers, OAuth token mint.
- Per-tenant fairness in multi-tenant SaaS — Free vs Plus vs Pro buckets.
- Abuse/credential-stuffing protection on `/login`, `/register`, `/forgot-password`.

## When NOT to use
- Pure internal RPC behind a private network or service mesh — use mTLS quotas instead.
- Latency-critical hot paths (<5 ms) where a Redis round-trip would double cost — push limiting to nginx/envoy.
- Single-user CLI tools or scripts ran on developer laptops.
- Idempotent webhooks from trusted partners with their own backpressure (Stripe, GitHub).

## Where it fails / limitations
- In-process counters (`dict`, `lru_cache`) break the moment you scale to 2 replicas — counts diverge, limits leak.
- Fixed-window allows 2x burst at window boundary (199 req at 10:59:59 + 10:00:00).
- Redis SET-based sliding window is O(N) memory per key — unbounded if `window` is hours and traffic is high.
- IP-based limiting punishes mobile carriers / corporate NATs sharing a single egress IP.
- Limits keyed only on `user_id` are bypassable with multiple anonymous accounts — pair with device/IP.
- 429 without `Retry-After` causes well-behaved clients to hammer in tight retry loops.
- `X-RateLimit-*` headers leak business intelligence about your tier structure to competitors.

## Agentic workflow
Drive rate-limit work as: (1) classify endpoints by cost/abuse-risk, (2) pick algorithm per class, (3) implement with shared store, (4) generate load test that hits the limit and verifies headers + 429 body. Subagent reads the existing API surface (OpenAPI or route table), proposes a tier table, generates middleware + tests in one pass. Human reviews tier numbers before deploy — those are business decisions, not code decisions.

### Recommended subagents
- `faion-api-agent` — owns API contracts, can derive limits from OpenAPI `x-rate-limit` extensions.
- `faion-sdd-executor-agent` — implements middleware + tests under SDD quality gates.
- `faion-browser-agent` — drives k6/Locust to verify limits work end-to-end (via shell, not browser).

### Prompt pattern
```
Audit routes in <api-dir>. For each, output JSON:
{path, method, cost_class (cheap|medium|expensive|destructive),
 suggested_algo (token-bucket|sliding-window|fixed-window),
 limit_per_tier {free, plus, pro}, key (user|ip|api_key|composite)}.
Stop. Wait for user approval before implementing.
```

```
Generate FastAPI middleware using Redis sliding window for the approved table.
Include 429 with RFC 6585 Retry-After + RateLimit-* headers (IETF draft).
Add pytest covering: (1) under-limit pass, (2) over-limit 429,
(3) reset after window, (4) tiered limits, (5) Redis-down fallback.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redis-cli` | Inspect counters, debug stuck keys | apt install redis-tools |
| `k6` | Generate sustained load to validate limits | https://k6.io/docs |
| `locust` | Python-based load gen, scriptable scenarios | pip install locust |
| `wrk` | Quick burst tests | apt install wrk |
| `hey` | Lightweight HTTP load tool | go install github.com/rakyll/hey |
| `nginx -t` | Validate `limit_req_zone` syntax | bundled |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cloudflare Rate Limiting | SaaS | yes (API + Terraform) | Edge layer; pair with origin limiter. faion-net already uses CF DNS. |
| AWS API Gateway throttling | SaaS | yes (boto3) | Per-stage + per-method limits. |
| Kong Gateway | OSS | yes (Admin API) | Pluggable; sliding-window, response-rate-limit plugins. |
| Envoy `local_ratelimit` / `ratelimit` | OSS | yes (config) | Sidecar pattern; pairs with Redis service. |
| nginx `limit_req`/`limit_conn` | OSS | yes (text cfg) | Built-in, leaky bucket. Already in faion-net stack. |
| Redis / Valkey | OSS | yes | Shared store for distributed counters; valkey-server already on faion-net. |
| Upstash Redis | SaaS | yes (REST) | Serverless-friendly when no persistent Redis. |
| `slowapi` (Python) | OSS | yes | FastAPI/Flask wrapper around `limits` library. |

## Templates & scripts
See `templates.md` for Python/FastAPI middleware. Inline k6 verification:

```js
// k6-rate-limit-check.js — run: k6 run -e BASE=https://api.example.com k6-rate-limit-check.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = { vus: 5, duration: '90s' };
const TOKEN = __ENV.TOKEN;

export default function () {
  const r = http.get(`${__ENV.BASE}/api/search?q=hello`, {
    headers: { Authorization: `Bearer ${TOKEN}` },
    tags: { name: 'search' },
  });
  check(r, {
    'has RateLimit-Limit header': (x) => !!x.headers['X-Ratelimit-Limit'] || !!x.headers['Ratelimit-Limit'],
    'on 429 has Retry-After': (x) => x.status !== 429 || !!x.headers['Retry-After'],
    'no 5xx': (x) => x.status < 500,
  });
  sleep(0.1);
}
```

## Best practices
- Key on the **most expensive identity available**: `api_key > user_id > session > device_id > ip`.
- Use sliding-window log only when limits are small (<1k/window). Otherwise sliding-window counter (two buckets, weighted).
- Token bucket for burst-tolerant endpoints (uploads, batch APIs); fixed-window for billing/quota where exact counts matter.
- Always emit `RateLimit-Policy`, `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` per IETF draft — clients (Stripe SDK, axios-retry) auto-honor them.
- Fail-open if Redis is down on read endpoints; fail-closed on writes/auth — choose per route, document the choice.
- Separate **abuse limits** (low, IP-based, short window, returns 429) from **quota limits** (high, key-based, long window, returns 402 or custom).
- Run a "pressure test" in staging weekly; sustained load reveals leaky-bucket misconfigurations before customers do.
- Whitelist your monitoring + health-check IPs/keys; otherwise Pingdom will trip your own limits.

## AI-agent gotchas
- Agents asked to "add rate limiting" love in-memory dict implementations — explicitly forbid; require shared store.
- LLMs hallucinate `redis.set_with_ttl()` API — use `setex` or `set(..., ex=...)`. Pin to `redis>=5` and ask for type-checked code.
- When an agent runs load tests against its own limited backend, it can lock itself out for hours; always provision a bypass header (`X-Internal-Token`) for the agent's own probes and rotate it.
- Code-gen often forgets the **clock skew** between app servers — sliding-window math must use Redis `TIME` cmd, not `time.time()`.
- Agents writing tests sometimes assert `< limit` instead of `<= limit` — off-by-one drift; always include a boundary test.
- LLMs default to keying on `request.client.host` which behind a proxy is `127.0.0.1` — require `X-Forwarded-For` parsing with trusted-proxy list.
- Human-in-loop checkpoint: tier numbers (limit values) are pricing decisions — never let the agent finalize them; surface as a question.

## References
- IETF draft "RateLimit Headers" — https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/
- Stripe rate limits — https://stripe.com/docs/rate-limits
- Cloudflare Rate Limiting docs — https://developers.cloudflare.com/waf/rate-limiting-rules/
- "Rate limiting at scale" (Figma engineering) — https://www.figma.com/blog/an-alternative-approach-to-rate-limiting/
- Redis rate-limiting glossary — https://redis.io/glossary/rate-limiting/
