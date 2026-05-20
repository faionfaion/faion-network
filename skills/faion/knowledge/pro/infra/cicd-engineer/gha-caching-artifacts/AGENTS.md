---
slug: gha-caching-artifacts
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cache dependency folders using actions/cache@v4 with lockfile-hash keys and ecosystem-specific restore-keys.
content_id: "fdd7714a7cc54467"
tags: [github-actions, caching, artifacts, ci, performance]
---
# GitHub Actions Caching and Artifacts

## Summary

**One-sentence:** Cache dependency folders using actions/cache@v4 with lockfile-hash keys and ecosystem-specific restore-keys.

**One-paragraph:** Cache dependency folders using actions/cache@v4 with lockfile-hash keys and ecosystem-specific restore-keys. Upload build outputs as artifacts with explicit retention-days. Never confuse caches (speed up builds, 7-day default) with artifacts (store outputs, 90-day default). Use type=gha cache for Docker Buildx layer caching.

## Applies If (ALL must hold)

- Any job that installs package dependencies (npm, pip, go mod, cargo, bundler).
- Jobs that build Docker images — use type=gha cache for layer reuse across runs.
- Build outputs that must be shared across jobs in the same run (use artifacts, not cache).
- Test reports, coverage files, compiled binaries that need to be downloadable after the run.

## Skip If (ANY kills it)

- Caching mutable state between runs where correctness depends on the latest state — caches are best-effort, not guaranteed to hit.
- Storing secrets or credentials in artifacts — artifacts are accessible to anyone with repo read access.
- Using artifacts for large binaries that are deployed via a registry — push to a container registry or S3 instead.

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

- parent skill: `pro/infra/cicd-engineer/`
