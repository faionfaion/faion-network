---
slug: team-rfc-process-for-devs
tier: pro
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Dev-scope RFC template + lifecycle (draft → review → accepted/rejected → archived) for P6 product-team devs, with review-SLA and archive-not-delete discipline.
content_id: "b2d07dc364d3c85d"
complexity: medium
produces: spec
est_tokens: 4800
tags: [rfc, design-doc, process, product-team]
---
# Team RFC Process for Devs

## Summary

**One-sentence:** Dev-scope RFC template + lifecycle (draft → review → accepted/rejected → archived) for P6 product-team devs, with review-SLA and archive-not-delete discipline.

**One-paragraph:** Dev-scope RFC template + lifecycle (draft → review → accepted/rejected → archived) for P6 product-team devs, with review-SLA and archive-not-delete discipline. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-team-rfc-process-for-devs.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- P6 product-team dev пропонує refactor / arch change з блок-радіусом >1 sprint.
- Multiple devs мають opine на design (≥3 review signatures для accept).
- Async-first team без shared whiteboard — text-based design doc is the medium.
- Архів rejected RFCs має value (futures дискусій повертаються до тих самих питань).

## Applies If (ALL must hold)

- Team ≥4 devs and design discussions span multiple sessions
- Async-first communication (text-doc-driven, not whiteboard-driven)
- Repo / wiki supports a /rfcs/ folder with status lifecycle
- Review-SLA agreed (e.g. 5 working days from review-open to accept/reject)

## Skip If (ANY kills it)

- Solo dev / pair team — RFC overhead exceeds the design conversation cost
- Design <1-day spike — pull-request description is enough
- Team rejects async-first culture — RFCs sit unreviewed
- No archive discipline (deletes rejected RFCs) — future devs re-debate same designs

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
| `content/05-examples.xml` | medium | One worked example end-to-end (filled artefact) | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-team-rfc-process-for-devs` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-rfc-process-for-devs.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[team-conventions-as-code]]
- [[stack-mandate-tradeoff-frame]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
