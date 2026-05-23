# ADR Supersession Detection

## Summary

**One-sentence:** Produces a report of ADRs likely superseded by newer decisions, by comparing evidence anchors and decision context across the ADR corpus.

**One-paragraph:** ADR Supersession Detection produces a report that fixes a recurring decision in the sdlc-ai domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Quarterly ADR hygiene: знайти, що застаріло.
- Onboarding: junior не читає obsolete ADR.
- Audit prep: показати regulator clean ADR set.
- Pre-RFC check: можливо існуючий ADR покриває.
- Decision graph integrity: superseded → linked.

## Applies If (ALL must hold)

- ADR corpus has ≥10 entries.
- ADRs follow a parseable template (MADR / Nygard).
- Quarterly review cadence exists.

## Skip If (ANY kills it)

- ADR corpus < 10 entries — manual review faster.
- ADRs are free-form prose and cannot be parsed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ADR directory | Markdown set | architect |
| Evidence anchor inventory | JSON | faion-network |
| Detection thresholds | YAML | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[adr-consequence-evidence-binding]] | supersession compares evidence anchors across ADRs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/05-examples.xml` | supplemental | One worked example end-to-end | 400 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-adr-supersession-detection` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/supersession-report.md` | Markdown report listing candidate pairs with overlap % |
| `templates/supersession.schema.json` | JSON Schema for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-adr-supersession-detection.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[adr-consequence-evidence-binding]]
- [[adr-ai-drafted-with-review]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
