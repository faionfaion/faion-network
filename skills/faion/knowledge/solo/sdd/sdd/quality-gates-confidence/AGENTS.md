---
slug: quality-gates-confidence
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Six sequential quality gate levels (L1-L6) prevent defects from propagating through SDD phases.
content_id: "b93c384fef5e89ea"
tags: [quality-gates, testing, validation, confidence, ci-cd]
---
# Quality Gates & Confidence Checks

## Summary

**One-sentence:** Six sequential quality gate levels (L1-L6) prevent defects from propagating through SDD phases.

**One-paragraph:** Six sequential quality gate levels (L1-L6) prevent defects from propagating through SDD phases. Each gate has a minimum confidence threshold that blocks progression when not met: L1 syntax/format (95%), L2 unit tests (90%), L3 integration tests (85%), L4 code review (80%), L5 staging (85%), L6 production (90%). Confidence score = Automated_Pass × 0.4 + Coverage × 0.2 + Risk_Mitigation × 0.2 + Traceability × 0.2. LLM-generated code enters the L1→L2 validation pipeline immediately after generation; failures trigger targeted re-prompt loops capped at 3 attempts before human escalation.

## Applies If (ALL must hold)

- Before any phase transition in the SDD workflow — confidence check gates progression
- After LLM-generated code is produced — run L1 and L2 before human review
- Setting up CI/CD for an LLM-assisted project — quality gates are the automated enforcement layer
- When using LLM-as-judge to evaluate AI output before integration
- When change failure rate spikes — tighten gate enforcement (soft block → hard block)

## Skip If (ANY kills it)

- Trivial configuration changes — full L1-L6 wastes time
- Exploratory prototypes that will be discarded — gate overhead exceeds learning value
- When gate tooling is not set up (no linter config, no test suite) — set up tooling first
- L5/L6 for local development — these are deployment gates, not development gates

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
