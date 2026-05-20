---
slug: methodologies-summary
tier: pro
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A routing index for all 33 methodologies in pro/product/product-manager/.
content_id: "c20b7901ab92a19e"
tags: [routing, product-manager, methodology-index, quick-reference, task-triage]
---
# Methodologies Summary (Product Manager)

## Summary

**One-sentence:** A routing index for all 33 methodologies in pro/product/product-manager/.

**One-paragraph:** A routing index for all 33 methodologies in pro/product/product-manager/. Not a methodology itself — it answers "which methodology do I need?" for a given PM task and returns a single slug. Read this first when entering product-manager scope without a specific methodology pinned; then load the chosen methodology's own AGENTS.md and execute.

## Applies If (ALL must hold)

- Cold start: agent has a PM task and no methodology is pre-selected.
- Task triage: deciding between RICE vs MoSCoW, MVP vs MLP, roadmap vs OKR, lifecycle vs feedback management.
- Onboarding a new PM or agent to the skill — first read to orient.
- Ambiguous task language: stakeholder said "prioritize" or "plan" without naming a framework.
- Multiple PM activities bundled in one request — split using the Quick Selection Guide before execution.

## Skip If (ANY kills it)

- Methodology already chosen — skip summary, go straight to that folder's AGENTS.md.
- Cross-skill work (BA, PM-agile, project-manager) — use the respective skill's own router.
- Execution or templates — look in the chosen methodology's own files, never here.
- Strategic/portfolio decisions across multiple products — escalate to product leader, not a single methodology.

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

- parent skill: `pro/product/product-manager/`
