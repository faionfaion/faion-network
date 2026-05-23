<!-- purpose: Minimum viable filled-in audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Bash Aliases — Audit Report

## Host

- hostname: faion-net
- shell: bash 5.2

## Categories present

- [x] system
- [x] git
- [x] docker
- [x] systemd
- [x] safety
- [x] modern-tools (gated)
- [x] completion-wired short aliases

## Findings

- F1 — safety flags present on rm/mv/cp — verified with `alias | grep -- -i`

## Recommendations

- R1 — wire `__git_complete g git` — owner @ruslan

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
