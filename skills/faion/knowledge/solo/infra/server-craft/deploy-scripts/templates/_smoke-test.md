<!-- purpose: Minimum viable filled-in deploy audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Deploy Script — Audit Report

## Project

- name: faion-net-api
- repo: faionfaion/faion-net
- runtime_dir: /srv/faion-net-api/current
- workspace_dir: ~/workspace/projects/faion-net/faion-net-be

## Checklist

- [x] `set -euo pipefail` at top
- [x] pre-deploy lint (ruff) + tests (pytest -x) gate
- [x] rsync to /srv/faion-net-api/releases/<ts> then mv current -> ts
- [x] systemd reload faion-net-api
- [x] post-deploy smoke (HTTP 200 from /health)
- [x] current/previous symlink scheme
- [x] rollback = `cd /srv/.../releases && ln -sfn previous current && systemctl reload`

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
