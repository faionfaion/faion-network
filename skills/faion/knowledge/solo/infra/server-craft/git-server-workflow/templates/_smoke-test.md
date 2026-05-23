<!-- purpose: Minimum viable filled-in workflow audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Git Server Workflow — Audit Report

## Project

- name: faion-net-api
- source: ~/workspace/projects/faion-net/faion-net-be
- runtime: /srv/faion-net-api/current

## Discipline

- [x] no live edits in /srv
- [x] deploy-be.sh is the only boundary
- [x] git tags per release (v2026-05-23T10:00Z)
- [x] clean-tree pre-check
- [x] systemd service points at /srv/faion-net-api/current/.venv/bin/python

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
