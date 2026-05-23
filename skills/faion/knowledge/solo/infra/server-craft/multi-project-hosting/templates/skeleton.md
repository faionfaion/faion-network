<!-- purpose: Multi-project audit listing port ranges + isolation + vhost coverage. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Multi-Project Hosting — Audit Report

## Port registry

| project | range | services | nginx vhost |
|---------|-------|----------|-------------|
| project-a | 8000-8099 | api(8000), worker(8001) | site-a.conf |
| project-b | 8100-8199 | api(8100) | site-b.conf |

## Isolation

- per-project user: yes/no
- /srv/<project>/ root: yes
- systemd-user per project: yes

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
