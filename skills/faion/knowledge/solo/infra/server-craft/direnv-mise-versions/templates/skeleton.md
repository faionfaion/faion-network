<!-- purpose: Per-project env audit listing .mise.toml + .envrc + verify steps. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Direnv + Mise — Audit Report

## Repo

- repo:
- branch:

## Files

- [ ] .mise.toml committed with `python = "3.X"` (etc.)
- [ ] .envrc committed with `use mise`
- [ ] .envrc trusted via `direnv allow`
- [ ] .mise.toml trusted via `mise trust`

## Verify

- `mise current` → matches .mise.toml
- `python --version` (in repo) → matches

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
