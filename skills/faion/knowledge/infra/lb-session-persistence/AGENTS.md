# Load Balancer Session Persistence (Sticky Sessions)

## Summary

**One-sentence:** Generates a session-persistence decision (externalize → cookie-sticky → IP-hash) + LB config snippet picking the right method for the client + scaling constraints.

**One-paragraph:** Session persistence ensures requests from the same client always reach the same backend server. Methods include source-IP hashing, load-balancer-inserted cookies, application-managed cookies, and SSL session ID tracking. Sticky sessions are a last resort — externalized session storage (Redis, Memcached) eliminates the need for stickiness while enabling true stateless scaling. When sticky sessions are unavoidable, cookie-based persistence is the most accurate and flexible method.

**Ефективно для:**

- Legacy app з in-process session — sticky тільки на час міграції на Redis.
- WebSocket / long-poll: prefer cookie-based для NAT / autoscale-safety.
- ASG environment: НІКОЛИ ip-hash; always cookie-sticky.
- Configuration review: знайти прихований ip-hash + порадити Redis-based externalization.
- Shopping cart, wizard state — cookie-sticky тільки до того часу, як state переїде у Redis.

## Applies If (ALL must hold)

- Application stores session state in local memory or local disk (cannot be moved to shared storage in the short term).
- WebSocket connections that must maintain connection to a specific backend for the session lifetime.
- Shopping cart, login session, or wizard state stored in-process rather than in a database or cache.
- Legacy application that cannot be modified to use a centralized session store.
- Reviewing an existing configuration to determine whether sticky sessions can be removed by adding Redis.

## Skip If (ANY kills it)

- Stateless applications — stickiness adds complexity and reduces distribution quality with no benefit.
- Applications that already use centralized session storage (Redis, database-backed sessions) — remove stickiness and simplify the config.
- Auto-scaling environments where session survival matters — backend removal terminates sticky sessions; use shared storage instead.
- Maximum even distribution is required — any persistence method degrades distribution quality.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Application session storage | inproc / Redis / DB | architecture |
| Client environment | direct / NAT / VPN | network |
| Autoscaling policy | yes/no | infra |
| Connection lifetime | short / long / WebSocket | architecture |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-algorithms]] | Affinity choice constrains which algorithm can be used. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: externalize-first, cookie-over-iphash, no-iphash-asg-nat, ssl-session-id-fragile, sticky-time-bounded | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-method` | sonnet | Decision tree on client + scaling. |
| `emit-snippet` | haiku | Mechanical template fill (HAProxy / Nginx / cloud LB). |

## Templates

| File | Purpose |
|------|---------|
| `templates/sticky-haproxy.cfg` | HAProxy cookie-based sticky session snippet |
| `templates/sticky-nginx.conf` | Nginx Plus / OSS cookie-hash sticky snippet |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-session-persistence.py` | Validate the session-persistence artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-algorithms]]
- [[lb-layer-selection]]
- [[lb-health-checks]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (session-storage location, NAT/autoscale, conn lifetime) to a method choice, each leaf referencing a rule from `01-core-rules.xml`.
