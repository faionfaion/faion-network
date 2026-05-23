# KPI Drift Alarm Template

## Summary

**One-sentence:** Lightweight KPI drift alarm: baseline window, deviation threshold, alert routing, suppression window, escalation path; runs against any time-series KPI.

**One-paragraph:** KPI Drift Alarm Template pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Outsource engagement where BA reports KPIs to a client weekly.
- Product team tracking activation / retention / monetisation KPIs.
- Compliance KPIs (security incidents, audit pass rate, MTTR).
- Marketing KPIs (CAC, payback, LTV) where drift erodes margin silently.

## Applies If (ALL must hold)

- Engagement tracks at least 3 KPIs with weekly / monthly cadence.
- Stakeholders need to be alerted to drift before the next review meeting.
- Data is accessible programmatically (warehouse, API, CSV export).
- There is at least one prior incident where drift was caught late.

## Skip If (ANY kills it)

- KPIs are reviewed daily in person — alarm overhead is wasted.
- Data lacks history (less than 4 cycles) — baseline is unreliable.
- Team is too small to act on alarms (no on-call coverage).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| KPI catalogue | yaml | BA / product |
| Historical data (at least 4 cycles) | csv / sql | Warehouse |
| Alert routing config (email / Slack / TG) | yaml | Comms infra |
| On-call schedule | yaml | Team ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-kpi-drift-alarm-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/kpi-drift-alarm-template.yaml` | YAML config skeleton with required keys |
| `templates/kpi-drift-alarm-template.schema.json` | JSON Schema for the config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kpi-drift-alarm-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
