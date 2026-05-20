---
slug: elicitation-techniques
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Elicitation is the process of drawing out information from stakeholders about their needs, wants, and constraints — not just asking questions but using structured techniques to uncover stated and unstated requirements.
content_id: "d86f3492ffac9a26"
tags: [elicitation, requirements, stakeholder-engagement, discovery, triangulation]
---
# Elicitation Techniques

## Summary

**One-sentence:** Elicitation is the process of drawing out information from stakeholders about their needs, wants, and constraints — not just asking questions but using structured techniques to uncover stated and unstated requirements.

**One-paragraph:** Elicitation is the process of drawing out information from stakeholders about their needs, wants, and constraints — not just asking questions but using structured techniques to uncover stated and unstated requirements. Core techniques are: interviews (depth), workshops (consensus), observation (actual behavior), document analysis (existing state), surveys (breadth), prototyping (validation), focus groups (user perspective), and brainstorming (ideation). Each session produces a typed artifact committed to version control with consent and PII-redaction markers; a synthesis step extracts REQ stubs that cite at least two distinct technique sessions per requirement, enforcing triangulation as an empirical requirement quality gate.

## Applies If (ALL must hold)

- Kickoff of a new initiative where stakeholder needs are vague, contradictory, or undocumented.
- Migration or replatforming projects where knowledge lives in a few senior employees' heads.
- Regulated domains (medical, fintech, gov) where elicitation evidence is part of the audit trail.
- Discovery sprints where the BA must triangulate a process within one week using mixed techniques.
- Distributed or async teams where surveys, recorded interviews, and async observation are the only feasible channels.

## Skip If (ANY kills it)

- Solo founder or 2-person team where direct conversation is faster than scheduling formal sessions.
- Backlog refinement on a stable product — DoR conversations and slice discussions cover it.
- The answer is already in a spec, ADR, or RFC — read first, elicit only the gaps.
- Bug triage or incident postmortems — those have their own templates (5-whys, blameless retro).
- Stakeholders are unwilling or unavailable — surveys to non-responsive groups produce noise; escalate sponsorship instead.

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
