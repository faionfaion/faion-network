---
slug: yaml-frontmatter
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: YAML frontmatter is a metadata block (`---` delimited) at the top of Markdown/MDX files that provides structured, machine-readable data about the document.
content_id: "a49818c57b9c3831"
tags: [metadata, yaml, frontmatter, schema]
---
# YAML Frontmatter Standards

## Summary

**One-sentence:** YAML frontmatter is a metadata block (`---` delimited) at the top of Markdown/MDX files that provides structured, machine-readable data about the document.

**One-paragraph:** YAML frontmatter is a metadata block (`---` delimited) at the top of Markdown/MDX files that provides structured, machine-readable data about the document. Every SDD document must include frontmatter with typed fields (type, version, status, created) following the project's canonical schema defined in constitution.md.

## Applies If (ALL must hold)

- Generating any new SDD document (spec, design, task, roadmap, constitution)
- Integrating docs with a static site generator (Astro, Hugo, MkDocs) that reads frontmatter
- Setting up CI validation to enforce consistent metadata across `.aidocs/`
- Writing a script or agent tool that filters or routes documents by status or priority

## Skip If (ANY kills it)

- `AGENTS.md`, `CLAUDE.md`, `README.md` files — these have no lifecycle metadata by convention
- Configuration files using YAML as their primary format (use `.env` or proper config files)
- Deeply nested hierarchical data — frontmatter handles flat/shallow metadata; complex relations belong in the document body

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

- parent skill: `solo/sdd/sdd/`
