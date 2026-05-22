---
slug: lb-session-persistence
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Session persistence ensures requests from the same client always reach the same backend server.
content_id: "bd38c678b036cc2e"
tags: [load-balancing, session-persistence, sticky-sessions, stateful, infrastructure]
---
# Load Balancer Session Persistence (Sticky Sessions)

## Summary

**One-sentence:** Session persistence ensures requests from the same client always reach the same backend server.

**One-paragraph:** Session persistence ensures requests from the same client always reach the same backend server. Methods include source-IP hashing, load-balancer-inserted cookies, application-managed cookies, and SSL session ID tracking. Sticky sessions are a last resort — externalized session storage (Redis, Memcached) eliminates the need for stickiness while enabling true stateless scaling. When sticky sessions are unavoidable, cookie-based persistence is the most accurate and flexible method.

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

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/cicd-engineer/`
