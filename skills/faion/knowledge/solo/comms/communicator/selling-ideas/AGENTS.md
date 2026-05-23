---
slug: selling-ideas
tier: solo
group: comms
domain: comms
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an SPIN-Challenger pitch artefact (elevator pitch / executive pitch / one-pager) that amplifies pain before presenting a solution, with LAER objection handling.
content_id: "80ef1211f8e6a13b"
complexity: medium
produces: spec
est_tokens: 4200
tags: [selling, spin, challenger, elevator-pitch, laer]
---
# Selling Ideas

## Summary

**One-sentence:** Generates an SPIN-Challenger pitch artefact (elevator pitch / executive pitch / one-pager) that amplifies pain before presenting a solution, with LAER objection handling.

**One-paragraph:** A persuasion framework for pitching technical or business ideas to different audiences. Combines SPIN Selling (uncover and amplify pain via Situation → Problem → Implication → Need-payoff), Challenger Sale (teach a new insight, tailor, take control), the elevator pitch template, and LAER objection-handling (Listen, Acknowledge, Explore, Respond). Core rule: never pitch until the audience feels the problem.

**Ефективно для:**

- 30-second elevator pitch at a networking event.
- Executive briefing where the audience won't read past page 1.
- Sales conversation transitioning from discovery to proposal.
- Internal idea sale (engineer pitching adoption to PM).

## Applies If (ALL must hold)

- Audience has a real pain that the idea addresses.
- Author has time to ask 2-3 SPIN questions before pitching.
- Audience has decision authority on at least one next step.
- The idea has a concrete differentiator (Challenger insight).

## Skip If (ANY kills it)

- Audience is in evaluation-only mode (RFP) — different format.
- Pain has not been validated — go back to mom-test first.
- Pure information sharing, no decision sought — use storytelling.
- Author is hostile to the audience — selling is a relationship act.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Idea + differentiator | 1-sentence insight | author |
| Audience profile | role + likely pain + decision power | research |
| Proof points | evidence the solution works | case studies / metrics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[mom-test]] | discovery before pitching |
| [[business-storytelling]] | frame the pitch with Pyramid / SCQA |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `challenger-insight-draft` | sonnet | Synthesis of insight from data. |
| `spin-composition` | sonnet | Tone + order-sensitive. |
| `laer-objection-prep` | sonnet | Empathy + bounded judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/elevator-pitch.txt` | 30s elevator pitch skeleton (insight + 1-line SPIN + CTA) |
| `templates/executive-pitch.txt` | Executive pitch skeleton (insight + full SPIN + CTA) |
| `templates/one-pager.txt` | One-pager skeleton (Pyramid + SPIN + CTA box) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-selling-ideas.py` | Validate selling-ideas artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[mom-test]]
- [[business-storytelling]]
- [[stakeholder-communication]]
- [[negotiation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on pain validation first; without it the methodology refuses to apply. Otherwise it routes by format to the matching structure rule.
