# HAProxy Production Configuration

## Summary

**One-sentence:** Generates a production HAProxy config with TLS-1.2+/1.3, stick-table rate-limiting, path-based ACL routing, keepalived VIP HA, and tuned maxconn/nbthread.

**One-paragraph:** Production HAProxy setup covers: global performance tuning (`maxconn`, `nbthread`, `cpu-map`), TLS 1.2+/1.3 with strong cipher suites, rate limiting via `stick-table` (e.g., 100 req/10s per IP) without an external state store, path-based ACL routing to separate backends, HTTP health checks with `expect` directives, and active-passive HA using `keepalived` for VIP failover.

**Ефективно для:**

- Bare-metal / VM фронт перед service fleet, де управління повне.
- Rate-limiting без Redis: stick-table в-процесі — досить для 1-2 інстансів.
- Mixed L4 (DB / Redis) + L7 (HTTP) в одному процесі через окремі frontend-блоки.
- Keepalived VIP active-passive HA для on-prem deployments.
- MetalLB + HAProxy ingress pattern для bare-metal Kubernetes.

## Applies If (ALL must hold)

- Standing up HAProxy in front of a service fleet on bare metal, VMs, or as a Kubernetes Ingress controller.
- Implementing rate limiting without an external Redis/Memcached state store.
- Routing TCP (database, Redis) alongside HTTP workloads from a single LB process.
- Setting up active-passive HA with keepalived for a VIP that survives node failure.

## Skip If (ANY kills it)

- Simple web server + LB combo — Nginx handles this with less config overhead.
- Static-content caching — Nginx has a built-in cache; HAProxy does not.
- Managed cloud environments where ALB/NLB is available — see lb-cloud-terraform.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Backend list | IP:port table | service inventory |
| TLS cert + key | PEM | cert manager |
| VIP CIDR + interface | string | network |
| Rate-limit policy | req/sec per IP | product / abuse team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-technology-selection]] | Confirms HAProxy is the right tool before tuning. |
| [[lb-health-checks]] | Health-check endpoint design feeds the `option httpchk` block. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: tls12-min-cipher-suites, stick-table-rate-limit, nbthread-cpu-map, maxconn-sized, http-check-expect, keepalived-vrrp | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tune-maxconn-nbthread` | sonnet | Sizing arithmetic from RAM/CPU. |
| `write-frontend-acls` | sonnet | Routing logic per path/host. |
| `lint-config` | haiku | Mechanical `haproxy -c -f` smoke test. |

## Templates

| File | Purpose |
|------|---------|
| `templates/haproxy.cfg` | Full production config: global + defaults + http_front + acl + backends + stick-table |
| `templates/keepalived.conf` | VRRP active-passive VIP config |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-haproxy-production.py` | Validate the HAProxy artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-technology-selection]]
- [[lb-nginx-production]]
- [[lb-high-availability]]
- [[lb-health-checks]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (protocol mix, HA need, rate-limit need, capacity per node) to a concrete config shape, each leaf referencing a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/haproxy.cfg`

```ini
global
    log         /dev/log local0
    chroot      /var/lib/haproxy
    user        haproxy
    group       haproxy
    daemon
    nbthread    8
    cpu-map     auto:1/1-8 0-7
    maxconn     200000
    tune.ssl.default-dh-param 2048
    ssl-default-bind-options no-sslv3 no-tlsv10 no-tlsv11 prefer-client-ciphers
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384

defaults
    log         global
    mode        http
    option      httplog
    option      dontlognull
    option      forwardfor
    timeout connect 5s
    timeout client  50s
    timeout server  50s
    maxconn     50000

frontend https_front
    bind *:443 ssl crt /etc/haproxy/certs/site.pem alpn h2,http/1.1
    http-response set-header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"

    # rate limit: 100 req/10s per IP
    stick-table type ip size 100k expire 10m store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }

    acl is_api path_beg /api
    use_backend api_servers if is_api
    default_backend web_servers

frontend http_redirect
    bind *:80
    http-request redirect scheme https code 301

backend web_servers
    balance leastconn
    option httpchk GET /health
    http-check expect status 200
    default-server inter 10s fall 3 rise 2 weight 100

    server web1 10.0.1.1:8080 check
    server web2 10.0.1.2:8080 check

backend api_servers
    balance leastconn
    option httpchk GET /api/health
    http-check expect status 200
    default-server inter 10s fall 3 rise 2 weight 100

    server api1 10.0.2.1:8000 check
    server api2 10.0.2.2:8000 check
```

### `templates/keepalived.conf`

```conf
vrrp_script chk_haproxy {
    script   "/usr/bin/killall -0 haproxy"
    interval 2
    weight   -20
    fall     2
    rise     2
}

vrrp_instance VI_1 {
    state            MASTER          # change to BACKUP on the secondary node
    interface        eth0
    virtual_router_id 51             # same on master + backup; unique per VRRP group
    priority         150             # 100 on backup
    advert_int       1
    unicast_src_ip   10.0.0.10       # this node's IP
    unicast_peer { 10.0.0.11 }       # other node's IP

    authentication {
        auth_type    PASS
        auth_pass    "REPLACE_ME"    # must match on master + backup
    }

    virtual_ipaddress {
        10.0.0.100/24                # VIP — clients point here
    }

    track_script {
        chk_haproxy
    }

    notify_master  "/etc/keepalived/notify.sh MASTER"
    notify_backup  "/etc/keepalived/notify.sh BACKUP"
    notify_fault   "/etc/keepalived/notify.sh FAULT"
}
```
