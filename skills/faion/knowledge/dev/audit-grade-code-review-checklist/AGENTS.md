# Audit-Grade Code Review Checklist

## Summary

**One-sentence:** Per-PR audit-grade checklist: contract conformance, error handling, secret hygiene, auth scope, logging, performance, tests.

**One-paragraph:** Per-PR audit-grade checklist: contract conformance, error handling, secret hygiene, auth scope, logging, performance, tests. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Defensible PR review evidence для SOC2 / ISO audit.
- Inter-reviewer consistency через checklist (а не 'looks fine to me').
- Розширення junior reviewers до audit-grade рівня через явні check items.

## Applies If (ALL must hold)

- Codebase is under SOC2 / ISO scope or has external SLA.
- Org wants traceable PR review evidence for audit.
- Reviewer pool is ≥2 to enable independent verification.

## Skip If (ANY kills it)

- Throwaway prototype / spike branch.
- Documentation-only PRs (still review, but lightweight).
- Single-reviewer setup — checklist value is reduced.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| API spec (if applicable) | markdown / openapi | audit-grade-api-design |
| Logging + secret-handling policy | markdown | security |
| Test coverage target | policy | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[audit-grade-api-design]] | Checklist references the API contract for conformance items |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `fill-template` | haiku | Mechanical template fill with bounded inputs |
| `apply-rubric` | sonnet | Per-instance judgment against calibrated anchors |
| `cross-check-evidence` | sonnet | Verify each claim cites an input artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/review-checklist.md` | Per-PR audit checklist with sections per concern |
| `templates/review-evidence-log.md` | Log capturing reviewer + timestamp + check pass/fail per PR |
| `templates/_smoke-test.md` | Filled-in checklist for a small payments PR |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-audit-grade-code-review-checklist.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[audit-grade-api-design]]
- [[architecture-review-meeting-facilitation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
