---
slug: prototype-iteration-log-template
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pinned per-flow iteration log with fixed shape (problem → hypothesis → variant → evidence → outcome → next) so prototype work stops being folklore and starts being a reviewable operating tool.
content_id: "f3bba5f49f36895e"
complexity: medium
produces: decision-record
est_tokens: 3600
tags: ["prototype", "iteration", "log", "ux", "evidence"]
---
# Prototype Iteration Log Template

## Summary

**One-sentence:** Pinned per-flow iteration log with fixed shape (problem → hypothesis → variant → evidence → outcome → next) so prototype work stops being folklore and starts being a reviewable operating tool.

**One-paragraph:** Solo designers iterate prototypes in 1-3 hour sprints and forget the why next week. This template forces a per-flow log row: problem statement, hypothesis under test, variant shipped, evidence collected (5-user test, click-through metric, internal review), outcome (kept | rolled-back | shipped-with-changes), and next iteration. Rows are append-only and signed by a named owner.

**Ефективно для:**

- Solo designer running 1-3hr prototype sprints multiple times per week.
- AI agent generating prototype variants that need a log to track outcome.
- Handoff to a new designer who must understand why the prototype state is what it is.
- Pre-mortem on a stalled prototype where the chain of decisions is unclear.

## Applies If (ALL must hold)

- Active prototype with at least 1 variant tested in the last 14 days.
- Evidence collection mechanism exists (user test, metric, review).
- Owner has 15 minutes per iteration to log the row.
- Downstream consumer (designer, PM, agent) will read the log.

## Skip If (ANY kills it)

- Throwaway sketch with no test cycle.
- Production design (not prototype) — log via design-decision-log instead.
- No evidence collection — log becomes opinion log, low value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prototype flow URL | Figma / Codepen / live URL | Prototype tool |
| Hypothesis statement | string | Author memory |
| Evidence collection method | string | Test plan |
| Owner handle | string | Designer / agent registry |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/prototyping` | Prototype methodology this log sits inside. |
| `solo/ux/design-decision-log-template` | Stable decisions graduate to the decision log. |

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
| `draft-iteration-row` | sonnet | Per-iteration judgement on hypothesis and outcome. |
| `dedupe-and-status` | haiku | Deterministic similarity check across rows. |
| `sprint-retro-pass` | opus | Cross-row pattern detection across a sprint. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prototype-iteration-log-template.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/prototype-iteration-log-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prototype-iteration-log-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-decision-log-template]]
- [[scope-creep-park-list-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
