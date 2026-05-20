---
slug: requirements-traceability
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Without typed traceability, changed requirements cause unknown downstream impact and auditors cannot verify completeness.
content_id: "5c8b6df0fd700d15"
tags: [traceability, rtm, requirements, coverage, impact-analysis]
---
# Requirements Traceability

## Summary

**One-sentence:** Without typed traceability, changed requirements cause unknown downstream impact and auditors cannot verify completeness.

**One-paragraph:** Without typed traceability, changed requirements cause unknown downstream impact and auditors cannot verify completeness. Use five typed link roles: satisfies, derives, implements, verifies, conflicts. Generate RTM from frontmatter; never hand-edit. Track three gates: forward (≥95%), backward (100%), horizontal (zero cycles).

## Applies If (ALL must hold)

- Pre-audit, pre-release, or before a major refactor: needs a single defensible coverage answer
- Designing a new RTM schema from scratch: deciding which artifact types are nodes and which link roles are allowed
- Migrating from spreadsheet RTMs to requirements-as-code (frontmatter links)
- Teaching subagents what "satisfies", "derives", "verifies" mean before letting them propose links
- Lightweight projects where generated matrix from typed markdown links covers the audit surface

## Skip If (ANY kills it)

- You only need tool/vendor guidance — use the sibling `business-analyst/requirements-traceability/`
- Discovery or pre-PMF: lock-in of an RTM encodes premature decisions
- One-shot prototypes, internal scripts, throwaway spikes — overhead exceeds value
- Team will not enforce link discipline — an out-of-date matrix is worse than none
- Pure SLO/SRE work where the trace artifact is a dashboard alert rule, not a requirement

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

- parent skill: `pro/ba/ba-core/`
