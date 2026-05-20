---
slug: sdd-workflow-overview
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Specification-Driven Development: intent is the source of truth.
content_id: "5e85d5ebf87fde25"
tags: [sdd, specification, workflow, planning, quality-gates]
---
# SDD Workflow Overview

## Summary

**One-sentence:** Specification-Driven Development: intent is the source of truth.

**One-paragraph:** Specification-Driven Development: intent is the source of truth. The complete phase sequence is CONSTITUTION → SPEC → DESIGN → TEST-PLAN → IMPL-PLAN → TASKS → EXECUTE → REVIEW → DONE. Spec answers WHAT to build, design answers HOW, test-plan answers HOW to verify (written before impl-plan). Each phase transition requires a confidence threshold (90%+ for spec→design, 95%+ for plan→execute). The "15-minute waterfall" variant covers medium tasks: 5min spec, 5min design, 5min task list.

## Applies If (ALL must hold)

- Multi-day features or anything requiring cross-module coordination
- AI-assisted development where reducing hallucinations is critical
- Production systems requiring quality assurance and audit trail
- Team collaboration requiring shared understanding of requirements

## Skip If (ANY kills it)

- Tasks under 2 hours with a clear implementation path — direct implementation
- Exploratory prototypes where code is discarded — spike with throwaway code
- Bug fixes with clear root cause — fix + test
- Project has no .aidocs/ structure and no bandwidth to set it up — use 15-minute waterfall

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
