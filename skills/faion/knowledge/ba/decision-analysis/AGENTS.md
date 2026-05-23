# Decision Analysis

## Summary

**One-sentence:** Six-step structured evaluation (define → generate → weight → score → sensitivity → document) yielding an auditable decision record with traceability to elicited requirements and reconciled stakeholder weights.

**One-paragraph:** A six-step structured evaluation framework: define decision, generate options including status quo, elicit weights individually then reconcile, route scoring by expertise, run sensitivity analysis, document with traceability. Used for vendor/platform/package selection, build-vs-buy-vs-extend, regulated approval-gate decisions, and end-of-BA-cycle solution evaluation. Output is a decision record with weighted-score table, sensitivity report, and citation back to requirements.

**Ефективно для:**

- Vendor selection між 3+ кандидатами зі змішаними групами стейкхолдерів.
- Build/buy/extend з reconciled weights від Finance / Architecture / Security / Ops.
- Регульованих approval-gate рішень, де потрібен audit trail.
- Розблокування steerco, який сперечається інтуїціями замість критеріїв.

## Applies If (ALL must hold)

- Enterprise vendor/platform/package selection (CRM, ERP, ITSM, IdP) with 3+ candidates and 5–7 stakeholder groups.
- Build-vs-buy-vs-extend evaluations spanning Finance, Architecture, Security, Operations.
- Approval-gate decisions in regulated environments (banking, healthcare, gov) requiring documented rationale.
- Investment/portfolio prioritization where the same matrix template is reused across N initiatives.
- Solution evaluation at the end of a BA cycle comparing candidates against elicited requirements.
- Steering committee deadlock where members argue intuitions rather than criteria.

## Skip If (ANY kills it)

- Decisions inside one team's autonomy (npm package, CI runner version) — use a 5-line ADR.
- Pure financial decisions — use NPV/IRR/payback, not 1–5 scoring.
- Strategic direction questions — use scenario planning / BABOK strategy analysis.
- Decision-maker has already decided and asked for cover — retrofitted matrix is theater.
- Early discovery with high uncertainty — use opportunity-solution trees instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Decision statement | Markdown (outcome-shaped) | sponsor |
| Requirements catalog | YAML / Markdown | elicitation-techniques upstream |
| Stakeholder group list | JSON | stakeholder-analysis |
| Candidate options list | Markdown (must include status quo) | BA team |
| Weighting template | YAML | this methodology / templates |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/requirements-traceability` | Criteria trace back to BR-IDs. |
| `pro/ba/business-analyst/requirements-prioritization` | Provides criteria importance ordering. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `weight-elicitation` | sonnet | Light reasoning on per-stakeholder weights. |
| `weight-reconciliation` | opus | Deep cross-stakeholder synthesis; high stakes. |
| `score-by-expertise` | sonnet | Route each criterion to the right SME. |
| `sensitivity-analysis` | haiku | Mechanical Monte Carlo / one-at-a-time perturbation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-analysis-document.md` | Full decision record: statement, options, weights, scores, sensitivity, rationale, sign-off. |
| `templates/decision-matrix.md` | Weighted-score matrix skeleton (criteria × options). |
| `templates/weight-reconcile.py` | Reconcile per-stakeholder weight vectors; emits group weights + dispersion warning. |
| `templates/_smoke-test.md` | Minimum viable filled-in decision record. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-analysis.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[requirements-prioritization]]
- [[requirements-traceability]]
- [[modern-ba-framework]]
- [[knowledge-areas-detail]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
