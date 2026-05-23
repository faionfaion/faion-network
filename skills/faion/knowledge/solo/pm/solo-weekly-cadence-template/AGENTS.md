---
slug: solo-weekly-cadence-template
tier: solo
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Sunday-review + Monday-prime weekly cadence checklist for a one-operator product \u2014 fixed two artefacts, four mandatory inputs, memory hook, hard 60-minute time-box."
content_id: "9cf9ffcb9b424b82"
complexity: medium
produces: checklist
est_tokens: 4000
tags: [solo-weekly-cadence-template, pm, solo, weekly-review, operator-cadence]
---
# Solo Weekly Cadence Template

## Summary

**One-sentence:** Sunday-review + Monday-prime weekly cadence checklist for a one-operator product — fixed two artefacts, four mandatory inputs, memory hook, hard 60-minute time-box.

**One-paragraph:** Existing weekly-review methodologies state intent ('review the week') but leave the artefact set vague, so the ritual drifts and dies. This methodology pins (a) the exact two artefacts produced each week (week-note + next-week-plan), (b) the four mandatory inputs reviewed (KPI dashboard, last-week plan, support inbox, backlog top-10), (c) the memory-hook step that connects this week's decisions back to last week's plan, and (d) a 60-minute total time-box split 30/30 between Sunday review and Monday prime.

**Ефективно для:**

- Solo SaaS operator running their own product + support + marketing.
- Indie hacker in weeks 4-52 looking for a recoverable rhythm after burnout.
- Freelance technologist managing 3-5 retainers who need a single weekly checkpoint.
- Operator stuck in firefighting mode without time for prioritisation.

## Applies If (ALL must hold)

- Operator is solo (no team to broadcast to).
- Product or practice is live with at least 4 weeks of operating data.
- Weekend availability allows a 30-minute Sunday slot + Monday 30-minute prime slot.
- Operator is willing to commit to ≥3 consecutive weeks before evaluating.

## Skip If (ANY kills it)

- Operator is on holiday / parental leave — pause cadence rather than half-ass it.
- Product is pre-launch with no users — switch to a build-week cadence instead.
- Operator already runs a working Monday standup in a team context.
- Cadence has been skipped 3 weeks in a row — restart from scratch, do not catch up.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Weekly-note file template | Markdown / Notion / Obsidian | operator template store |
| KPI dashboard reference | URL or doc path | solo-kpi-dashboard-template |
| Backlog with last-week plan items | list | task tracker |
| 60 minutes of uninterrupted time | calendar block | operator calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager` | parent skill — operator weekly rhythm |
| `solo/product/solo-kpi-dashboard-template` | metric block source for the weekly note |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-solo-weekly-cadence-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-weekly-cadence-template.md` | Markdown skeleton for the checklist artefact, matching content/02-output-contract.xml |
| `templates/solo-weekly-cadence-template.schema.json` | JSON Schema seed + filled fixture for the checklist artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-weekly-cadence-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `solo/pm/project-manager`
- `[[solo-kpi-dashboard-template]]`
- `[[tiny-bets-quarterly-cadence]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
