---
slug: multi-machine-offline-cache
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Per-machine cache, deterministic offline fallback, license-aware re-activation for the faion CLI on outsource-specialist setups (laptop + workstation + client laptop).
content_id: "8d939f0d7c04ecd5"
tags: [multi-machine-offline-cache, infra, pro]
---

# Multi-Machine Offline Cache

## Summary

**One-sentence:** Per-machine cache, deterministic offline fallback, license-aware re-activation for the faion CLI on outsource-specialist setups (laptop + workstation + client laptop).

**One-paragraph:** Outsource specialists work from laptop + workstation + sometimes client-issued machine. Faion CLI must support per-machine cache, deterministic offline fallback, license-aware re-activation. Methodology + CLI capability missing. Output: cache layout + sync protocol + license rules.

## Applies If (ALL must hold)

- user works on ≥2 machines
- user expects CLI to function offline (flight, no-internet client site)
- license model includes per-machine activation count

## Skip If (ANY kills it)

- single-machine user — out of scope
- fully cloud-hosted dev environment (Codespaces / Devbox) — different sync model
- license is unlimited devices — no activation logic needed

## Prerequisites

- list of machines + roles (primary, secondary, client)
- CLI version supporting offline cache
- license token / refresh-token storage spec

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent skill — provides operating context for this methodology |
| `solo/infra/server-craft` | peer methodology — produces inputs or consumes outputs |
| `pro/sec/secrets-rotation-end-to-end` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodology: `solo/infra/server-craft`
- peer methodology: `pro/sec/secrets-rotation-end-to-end`
- external: https://github.com/sigstore/cosign (offline verification); https://en.wikipedia.org/wiki/Software_license_management
