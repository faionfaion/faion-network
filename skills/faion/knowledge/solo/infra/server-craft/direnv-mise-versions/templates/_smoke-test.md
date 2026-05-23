<!-- purpose: Minimum viable filled-in env audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Direnv + Mise — Audit Report

## Repo

- repo: faion-net-be
- branch: main

## Files

- [x] .mise.toml committed with `python = "3.12"`
- [x] .envrc committed with `use mise`
- [x] direnv allow run
- [x] mise trust run

## Verify

- `mise current` → python 3.12.7
- `python --version` → Python 3.12.7

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
