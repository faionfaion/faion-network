---
slug: decision-options-memo-template
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3624f920e0dd6eac"
summary: Standardized "options memo" template BAs use to escalate decisions — option framing, cost-value-risk per option, recommendation, dissent acknowledgement, decision-required-by date.
tags: [business-analyst, decision-memo, options-memo, escalation, requirements-baseline]
---
# Decision Options Memo Template

## Summary

**One-sentence:** A standardized BA decision-options memo — three named options, cost-value-risk per option, recommendation with dissent acknowledged, and a decision-required-by date — replacing the per-project improvised escalation document.

**One-paragraph:** BAs repeatedly write "options memos" to escalate decisions to product owners, sponsors, or steering committees. Each BA invents the format, the rigor varies, and the receiving decision-maker has to re-orient every time. The result: decisions delayed, follow-up rounds for missing context, or hasty commitments based on a one-option framing that hid the trade-off. This methodology pins the format: exactly three options (or N + a "why exactly three" justification), structured cost/value/risk per option, recommendation with explicit "why not the other two," dissenting-view acknowledgement (named), and a hard decision-required-by date. Output: decision-memo-NNN.md that the decision-maker can act on in 10 minutes.

## Applies If (ALL must hold)

- BA has identified a decision that requires escalation (cannot be made within the project team).
- More than one viable option exists (single-option memos are not decision memos — they are recommendations).
- A named decision-maker is available within the required timeframe.
- The decision affects scope, schedule, budget, or quality (the four classic levers).

## Skip If (ANY kills it)

- Decision is purely technical and within the engineering team's authority — use ADR.
- Decision is reversible and low-impact — escalate via Slack with one line.
- Stakeholder is unwilling or unable to read a 2-page memo — switch to verbal + meeting minutes.
- The "options" are all variations of one approach — re-frame; that's a recommendation, not a decision.

## Prerequisites

- The decision is well-framed: what is being decided, by when, by whom.
- Each option has been at least sketched (not necessarily costed) by the BA.
- Stakeholders consulted to surface dissent.
- A target decision-maker identified.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/stakeholder-analysis` | Dissent acknowledgement requires the named-stakeholder map. |
| `pro/ba/business-analyst/risk-analysis` | Per-option risk uses the standard risk register format. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 3-option floor, structured C/V/R, recommendation with why-not, dissent named, decision-by date | ~900 |
| `content/02-output-contract.xml` | essential | Memo shape, required sections, length cap | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: straw-man options, hidden recommendation, missing dissent | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `option-cost-value-risk-fill` | sonnet | Bounded fill per option from inputs |
| `dissent-summary` | sonnet | Synthesize named-stakeholder objections |
| `recommendation-rationale` | opus | Cross-option synthesis + trade articulation |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-memo.md` | Skeleton with all required sections |
| `templates/cvr-table.md` | Cost-Value-Risk table per option |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/memo-completeness-check.py` | Verifies all required sections populated; flags template-default lines | Pre-send |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodology: `stakeholder-analysis`, `risk-analysis`, `change-impact-assessment`
- external: [Amazon 6-page memo culture](https://www.businessinsider.com/jeff-bezos-meeting-amazon-rules-2018-4) · [BABOK §10.21 Decision Analysis](https://www.iiba.org/career-resources/babok/)
