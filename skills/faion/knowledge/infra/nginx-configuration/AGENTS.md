# Nginx Configuration Hardening

## Summary

**One-sentence:** Nginx server configuration: TLS profile, upstream health checks, rate-limit zones, security headers and proxy-cache sizing for production workloads.

**One-paragraph:** Nginx server configuration: TLS profile, upstream health checks, rate-limit zones, security headers and proxy-cache sizing for production workloads. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `config` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-nginx-configuration.py` before publication.

**Ефективно для:**

- Hardening публічного reverse-proxy перед запуском.
- Налаштування rate-limit zones для login / signup.
- Виставлення proxy_cache з sizing + cache lock.

## Applies If (ALL must hold)

- Input matches the methodology scope (nginx-configuration) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `config` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Upstream catalogue | service → host:port + health-check path | service team |
| TLS certificate source | ACME / Vault / file path per host | security team |
| Traffic profile | expected RPS + burst per route | product owner |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[kubernetes]] | upstream context likely already loaded when this methodology fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output/gate per step | ~800 |
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-config-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nginx.conf` | Annotated configuration skeleton with required keys + comments per knob |
| `templates/_smoke-test.json` | Minimum viable filled-in version of the template used by `--self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nginx-configuration.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[kubernetes]]
- [[iac-pr-review-checklist]]
- [[gitops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `tls-modern-profile` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/nginx.conf`

```conf
worker_processes auto;
worker_rlimit_nofile 65535;

events { worker_connections 8192; multi_accept on; }

http {
  sendfile on; tcp_nopush on; tcp_nodelay on;
  client_max_body_size 16m;
  client_header_timeout 10s; client_body_timeout 30s;
  large_client_header_buffers 4 16k;

  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_prefer_server_ciphers on;
  ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';

  limit_req_zone $binary_remote_addr zone=login:10m rate=5r/s;
  proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=app_cache:64m max_size=2g inactive=60m use_temp_path=off;

  upstream app {
    zone app 64k;
    keepalive 64;
    server app1.local:8080 max_fails=3 fail_timeout=30s;
    server app2.local:8080 max_fails=3 fail_timeout=30s;
  }

  server {
    listen 443 ssl http2;
    server_name example.com;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location /login {
      limit_req zone=login burst=10 nodelay;
      proxy_pass http://app;
    }

    location / {
      proxy_cache app_cache;
      proxy_cache_lock on;
      proxy_cache_valid 200 1h;
      proxy_pass http://app;
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "slug": "nginx-configuration",
  "version": "1.0.0",
  "settings": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
  },
  "applied_to": [
    "prod"
  ],
  "notes": "Generated by nginx-configuration methodology."
}
```
