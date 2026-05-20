---
slug: api-versioning
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for managing breaking changes in HTTP APIs.
content_id: "e31f4452a1dc2292"
tags: [api, versioning, rest, deprecation, breaking-changes]
---
# API Versioning

## Summary

**One-sentence:** A methodology for managing breaking changes in HTTP APIs.

**One-paragraph:** A methodology for managing breaking changes in HTTP APIs. Use URL path versioning (/api/v1/, /api/v2/) for public REST APIs. Announce deprecation via Deprecation, Sunset, and Link: rel="successor-version" headers at least 180 days before removal. Classify every change as additive (no bump), behavioral (warn), or breaking (new version). Maintain at least two concurrent versions; implement v(n+1) atop shared services, never by copying v(n) handlers.

## Applies If (ALL must hold)

- Public APIs with external consumers who can't deploy atomically with you
- Mobile apps where old client versions stay in the wild for months
- B2B integrations where SDKs are pinned per customer
- Any breaking change to a stable resource shape, status code, or auth scheme
- LLM tool-use — pin a stable version so the agent's tool schema keeps working

## Skip If (ANY kills it)

- Internal-only APIs where you control all consumers and can deploy atomically — use expand-then-contract without versions
- Pre-1.0 / pre-launch — commit to v1 only when an external user exists
- Pure additive changes (new optional field, new endpoint) — no version bump needed
- Experimental endpoints behind feature flags — the flag is the version axis

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

- parent skill: `solo/dev/software-developer/`
