---
slug: tech-debt-cost-of-delay-scoring
tier: pro
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Cost-of-Delay rubric for tech-debt items: weekly bleed × time-criticality × business-value × ease, producing a comparable score for weekly prioritisation session.
content_id: "a590fc463d7ec76e"
complexity: medium
produces: rubric
est_tokens: 4100
tags: [tech-debt, cost-of-delay, scoring, prioritisation]
---
# Tech Debt Cost-of-Delay Scoring

## Summary

**One-sentence:** Cost-of-Delay rubric for tech-debt items: weekly bleed × time-criticality × business-value × ease, producing a comparable score for weekly prioritisation session.

**One-paragraph:** Cost-of-Delay rubric for tech-debt items: weekly bleed × time-criticality × business-value × ease, producing a comparable score for weekly prioritisation session. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-tech-debt-cost-of-delay-scoring.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Weekly arch review з 20+ tech-debt items конкуруючих за headcount.
- Eng leadership потребує comparable score (а не gut-feel ordering).
- Tech debt вже tracked у backlog із costs (rework time, on-call incidents).
- Solopreneur / small-team де cost-of-delay frame маpsає вiдомі параметри.

## Applies If (ALL must hold)

- Tech-debt backlog has ≥10 items competing for fix time
- Items have observable bleed (extra dev-time, on-call pages, customer escalations)
- Decision-maker exists who will act on the scoring
- Re-scoring cadence agreed (weekly or sprint boundary)

## Skip If (ANY kills it)

- <5 tech-debt items — gut-feel ordering matches rubric output
- No observable bleed (debt is theoretical) — Cost-of-Delay collapses to 0
- Items lack business-value link — rubric becomes engineering-internal noise
- Decision-maker absent — scoring without action is shelfware

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
| `draft-tech-debt-cost-of-delay-scoring` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | JSON instance with axis scores |
| `templates/rubric.md` | Rubric skeleton with weighted axes |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-cost-of-delay-scoring.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[technology-evaluation-rubric]]
- [[test-suite-audit-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
