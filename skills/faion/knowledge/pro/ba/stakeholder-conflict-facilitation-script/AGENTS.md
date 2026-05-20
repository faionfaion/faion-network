---
slug: stakeholder-conflict-facilitation-script
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Step-by-step facilitation script for a live stakeholder-conflict meeting — agenda, ground rules, position framing, decision rubric, and dissent-capture format — replacing soft-skill folklore with a codified process.
content_id: "f29b084876d9937d"
tags: [business-analyst, stakeholder-conflict, facilitation, decision-rationale, p4-outsource, p6-product-dev-team]
---
# Stakeholder Conflict Facilitation Script

## Summary

**One-sentence:** A meeting-day script that runs a stakeholder-conflict facilitation as a five-phase sequence — frame → state positions → apply rubric → decide → record dissent — and produces a signed decision log entry instead of a vibe.

**One-paragraph:** Stakeholder analysis methodologies map who has what stake, but say nothing about how to facilitate an actual conflict meeting where two named stakeholders disagree on a requirement. BAs default to whatever soft skill they happen to have, which means quality varies by personality. This methodology codifies the facilitation: a 60-minute structured meeting with phase-explicit agenda (5 min frame → 15 min positions → 15 min rubric application → 10 min decision → 15 min dissent capture and assignments), pre-circulated ground rules, a decision rubric that converts qualitative arguments into a shared score, and a written dissent capture that documents who disagreed and on what grounds. Output is a one-page decision-rationale entry signed by all attendees. Eliminates the "we discussed it and decided" entry in the requirements doc that everyone later disowns.

## Applies If (ALL must hold)

- Two or more named stakeholders disagree on a requirement, scope item, or design choice — disagreement is recorded somewhere (email, doc comment, meeting note).
- The BA owns or co-owns the resolution process (not pure escalation to a sponsor).
- Stakeholders can be brought into one synchronous meeting (in-person or video) — fully async is a different methodology.
- Decision affects work that is committed within the next sprint cycle (i.e., real time pressure).

## Skip If (ANY kills it)

- Pure escalation case where the sponsor will rule unilaterally — script over-engineers it.
- Conflict is interpersonal, not requirements-based — needs HR/coaching, not BA facilitation.
- Stakeholders refuse to commit to the rubric in advance — phase 3 collapses without it.
- Decision can be safely deferred more than 2 sprints — run async requirements clarification instead.

## Prerequisites

- One-paragraph statement of the disagreement signed off by both stakeholders ("yes, this is what we disagree about").
- Pre-circulated decision rubric template (criterion + weight + scoring scale).
- Decision-log file with a stub entry created before the meeting.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/stakeholder-analysis` | Stakeholder map informs who must attend and what authority each carries. |
| `pro/ba/decision-rationale-capture` | Output format consumed by this script. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: five phases timeboxed, pre-circulated agenda + ground rules, rubric used not narrative, named dissent captured, one-page signed log. | ~900 |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer: `stakeholder-conflict-mediation`, `decision-rationale-capture`, `decision-options-memo-template`
- external: BABOK §10.43 Stakeholder List + IAF Core Facilitator Competencies E (Guide Group to Appropriate and Useful Outcomes)
