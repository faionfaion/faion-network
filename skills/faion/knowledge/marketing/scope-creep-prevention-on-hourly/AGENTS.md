# Scope Creep Prevention on Hourly Engagements

## Summary

**One-sentence:** Hourly-specific countermeasure: explicit weekly-budget gate, billable-vs-non-billable taxonomy, async approval-before-work rule.

**One-paragraph:** Existing pro/client-engagement/scope-creep-management is fixed-price-shaped (change-request → SOW addendum). On hourly engagements, scope creep manifests as 'just one more thing' that bleeds time. Output: weekly budget gate + billable taxonomy + approval rules.

**Ефективно для:**

- Hourly engagement з тижневим budget gate (наприклад 20-40 год).
- Чіткої taxonomy білабельного/небілабельного часу.
- Async approval-before-work для будь-якого таску >2h.
- Команд фрілансерів, які регулярно перевищують бюджет без сигналу клієнту.

## Applies If (ALL must hold)

- freelancer on hourly retainer or hourly billable
- weekly billable hours target (e.g., 20-40h)
- scope creep observed (actual hours > target OR fluctuating)

## Skip If (ANY kills it)

- fixed-fee engagements (different scope-creep dynamics)
- no weekly cadence (e.g., monthly only)
- single-client + healthy margin — over-engineered

## Prerequisites

- current contract with hourly rate + cap
- time-tracking discipline
- client comms cadence (Slack, email)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/late-invoice-dunning-sequence` | peer methodology — produces inputs or consumes outputs |
| `pro/marketing/rate-raise-conversation-script` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/scope-creep-prevention-on-hourly.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/scope-creep-prevention-on-hourly.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-scope-creep-prevention-on-hourly.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `pro/marketing/late-invoice-dunning-sequence`
- peer methodology: `pro/marketing/rate-raise-conversation-script`
- peer methodology: `pro/client-engagement/scope-creep-management`
- external: https://www.freelancersunion.org/resources/contract-templates/; https://philipmorganconsulting.com/scope-creep/

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

