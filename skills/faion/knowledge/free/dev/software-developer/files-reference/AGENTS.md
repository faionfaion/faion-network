---
slug: files-reference
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Catalog index of all methodology folders in the `software-developer` skill, grouped by language and domain (Python, Django, JavaScript/TypeScript, Go, Rust, Ruby, PHP, Java, C#, API Design, Testing, Frontend, Architecture, Dev Practices).
content_id: "50300ffd5cca02cc"
tags: [catalog, routing, index, software-developer]
---
# Software Developer Files Reference

## Summary

**One-sentence:** Catalog index of all methodology folders in the `software-developer` skill, grouped by language and domain (Python, Django, JavaScript/TypeScript, Go, Rust, Ruby, PHP, Java, C#, API Design, Testing, Frontend, Architecture, Dev Practices).

**One-paragraph:** Catalog index of all methodology folders in the `software-developer` skill, grouped by language and domain (Python, Django, JavaScript/TypeScript, Go, Rust, Ruby, PHP, Java, C#, API Design, Testing, Frontend, Architecture, Dev Practices). Used as a routing map: agent reads the topical section, picks the slug, then resolves the actual `[slug]/methodology.xml` path via `Glob`. The list predates the unified-XML restructure and may be stale — always verify existence with a filesystem lookup before loading a path.

## Applies If (ALL must hold)

- Routing step inside `software-developer` orchestrator: pick the topical section, then the slug.
- Building a documentation index or sidebar from the canonical catalog.
- Validating that referenced methodology folders exist before dispatching a task to a sub-agent.

## Skip If (ANY kills it)

- As a semantic search tool ("how do I handle errors?") — the list is name-based; use `Grep` over actual `methodology.xml` bodies.
- As an authoritative tier map — some entries listed here belong logically to other tiers; trust the directory tree at `skills/faion/knowledge/<tier>/<group>/<domain>/<slug>/`.
- Dumping the full catalog into a sub-agent prompt — it is too large; filter to one topical section only.

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

- parent skill: `free/dev/software-developer/`
