# Agent Integration — Rate Limiting

## When to use
- Public APIs that anonymous or semi-trusted users hit (sign-up, password-reset, OTP, search).
- Tiered SaaS where plan = limit (free/plus/pro/enterprise).
- Expensive endpoints (export, report generation, LLM proxy, image upload) where one bad actor sinks cost.
- Auth endpoints to mitigate credential stuffing (per-IP + per-account limits).
- Edge layer protection in front of slow upstreams to shed load.

## When NOT to use
- Internal service-to-service traffic with mTLS or service mesh — use authz + circuit breakers instead.
- Single-user CLI / desktop apps talking to a private backend — limits add no security value.
- Background workers reading from a queue — backpressure is queue depth, not rate.
- Use cases that need quota / billing accounting, not throttling — those need a metering system (Stripe Meter, OpenMeter), rate-limiting is the wrong tool.

## Where it fails / limitations
- In-memory limiters (`dict` counters) break the moment you scale to >1 replica — every replica has its own counter.
- Fixed window has the well-known 2× burst at the boundary; switch to sliding window if fairness matters.
- Token bucket can be gamed by clients that warm the bucket then burst; cap bucket size aggressively.
- Distributed limiters add per-request Redis RTTs; for hot paths, use approximate counting (cell-based, like `redis-cell`) or local + global hybrid.
- IP-based limits punish CGNAT/corporate users; combine with auth-keyed limits.
- LLM gateways: token-based limiting (TPM) ≠ request-based (RPM); you need both.
- IPv6 makes per-IP limiting nearly meaningless without `/64` aggregation.

## Agentic workflow
A planner subagent inventories endpoints, classifies each by cost (cheap / medium / expensive / abuse-target) and key (anonymous-IP / authed-user / API-key / tenant). An implementer subagent generates middleware/decorator code in the right framework (FastAPI, Express, Axum, NestJS) and wires Redis/Valkey. A test subagent generates load tests (`k6` / `vegeta`) that probe limits, headers, and `Retry-After` correctness. A reviewer subagent audits for missing limits on auth + abuse-prone endpoints.

### Recommended subagents
- `faion-sdd-executor-agent` — drives planner → implementer → test loop.
- A user-defined `loadtest-runner` (model: haiku) — generates and runs `k6` scripts, reports p99.
- A user-defined `endpoint-auditor` (model: sonnet) — scans routes file, flags any unrate-limited login/signup/forgot-password.

### Prompt pattern
- "Read `rate-limiting/README.md`. Inventory all routes in `<routes-file>`. For each: assign tier (cheap/medium/expensive), key (ip/user/tenant/apikey), algorithm (fixed/sliding/token-bucket), limit, window. Output a YAML table; do not edit code yet."
- "Implement rate-limiting middleware in `<framework>` using sliding window on Redis. Read keys from `rate_limits.yaml`. Emit `X-RateLimit-*` and `Retry-After` headers. Return JSON 429 per the schema in README. Add unit + integration tests."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redis-cli` / `valkey-cli` | Inspect counters, ZSETs, TTL during debug | bundled with Redis/Valkey |
| `redis-cell` | Generic Cell Rate Algorithm module (precise, low overhead) | https://github.com/brandur/redis-cell |
| `k6` | Scripted load tests, can probe 429s | https://k6.io |
| `vegeta` | Constant-rate HTTP attacker for replication tests | https://github.com/tsenart/vegeta |
| `slowloris.py` / `goloris` | Test slow-request shedding | OSS scripts |
| `wrk2` | Constant-throughput latency probe | https://github.com/giltene/wrk2 |
| `hey` | Quick burst-traffic generator | `go install github.com/rakyll/hey@latest` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cloudflare Rate Limiting | SaaS | Yes (API/Terraform) | Edge enforcement; cheap to wire, opaque to debug. |
| AWS WAF rate-based rules | SaaS | Yes (Terraform) | Per-IP only, 5-min minimum window. |
| Kong | OSS / SaaS | Yes (Admin API) | Plugin-based; `rate-limiting-advanced` for sliding window + Redis. |
| Tyk | OSS / SaaS | Yes | Per-key, per-endpoint, quota + rate. |
| Envoy `local_ratelimit` + `ratelimit` service | OSS | Yes | Service mesh native; complex setup. |
| Upstash Ratelimit | SaaS | Yes (TS SDK) | Redis-as-a-service; stock sliding window/token bucket; ideal for serverless. |
| `slowapi` (FastAPI) | OSS | Yes | Drop-in middleware backed by Redis or memory. |
| `express-rate-limit` + `rate-limit-redis` | OSS | Yes | Standard Node setup. |
| Redis / Valkey | OSS | Yes | The substrate; `redis-cell` for GCRA. |

## Templates & scripts
See `templates.md` for fixed/sliding/token-bucket limiters. Minimal `k6` probe an agent can drop in to verify limits + headers:

```js
// k6 run --vus 50 --duration 30s rl_probe.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const URL = __ENV.URL || 'https://api.example.com/v1/search';
const TOKEN = __ENV.TOKEN;

