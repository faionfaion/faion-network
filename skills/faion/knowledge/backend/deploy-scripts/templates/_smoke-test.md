<!-- purpose: Minimum viable filled-in deploy audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Deploy Script — Audit Report

## Project

- name: example-api
- repo: acme/example-api
- runtime_dir: /srv/example-api/current
- workspace_dir: ~/workspace/projects/example-api

## Checklist

- [x] `set -euo pipefail` at top
- [x] pre-deploy lint (ruff) + tests (pytest -x) gate
- [x] rsync to /srv/example-api/releases/<ts> then mv current -> ts
- [x] systemd reload example-api.service
- [x] post-deploy smoke (HTTP 200 from /health)
- [x] current/previous symlink scheme
- [x] rollback = `cd /srv/.../releases && ln -sfn previous current && systemctl reload`

**Owner:** @handle (founder)  •  **Reviewed:** 2026-05-23
