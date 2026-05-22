---
slug: CLAUDE-methodologies
tier: geek
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Index and selection guide for 32 core UX methodologies covering Nielsen's 10 usability heuristics, 6 research methods (interviews, usability testing, surveys, card sorting, personas, journey mapping), 9 design methods (wireframing, prototyping, A/B testing, heuristic evaluation, cognitive walkthrough, and others), and 7 advanced topics (IA framework, IA templates, mobile UX, voice UI, diary studies, competitive analysis, content audit).
content_id: "5c7e82dc21bf442c"
tags: [ux-methods, research, design, heuristics, methodology-index]
---
# UX/UI Methodologies — Complete Index

## Summary

**One-sentence:** Index and selection guide for 32 core UX methodologies covering Nielsen's 10 usability heuristics, 6 research methods (interviews, usability testing, surveys, card sorting, personas, journey mapping), 9 design methods (wireframing, prototyping, A/B testing, heuristic evaluation, cognitive walkthrough, and others), and 7 advanced topics (IA framework, IA templates, mobile UX, voice UI, diary studies, competitive analysis, content audit).

**One-paragraph:** Index and selection guide for 32 core UX methodologies covering Nielsen's 10 usability heuristics, 6 research methods (interviews, usability testing, surveys, card sorting, personas, journey mapping), 9 design methods (wireframing, prototyping, A/B testing, heuristic evaluation, cognitive walkthrough, and others), and 7 advanced topics (IA framework, IA templates, mobile UX, voice UI, diary studies, competitive analysis, content audit). Agent role: select, scaffold, and synthesize — not replace human participant work.

## Applies If (ALL must hold)

- Agent must select an appropriate UX research or design method for a given product problem
- Automated heuristic evaluation against Nielsen's 10 usability principles is needed
- Sprint requires a structured UX deliverable (persona, journey map, IA sitemap) that an agent can scaffold
- UX review of an existing design must be documented systematically before a critique session
- Cognitive walkthrough must be scripted for a new user flow

## Skip If (ANY kills it)

- User interviews, usability testing, focus groups, diary studies — require real human participants; agent cannot substitute for moderation or empathy-based interpretation
- Card sorting, tree testing — require actual user responses; agent can analyze results but not generate them
- A/B testing — requires live traffic; agent can design the test and analyze results, not run it
- Any method where output quality depends on observed human behavior in context

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

- parent skill: `geek/ux/ux-ui-designer/`
