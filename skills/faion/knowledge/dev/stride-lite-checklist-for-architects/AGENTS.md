# STRIDE Lite Checklist for Architects

## Summary

**One-sentence:** Lite STRIDE checklist tuned for an architect reviewing a new dependency or service-edge: six categories, observable signals, fix-now-or-defer verdict per row.

**One-paragraph:** Lite STRIDE checklist tuned for an architect reviewing a new dependency or service-edge: six categories, observable signals, fix-now-or-defer verdict per row. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-stride-lite-checklist-for-architects.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Архітектор робить security review нової vendor-dep / нового service edge за <60 хв.
- Trust boundary змінюється (new ingress, new third-party API, new auth surface).
- Procurement gate потребує threat-model artefact, але повна STRIDE workshop overkill.
- Repeatable cadence (weekly arch review) де lite checklist масштабується краще за full TM.

## Applies If (ALL must hold)

- New dependency, new service edge, or new trust boundary in scope
- Architect has ≤60 minutes for the review
- Service has a defined data flow (request → handler → store / external)
- Verdict will be acted on (fix-now ticket or accepted-risk decision-record)

## Skip If (ANY kills it)

- Full multi-day threat-model session already scheduled — use STRIDE not Lite
- No trust boundary change in scope — checklist would surface zero findings
- Regulated context (PCI / HIPAA / FedRAMP) — Lite is insufficient evidence
- Service has no data flow defined yet — model the flow first, then run checklist

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-stride-lite-checklist-for-architects` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/checklist.json` | JSON instance with per-item pass/fail |
| `templates/checklist.md` | Markdown checklist matching the rule set |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stride-lite-checklist-for-architects.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[stride-threat-model-template]]
- [[trust-boundary-diff-helper]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
