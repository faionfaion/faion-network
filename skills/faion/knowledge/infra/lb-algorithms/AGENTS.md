# Load Balancing Algorithm Selection

## Summary

**One-sentence:** Generates a load-balancing algorithm choice (round-robin, weighted RR, least-conn, weighted LC, least-response-time) + LB config snippet driven by traffic profile.

**One-paragraph:** Load balancing algorithms distribute traffic across backend servers. Static algorithms (round-robin, weighted round-robin, IP hash, random) ignore real-time server load; dynamic algorithms (least connections, weighted least connections, least response time, resource-based) adapt to server state. Algorithm choice is driven by request duration homogeneity, server capacity uniformity, and autoscaling behavior. The output is an LB config snippet (Nginx upstream, HAProxy backend, or cloud LB JSON) plus a one-paragraph decision record.

**Ефективно для:**

- Variable-cost workloads (WebSocket, DB proxy, mixed fast/slow API) — `leastconn` за замовчуванням.
- Autoscaling environments — eliminate `ip_hash`; use cookie-based persistence або leastconn.
- Heterogeneous fleet (CPU/RAM різні) — weighted least-connections з weight ~ capacity.
- p50/p99 spread &gt;2x — switch from round-robin to leastconn без коду.
- Architecture review caught агента, який пропонує "least-conn for performance" з sticky sessions — reject inconsistency.

## Applies If (ALL must hold)

- Selecting an algorithm before writing any load balancer config.
- Reviewing an existing config that exhibits uneven backend utilization or high p99 latency.
- Autoscaling events are causing distribution problems (ip-hash + frequent scale events).
- Traffic has variable request cost (some endpoints are fast, others are slow, long-running).

## Skip If (ANY kills it)

- Session persistence is the primary concern — see lb-session-persistence for ip-hash + cookie-based approaches.
- Tool-specific algorithm configuration (HAProxy `balance` directive, Nginx upstream) — see lb-haproxy-production / lb-nginx-production.
- Service-mesh internal load balancing (Envoy / Istio) — those use distinct xDS-configured algorithms.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Traffic profile | p50/p95/p99 latency + request rate | APM / load test |
| Fleet inventory | server count + per-server capacity | infra inventory |
| Autoscaling policy | min/max + scale-out trigger | infra |
| Connection type | short HTTP / long WebSocket / DB pool | architecture |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-layer-selection]] | L4 vs L7 choice constrains which algorithms are even available. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: round-robin-only-uniform, no-ip-hash-autoscale, leastconn-default-variable-cost, weighted-by-capacity, measure-before-choose | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-algorithm` | sonnet | Decision-tree application against measured traffic profile. |
| `emit-config-snippet` | haiku | Mechanical template-filling per chosen algorithm. |

## Templates

| File | Purpose |
|------|---------|
| `templates/algorithm-decision.json` | Algorithm-choice artefact matching 02-output-contract |
| `templates/upstream.conf` | Nginx upstream block skeleton |
| `templates/backend.cfg` | HAProxy backend block skeleton |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-algorithms.py` | Validate the algorithm-choice artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-layer-selection]]
- [[lb-session-persistence]]
- [[lb-health-checks]]
- [[lb-technology-selection]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (capacity homogeneity, request-cost variance, autoscaling, NAT presence) to a concrete algorithm, each leaf referencing a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/algorithm-decision.json`

```json
{
  "algorithm": "weighted-least-connections",
  "fleet_capacity": "heterogeneous",
  "request_cost": "variable",
  "autoscaling": true,
  "nat_behind_lb": false,
  "measured": {
    "p50_ms": 80,
    "p99_ms": 240
  },
  "weights": [
    100,
    100,
    50
  ],
  "rationale": "p99/p50 = 3x indicates variable request cost; ASG scales backends; fleet has two large + one small node. leastconn adapts to variance; weights restore proportional capacity."
}
```

### `templates/upstream.conf`

```conf
upstream app_backend {
    # Algorithm directive: omit for round-robin; least_conn for least-connections.
    # least_conn;
    # ip_hash;     # only on stable, NAT-free fleet — see lb-session-persistence
    # hash $cookie_SRVID consistent;  # cookie-based persistence (Nginx Plus)

    server 10.0.1.1:8080 weight=100 max_fails=3 fail_timeout=30s;
    server 10.0.1.2:8080 weight=100 max_fails=3 fail_timeout=30s;
    server 10.0.1.3:8080 weight=50  max_fails=3 fail_timeout=30s;

    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name app.example.com;

    location / {
        proxy_pass http://app_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### `templates/backend.cfg`

```ini
backend app_servers
    # balance roundrobin               # uniform workloads only
    balance leastconn                  # default for variable-cost
    # balance source                   # NEVER with autoscaling or NAT

    option httpchk GET /health
    http-check expect status 200
    default-server inter 10s fall 3 rise 2

    # weights proportional to per-server capacity
    server large1 10.0.1.1:8080 check weight 100
    server large2 10.0.1.2:8080 check weight 100
    server small1 10.0.1.3:8080 check weight 50

    # cookie-based stickiness (replace ip-hash on autoscaling/NAT)
    cookie SRVID insert indirect nocache
```
