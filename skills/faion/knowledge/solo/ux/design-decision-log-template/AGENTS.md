---
slug: design-decision-log-template
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Captures every design decision (Figma comment thread, Slack ping, standup verbal) as a single-row artefact with context, decision, alternatives, and owner so the same decision is not re-litigated next week.
content_id: "760dd09b25ff0056"
complexity: medium
produces: decision-record
est_tokens: 3600
tags: ["design-decision", "log", "audit-trail", "ux", "documentation"]
---
# Design Decision Log Template

## Summary

**One-sentence:** Captures every design decision (Figma comment thread, Slack ping, standup verbal) as a single-row artefact with context, decision, alternatives, and owner so the same decision is not re-litigated next week.

**One-paragraph:** Design decisions evaporate when they live in chat. This template forces a one-row artefact per decision: timestamp, context (the question), decision (active voice), alternatives considered, accepted-by owner, and a link back to the original thread. The log is append-only; superseded decisions reference the new row instead of being edited. AI handoffs cite log rows by ID.

**Ефективно для:**

- Solo founder making weekly design calls that need to survive an agent handoff.
- Two-person design + eng pair where Slack threads die after 14 days.
- Onboarding a new designer / agent that needs the why behind current Figma state.
- Compliance / audit context where decision provenance must be reconstructable.

## Applies If (ALL must hold)

- At least one non-trivial design choice (component shape, copy, motion, a11y rule) was made in the last 7 days.
- Decision was driven by a question, not by personal preference alone.
- Decision had at least one realistic alternative considered.
- Future readers (agent, new hire) will need to understand the why.

## Skip If (ANY kills it)

- Trivial implementation detail (which icon variant) with no alternative considered.
- Decision will certainly be revisited within 7 days — log it after stabilising.
- Decision is captured in an ADR already — do not duplicate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Original thread link | URL | Figma comment / Slack / standup notes |
| Question that triggered the decision | string | Author memory or thread quote |
| Alternatives shortlist | array of strings | Brainstorm or thread responses |
| Owner handle | string | Designer / agent registry |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/stakeholder-walkthrough-script` | Walkthrough script surfaces decisions for the log. |
| `solo/ux/scope-creep-park-list-template` | Parked ideas are kept distinct from decided rows. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-log-row` | sonnet | Per-decision judgement on framing and alternatives. |
| `dedupe-pass` | haiku | Deterministic similarity check against existing rows. |
| `weekly-log-audit` | opus | Cross-row pattern detection (e.g. 5 rows on the same component). |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-decision-log-template.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/design-decision-log-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-decision-log-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[stakeholder-walkthrough-script]]
- [[scope-creep-park-list-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
