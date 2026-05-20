---
slug: quality-management
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A three-process framework (Plan Quality → Manage Quality → Control Quality) applied as code-driven gates: DoD checked per PR by an automated validator, defect metrics aggregated weekly by a collector agent, and severity classified by a triager with human confirmation.
content_id: "d318ef649fa64829"
tags: [quality-management, definition-of-done, defect-management, quality-metrics, testing]
---
# Quality Management

## Summary

**One-sentence:** A three-process framework (Plan Quality → Manage Quality → Control Quality) applied as code-driven gates: DoD checked per PR by an automated validator, defect metrics aggregated weekly by a collector agent, and severity classified by a triager with human confirmation.

**One-paragraph:** A three-process framework (Plan Quality → Manage Quality → Control Quality) applied as code-driven gates: DoD checked per PR by an automated validator, defect metrics aggregated weekly by a collector agent, and severity classified by a triager with human confirmation. Quality is built in, not tested in — prevention over detection is the operative principle (Deming).

## Applies If (ALL must hold)

- Setting Definition of Done across a multi-team or multi-repo product.
- Defect-escape rate climbing or production incidents recurring on the same surfaces.
- Codebase has no quality dashboard and PM/PO cannot answer whether the trend is improving.
- Pre-release hardening: agent-driven quality audit before a major launch.
- Compliance kickoff (SOC2, ISO 9001) where evidence trail must be reproducible.

## Skip If (ANY kills it)

- One-person prototype before product-market fit — quality gates slow validation loops.
- Spike or research code marked throwaway — formal QC inflates effort 2-3x.
- When the team rejects DoD as ceremony — fix the trust issue first, then introduce gates.
- For aesthetic UX polish — use design review, not quality management process.

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

- parent skill: `pro/pm/project-manager/`
