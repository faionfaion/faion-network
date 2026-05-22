---
slug: user-research-at-scale
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An operating model for running research in parallel with product velocity using AI-augmented pipelines: automated transcription, agent-driven tagging and clustering, human verification on a sampled 10%, and a repository as the single source of truth.
content_id: "6ff97c201f0b5419"
tags: [user-research, ai-augmented, research-operations, transcription, tagging]
---
# User Research at Scale

## Summary

**One-sentence:** An operating model for running research in parallel with product velocity using AI-augmented pipelines: automated transcription, agent-driven tagging and clustering, human verification on a sampled 10%, and a repository as the single source of truth.

**One-paragraph:** An operating model for running research in parallel with product velocity using AI-augmented pipelines: automated transcription, agent-driven tagging and clustering, human verification on a sampled 10%, and a repository as the single source of truth. Humans own study design, ethics, interpretation, and stakeholder framing; agents own transcription, tagging, clustering, and report drafting.

## Applies If (ALL must hold)

- Product velocity outpaces a single research team — multiple squads need findings same-week, not month-later.
- Continuous-discovery operating model where every PM/designer is expected to run small studies, with researchers as enablers.
- High-volume unmoderated testing programmes (1k+ recordings/quarter) where AI-assisted analysis is a force multiplier.
- Multinational rollouts that require parallel sessions across regions/locales.
- Mature ResearchOps practice with a repository, intake, and recruitment infrastructure already in place.

## Skip If (ANY kills it)

- Pre-PMF startups with fewer than 50 paying users — qualitative depth from a researcher trumps scale.
- Studies requiring sensitive populations (children, healthcare, accessibility) where panel quality and ethics review must dominate over throughput.
- Strategic generative research (problem framing) — small samples with senior researcher synthesis still wins.
- Regulated environments (HIPAA, GDPR with special-category data) where AI auto-tagging is restricted.

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

- parent skill: `pro/ux/user-researcher/`
