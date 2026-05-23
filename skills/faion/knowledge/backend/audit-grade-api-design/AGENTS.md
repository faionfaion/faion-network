# Audit-Grade API Design

## Summary

**One-sentence:** Produces an audit-grade API spec: contract, error taxonomy, auth model, pagination, rate-limit, versioning, deprecation policy.

**One-paragraph:** Produces an audit-grade API spec: contract, error taxonomy, auth model, pagination, rate-limit, versioning, deprecation policy. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Зовнішнє API з contractual SLA: контракт, error taxonomy, auth, pagination, rate limits — всі formal.
- Підготовка до SOC2 / ISO аудиту: всі decisions traceable.
- Versioning з breaking-change discipline і deprecation policy.

## Applies If (ALL must hold)

- API is consumed by external partners or under contractual SLA.
- Org is preparing for SOC2 / ISO / regulatory audit.
- API will be versioned with breaking-change discipline.

## Skip If (ANY kills it)

- Internal-only API with no external consumers.
- Prototype / spike not yet stabilized.
- Webhook / fire-and-forget channel without request/response semantics.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Use case list with consumer personas | markdown | product |
| Auth model decision | markdown | security |
| Existing contracts (OpenAPI / proto) | yaml / proto | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[audit-grade-code-review-checklist]] | Reviewers will check the API code against the spec at review time |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
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
| `templates/api-spec.md` | Audit-grade API spec skeleton with contract + auth + pagination + error sections |
| `templates/openapi.yaml` | OpenAPI 3 skeleton matching the spec |
| `templates/deprecation-policy.md` | Deprecation policy template |
| `templates/_smoke-test.md` | Filled-in spec for a payments-create endpoint |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-audit-grade-api-design.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[audit-grade-code-review-checklist]]
- [[architecture-proposal-document-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
