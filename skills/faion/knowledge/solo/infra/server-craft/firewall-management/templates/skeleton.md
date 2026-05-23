<!-- purpose: UFW audit report with deny defaults + SSH limit + Docker bind inventory. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# UFW — Audit Report

## Host

- hostname:
- sshd_port:

## Defaults

- incoming: deny
- outgoing: allow
- routed: deny

## Rules

| from | port | action | comment |
|------|------|--------|---------|
| anywhere | 22022/tcp | limit | sshd rate-limit |
| Cloudflare IPs | 443/tcp | allow | proxy only |

## Docker binds

| service | bind | port |
|---------|------|------|
| postgres | 127.0.0.1 | 5432 |
| redis | 127.0.0.1 | 6379 |

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
