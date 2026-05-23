<!-- purpose: Minimum viable filled-in multi-project audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Multi-Project Hosting — Audit Report

## Port registry

| project | range | services | nginx vhost |
|---------|-------|----------|-------------|
| faion-net-api | 8000-8099 | api(8000) | api.faion.net.conf |
| faion-net-api-dev | 8100-8199 | api(8001) | api-dev.faion.net.conf |
| n8n | 8200-8299 | docker(8200) | n8n.faion.net.conf |

## Isolation

- per-project user: faion / nero / docker-host
- /srv/<project>/ root: yes
- systemd-user per project: yes

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
