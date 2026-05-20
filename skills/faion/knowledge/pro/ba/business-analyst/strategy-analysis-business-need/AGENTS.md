---
slug: strategy-analysis-business-need
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Strategy Analysis starts by defining why change is needed.
content_id: "7706876195b4be04"
tags: [strategy-analysis, business-need, babok, problem-framing, requirements]
---
# Strategy Analysis: Business Need Framing

## Summary

**One-sentence:** Strategy Analysis starts by defining why change is needed.

**One-paragraph:** Strategy Analysis starts by defining why change is needed. The business need must be outcome-shaped — not solution-shaped — and must carry drivers with primary-source evidence, a falsifiable consequence of inaction, a named decision-maker, a time horizon, and explicit traces to corporate strategic goals. A need frame signed by the sponsor is the gate to current-state work.

## Applies If (ALL must hold)

- A new initiative is starting and a sponsor has handed the BA a vague mandate ("we need to fix customer service") — you need a defensible problem frame before any solution is proposed.
- Annual or quarterly portfolio planning where N candidate initiatives compete for the same budget and each needs a one-pager linking to a strategic goal, gap, and capability.
- Pre-RFP or pre-business-case work where the change strategy will gate a 7-figure spend; auditors and the steering committee will demand traceability from need to spend.
- Digital transformation programs where the business need spans process, tech, people, and data simultaneously.
- M&A integration: acquired entity current state vs. post-merger future state, with a gap analysis driving Day-1 / Day-100 / Day-365 plans.
- Regulatory-driven change (SOX, GDPR, DORA, NIS2): the regulator defines the future state externally; the BA must produce the need frame and gap.
- After a strategy refresh by leadership: each function translates the new corporate strategy into its own future-state and gap, and the BA agents help pull the workstreams onto a shared template.

## Skip If (ANY kills it)

- Single-team, single-quarter, low-blast-radius work — a 5-line ADR plus a backlog item beats a strategy artifact.
- The future state is already locked by an executive who is not interested in alternatives — document it as a directive instead; producing a "strategy analysis" becomes theatre.
- Pure incident response or outage post-mortems — those use root-cause analysis, not future-state-vs-current-state framing.
- Early-stage product discovery where customer pain is unproven — use opportunity-solution-trees, jobs-to-be-done, or lean-canvas first, then strategy analysis once the opportunity is validated.
- Pure financial decisions with directly comparable cash flows — go to NPV / IRR; don't dress them as strategy analysis.
- Operational hot-fixes with a known cause and known patch — overhead exceeds value.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ba/business-analyst/`
