# HIPAA BAA Vendor Checklist

## Summary

**One-sentence:** Pre-engagement HIPAA Business Associate Agreement (BAA) checklist for every PHI-touching vendor: data flow, breach notification, sub-processor map, audit rights.

**One-paragraph:** HIPAA BAA Vendor Checklist pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- HealthTech outsource engagement onboarding a new SaaS vendor.
- M&A due-diligence of a target company's BAA portfolio.
- Audit prep where every vendor must surface a signed BAA.
- Migration where PHI flows shift across vendors.

## Applies If (ALL must hold)

- Engagement involves Protected Health Information (PHI) or US-regulated health data.
- A third-party vendor will store, process, or transmit PHI on the client's behalf.
- Client is a US Covered Entity (CE) or Business Associate (BA) under HIPAA.
- Vendor onboarding is upcoming or under review.

## Skip If (ANY kills it)

- No PHI in scope — engagement is purely structural / financial data.
- Vendor is being de-onboarded — different checklist applies.
- Client is non-US and HIPAA does not apply — use local regime checklist instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Vendor name + service description | markdown | Procurement |
| Data flow diagram (PHI surfaces) | diagram | Security / BA |
| Existing BAA (if any) | pdf | Legal |
| Sub-processor list | csv | Vendor disclosure |

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
| `draft-hipaa-baa-vendor-checklist` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hipaa-baa-vendor-checklist.md` | Markdown checklist skeleton matching the 8-item shape pinned in content/01-core-rules.xml |
| `templates/hipaa-baa-vendor-checklist.schema.json` | JSON Schema for the structured checklist output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hipaa-baa-vendor-checklist.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
