---
slug: requirements-lifecycle
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A governance framework for managing requirements from initial capture through implementation and verification.
content_id: "f7993c25c1bff05e"
tags: [requirements, lifecycle, change-control, governance, compliance]
---
# Requirements Lifecycle Management

## Summary

**One-sentence:** A governance framework for managing requirements from initial capture through implementation and verification.

**One-paragraph:** A governance framework for managing requirements from initial capture through implementation and verification. Defines eight requirement states (Draft → Proposed → Approved → Implemented → Verified, plus Rejected/Deferred/Deleted), enforces change control via a formal change request process, and maintains version history for every requirement. Prevents uncontrolled scope changes and preserves the audit trail needed for compliance and retrospectives.

## Applies If (ALL must hold)

- Projects with formal change control requirements (regulated industries, government, enterprise IT)
- Long-running projects where requirements evolve over months and version drift is a real risk
- Teams where stakeholders or developers frequently bypass the BA to change requirements informally
- Compliance context (SOX, ISO, HIPAA) requiring a documented requirements audit trail
- Post-implementation review revealed implementation mismatches — lifecycle management prevents recurrence
- Integrating multiple delivery streams that each own a subset of requirements

## Skip If (ANY kills it)

- Early-stage discovery / hypothesis testing where requirements legitimately change every sprint — add lifecycle overhead only after problem-solution fit
- Tiny internal tools with a single stakeholder and a one-week delivery — a shared doc suffices
- Pure agile backlogs managed in Jira/Linear where the tool already enforces state — duplicate governance adds friction without value
- Throwaway prototypes — formal lifecycle governance is wasted on artifacts designed to be discarded

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

- parent skill: `pro/ba/business-analyst/`
