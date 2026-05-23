<!-- purpose: Minimum viable filled-in UFW audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# UFW — Audit Report

## Host

- hostname: faion-net
- sshd_port: 22022

## Defaults

- incoming: deny
- outgoing: allow
- routed: deny

## Rules

| from | port | action | comment |
|------|------|--------|---------|
| anywhere | 22022/tcp | limit | sshd rate-limit |
| Cloudflare IPv4 | 443/tcp | allow | proxy only |
| Cloudflare IPv6 | 443/tcp | allow | proxy only |

## Docker binds

| service | bind | port |
|---------|------|------|
| postgres | 127.0.0.1 | 5432 |
| redis | 127.0.0.1 | 6379 |

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
