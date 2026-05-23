# Senior Promotion Case Template (Outsource Shop)

## Summary

**One-sentence:** Produces a defensible promotion case for senior-track promotions in an outsource/agency context with client-billable evidence.

**One-paragraph:** Produces a defensible promotion case for senior-track promotions in an outsource/agency context with client-billable evidence. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Defensible promotion case для senior-track в outsource shop з billable rate ladder.
- Evidence з ≥2 client engagements (а не з internal projects).
- Reuseable pattern для всіх кандидатів циклу — однакова форма + якірі.

## Applies If (ALL must hold)

- Promotion track is up-or-stay (no down) in an outsource shop with billable rate ladder.
- Promotion committee requires evidence of impact across ≥2 client engagements.
- Candidate has ≥18 months tenure in the prior level.

## Skip If (ANY kills it)

- Product / in-house promotion — different ladder semantics.
- Lateral move, not promotion — use scope-change template instead.
- Candidate is <12 months in the prior level — table the case.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Candidate self-assessment | markdown | candidate |
| Manager calibration notes | markdown | manager |
| Client-billable evidence per engagement | markdown / tickets / artefacts | delivery records |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[structured-interview-design]] | Promotion committee uses similar calibrated scoring patterns as hiring |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 4-step procedure with input/action/output per step | 1000 |
| `content/05-examples.xml` | reference | One full worked example end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/promotion-case-spec.md` | Promotion case skeleton: scope/impact/judgment/leadership × engagement |
| `templates/evidence-tracker.md` | Per-engagement evidence tracker for live data collection |
| `templates/_smoke-test.md` | Filled-in case for a Mid → Senior Engineer promotion |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-senior-promotion-case-template-outsource-shop.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[structured-interview-design]]
- [[star-interview-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
