---
slug: insight-to-design-ticket
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Translates a research insight into a properly-scoped design ticket with hypothesis, success metric, design constraints, and a draft acceptance criteria so the design sprint starts with no ambiguity.
content_id: "10eb2145dba12f56"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["insight", "design-ticket", "hypothesis", "research-to-design", "ux"]
---
# Insight-to-Design-Ticket

## Summary

**One-sentence:** Translates a research insight into a properly-scoped design ticket with hypothesis, success metric, design constraints, and a draft acceptance criteria so the design sprint starts with no ambiguity.

**One-paragraph:** Insights die between research and design when nobody writes the ticket. This methodology pins a four-section ticket: insight (the observed user behaviour), hypothesis (IF / THEN form), success metric (measurable target), design constraints (tokens / brand / a11y). The ticket has a draft AC that engineering will refine at handoff time; the designer commits to the AC at ticket creation, not later.

**Ефективно для:**

- Solo founder converting research notes into actionable design tickets.
- Researcher + designer handoff where the researcher writes the ticket.
- AI agent generating design tickets from session transcripts.
- Pre-sprint planning where backlog must contain only well-formed tickets.

## Applies If (ALL must hold)

- A research insight exists with observable user-behaviour evidence.
- Design will act on the insight in the next 1-3 sprints.
- A measurable success metric can be defined (or 'no-metric' explicitly accepted).
- Designer or agent will own the resulting ticket.

## Skip If (ANY kills it)

- Insight is too early — needs more sessions to confirm.
- Insight already addressed in an open design ticket — link to it instead.
- Insight is opinion / preference, not behaviour-based — discard or re-investigate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Research insight + evidence link | string + URL | research notebook |
| Backlog tool URL | URL | Sprint board |
| Success-metric source | metric system or 'no-metric' decision | Analytics or PM |
| Designer / agent handle | string | Team directory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/critical-issue-triage-protocol` | Triage feeds prioritised insights to this methodology. |
| `solo/ux/handoff-spec-template` | Ticket AC consumed at handoff time. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | End-to-end worked example | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ticket` | sonnet | Per-insight judgement on hypothesis + constraints. |
| `dedupe-ticket-bank` | haiku | Deterministic similarity check against existing tickets. |
| `sprint-batch-write` | opus | Batch of 5+ tickets from a single research sprint. |

## Templates

| File | Purpose |
|------|---------|
| `templates/insight-to-design-ticket.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/insight-to-design-ticket.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-insight-to-design-ticket.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[critical-issue-triage-protocol]]
- [[handoff-spec-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