export default function () {
  const res = http.get(URL, { headers: { Authorization: `Bearer ${TOKEN}` } });
  check(res, {
    'has limit hdr': (r) => !!r.headers['X-Ratelimit-Limit'],
    'has remaining hdr': (r) => !!r.headers['X-Ratelimit-Remaining'],
    '429 has Retry-After': (r) => r.status !== 429 || !!r.headers['Retry-After'],
    '429 body has retryAfter': (r) =>
      r.status !== 429 || (r.json('error.retryAfter') !== null),
  });
  sleep(0.05);
}
```

## Best practices
- Always emit standard headers (`X-RateLimit-Limit/Remaining/Reset`, `Retry-After`); also support draft IETF `RateLimit-*` if your clients are recent.
- Compose **multiple** keys per request: `ip + user + apikey + tenant`; deny if any one is over.
- For auth endpoints, use **two** limiters: per-IP (block bots) AND per-account (block targeted attacks). Per-account limits triggered ⇒ alert, not just 429.
- Use sliding window or GCRA in production; reserve fixed window for low-stakes counters.
- Store Redis keys with explicit TTL (`EXPIRE`) ≥ window; never rely on LRU eviction for correctness.
- Whitelist internal CIDRs / service accounts at the **outermost** layer, not inside the limiter (avoids bypass via spoofed headers).
- Log limit-exceeded events at WARN with key, route, limit; create a dashboard for top offenders.
- For LLM proxies: limit by both RPM and TPM (token estimate). Estimate tokens with `tiktoken` before forwarding.
- For multi-tenant SaaS, separate `tenant` and `user` keys; one tenant flooding shouldn't poison another.
- Always test the **429 path** in integration tests — broken `Retry-After` parsing is a common client bug.

## AI-agent gotchas
- LLMs default to in-memory limiters that are useless past 1 replica. Force Redis/Valkey backing.
- Agents implement fixed window first because it's the simplest example in the README — review and ask for sliding window for any user-facing endpoint.
- Sliding-window-with-ZSET as written has a race in the README (count includes the just-added entry); double-check that the count compare uses the value **after** zadd or use Lua to make it atomic.
- Token-bucket implementations frequently miss the `min(bucket_size, …)` clamp on refill — this lets bursts grow unbounded after long idle.
- Per-IP limiters in front of a CDN need `X-Forwarded-For` parsing with a trusted-proxy list; agents often grab `request.remote_addr` and limit the CDN's IP, killing all traffic together.
- Agents forget IPv6 `/64` aggregation; one user can rotate IPs in their /64 and bypass.
- When wiring Cloudflare/Kong, agents may double-limit (edge + app); decide one canonical layer per route and document it.
- Human-in-loop checkpoint: changes to limits on `/login`, `/signup`, `/forgot-password`, billing, and webhook endpoints should never be merged unreviewed.
- Don't let an agent silently raise a limit because a load test failed — first verify the load test isn't measuring the limiter itself.

## References
- IETF draft `RateLimit` headers — https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/
- Cloudflare blog: counting at scale — https://blog.cloudflare.com/counting-things-a-lot-of-different-things/
- Stripe API rate limits — https://stripe.com/docs/rate-limits
- GCRA / `redis-cell` — https://github.com/brandur/redis-cell
- Upstash Ratelimit — https://upstash.com/docs/oss/sdks/ts/ratelimit/overview
- Token-bucket vs leaky-bucket — https://en.wikipedia.org/wiki/Token_bucket
