---
slug: language-framework-guide
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a stack-selection report — one primary recommendation + two alternatives + ADR stub — mapped from project type, team profile, and runtime constraints to the canonical language/framework pair.
content_id: "dbbfc8d00bed04e4"
complexity: light
produces: report
est_tokens: 3000
tags: [adr, stack-selection, framework, language, decision]
---
# Language & Framework Guide

## Summary

**One-sentence:** Produces a stack-selection report — one primary recommendation + two alternatives + ADR stub — mapped from project type, team profile, and runtime constraints to the canonical language/framework pair.

**One-paragraph:** Tier-0 decision router for stack selection. Given a project brief, map task type to canonical language (Python, TypeScript, Go, Rust) and framework (Django, FastAPI, React, Next.js). For solo/founder projects, prefer Python (FastAPI or Django) or TypeScript (Next.js) — broadest LLM training coverage, fewer agent mistakes. Use ruff for Python; biome or prettier+eslint for JS/TS. Every selection produces a primary recommendation, two alternatives, and an ADR stub with Status/Context/Decision/Alternatives/Consequences. Stacks lasting > 6 months require human sign-off on the ADR before implementation.

**Ефективно для:** new project kickoff, refactors where the existing stack is misaligned with team or workload, decisions on adding a new language to a polyglot org, "should we adopt Rust" questions answered with ADR-grade evidence.

## Applies If (ALL must hold)

- A new project or component needs a language/framework decision documented.
- Project longevity is >= 3 months (long enough for the choice to matter).
- Team can write or accept an ADR (Architectural Decision Record).
- Recommendation will be filed into a public/internal decision log.

## Skip If (ANY kills it)

- One-day scripts or POCs where the choice is reversible in an hour.
- Mandated stack — team has no decision authority (corporate standard).
- Existing greenfield repo where the choice is already made.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Project brief | Markdown (≤1 page) | PM/product ticket |
| Team profile | bullet list (skills, headcount) | HR / lead |
| Runtime constraints | bullet list (latency target, deployment env) | infra/SRE ADR |
| 6-month outlook | yes/no | roadmap |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[files-reference]]` | After choosing a language, route into the language-specific methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: canonical mapping, solo-prefers-Python/TS, framework picks, ruff/biome, three-options output, ADR for 6mo+ | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for the recommendation report + ADR stub shape | ~600 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: stack-name-only output, hype-driven choice, no alternatives evaluated | ~500 |
| `content/05-examples.xml` | light | Two worked recommendations | ~600 |
| `content/06-decision-tree.xml` | essential | Root: "Is project type known and longevity >= 3 months?" | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Map brief to canonical stack | sonnet | Lookup table + small reasoning. |
| Generate ADR stub | sonnet | Template-driven. |
| Compare alternatives | opus | Multi-factor tradeoff reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-stub.md` | ADR template (Status, Context, Decision, Alternatives, Consequences). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-language-framework-guide.py` | Validates that a recommendation report contains primary + 2 alternatives + ADR fields. | Post-recommendation, pre-merge. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[files-reference]]` — routes into language-specific methodology after the pick
- `[[methodologies]]` — keyword dispatcher complement

## Decision tree

The decision tree at `content/06-decision-tree.xml` checks project longevity, team skills, and runtime constraints; gates whether the methodology applies (longer projects only) and whether an ADR is required.
