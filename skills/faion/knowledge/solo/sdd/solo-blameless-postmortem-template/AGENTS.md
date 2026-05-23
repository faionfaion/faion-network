---
slug: solo-blameless-postmortem-template
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: A 20-minute postmortem template sized for one human — fills mistakes.md and patterns.md directly, with no retro meeting, no blame language, and no team-scale rituals.
content_id: "50d0f1c3712d634f"
complexity: light
produces: report
est_tokens: 2800
tags: [postmortem, blameless, solo, incident-review, learning]
---
# Solo Blameless Postmortem Template

## Summary

**One-sentence:** A 20-minute postmortem template sized for one human — fills mistakes.md and patterns.md directly, with no retro meeting, no blame language, and no team-scale rituals.

**One-paragraph:** A 20-minute postmortem template sized for one human — fills mistakes.md and patterns.md directly, with no retro meeting, no blame language, and no team-scale rituals. The methodology pins the artefact: a fixed five-section structure (incident summary, timeline, root cause, lessons, prevention rule) and writes outputs to two files the solo memory layer already indexes.

**Ефективно для:**

- Solo founders running incidents on production but lacking a team retro.
- Agents that need to log a failure with a corrective rule for memory.
- Reviewers scanning recurring mistake patterns over time.
- Audit surface: every incident has a postmortem with a prevention rule.

## Applies If (ALL must hold)

- A user-visible or revenue-affecting incident occurred.
- There is exactly one operator (no team retro to run).
- memory/mistakes.md and memory/patterns.md exist as durable stores.

## Skip If (ANY kills it)

- Minor glitch with no customer impact and no operational lesson.
- Incident is still ongoing — postmortem comes after stabilisation.
- A team retro is already planned — use the team template instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Incident log | text | Telegram / monitoring |
| Timeline notes | text | Operator notes |
| memory/mistakes.md | markdown | Memory store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `none` | This methodology has no upstream dependency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-solo-blameless-postmortem-template` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-solo-blameless-postmortem-template` | haiku | Schema check + threshold checks; deterministic. |
| `review-solo-blameless-postmortem-template` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-blameless-postmortem-template.json` | JSON skeleton conforming to the output contract schema. |
| `templates/solo-blameless-postmortem-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-blameless-postmortem-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[reflexion-learning]]
- [[quality-gates-confidence]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
