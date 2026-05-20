---
slug: lint-megalinter-polyglot
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Polyglot repositories (three or more languages, e.
content_id: "4c3a7beeccaceec4"
tags: [lint, megalinter, ci, polyglot, sarif]
---
# MegaLinter as the Polyglot Quality Umbrella in CI

## Summary

**One-sentence:** Polyglot repositories (three or more languages, e.

**One-paragraph:** Polyglot repositories (three or more languages, e.g., Python + TypeScript + Terraform + Markdown) MUST run MegaLinter in CI as a single GitHub Action or GitLab job. MegaLinter auto-detects the languages present, dispatches 100+ underlying linters in parallel via Python multiprocessing, and emits a unified SARIF report so the agent and the security UI both consume one feed. Pick a flavor (security, python, javascript, terraform, dotnet, cupcake) to keep the runner image lean. MegaLinter MUST NOT run as a pre-commit hook — its image is too heavy for the local commit lifecycle; reserve it for CI and let per-language tools (ruff, biome) cover the local hook floor.

## Applies If (ALL must hold)

- Polyglot repositories with three or more languages or stack zones (Python + TS + Terraform + Markdown is the canonical example).
- Monorepos where each package may use different linters and a single CI job is simpler than per-language workflow shards.
- Repositories that need uniform SARIF output for GitHub Advanced Security or GitLab UltimateSecurity.
- Quarterly hygiene scans that want every linter in one report without per-tool maintenance.

## Skip If (ANY kills it)

- Single-language repositories — ruff (Python), biome (JS/TS), or golangci-lint (Go) cover the same ground with sub-second startup; MegaLinter's image overhead dwarfs the value.
- Local pre-commit hooks — MegaLinter's image is multi-gigabyte and adds tens of seconds of pull/start time, breaking the sub-second hook contract.
- Throwaway prototype repos with one or two files of code — install ruff or biome and stop.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
