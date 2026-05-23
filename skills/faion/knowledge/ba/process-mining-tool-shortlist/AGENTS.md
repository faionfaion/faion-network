# Process Mining Tool Shortlist

## Summary

**One-sentence:** Decision-grade shortlist of process-mining tools (Celonis / UiPath PM / Disco / open-source) with weighted criteria, evidence anchors, and named owner.

**One-paragraph:** Process Mining Tool Shortlist pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Operational-excellence engagements requiring an ROI-grade tool pick.
- M&A or carve-out where two process-mining tools must converge.
- Compliance-driven mining (SOX, ISO 9001) needing auditable lineage.
- Open-source-first orgs evaluating PM4Py / ProM.

## Applies If (ALL must hold)

- Engagement scope includes a process-mining initiative of at least 4 weeks.
- Client has at least one event-log source (ERP, ticketing, BPM tool).
- Decision-makers need a defensible tool-pick before committing license / budget.
- Team has no incumbent process-mining tool.

## Skip If (ANY kills it)

- Engagement already mandates a specific tool (no choice exercised).
- Process scope is too small (single workflow with under 1000 events) — Excel suffices.
- Team lacks data-engineering capacity to ingest event logs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event-log sample | csv / xes | Client data team |
| Decision criteria draft | yaml | BA toolkit |
| Budget constraint | yaml | Client finance |
| Vendor reference contacts | csv | BA network / G2 |

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
| `content/05-examples.xml` | essential | Worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-process-mining-tool-shortlist` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/process-mining-tool-shortlist.md` | Markdown report skeleton with required sections + placeholders |
| `templates/process-mining-tool-shortlist.schema.json` | JSON Schema for the structured report output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-process-mining-tool-shortlist.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
