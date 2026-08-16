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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-session-persistence.py` | Validate the session-persistence artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[lb-algorithms]]
- [[lb-layer-selection]]
- [[lb-health-checks]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (session-storage location, NAT/autoscale, conn lifetime) to a method choice, each leaf referencing a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/sticky-haproxy.cfg`

```ini
backend app_servers
    balance leastconn
    option httpchk GET /health
    http-check expect status 200

    # LB-inserted sticky cookie with bounded lifetime + invalidate on backend removal
    cookie SRVID insert indirect nocache maxidle 1h maxlife 24h

    server srv1 10.0.1.1:8080 cookie srv1 check
    server srv2 10.0.1.2:8080 cookie srv2 check
    server srv3 10.0.1.3:8080 cookie srv3 check
```

### `templates/sticky-nginx.conf`

```conf
upstream app_backend {
    zone app_backend 64k;

    # Nginx Plus (commercial): real sticky-cookie support
    # sticky cookie SRVID expires=1h path=/;

    # OSS Nginx workaround: hash on Set-Cookie or app-managed cookie
    # hash $cookie_session_id consistent;

    server 10.0.1.1:8080;
    server 10.0.1.2:8080;
    server 10.0.1.3:8080;

    keepalive 32;
}

# NEVER `ip_hash;` with autoscaling or NAT — see lb-session-persistence rule no-iphash-asg-nat.
```
