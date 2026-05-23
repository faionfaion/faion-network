---
slug: program-weekly-note-template
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pinned weekly programme note template — headline, per-workstream progress, top-3 risk moves, decisions, sponsor asks with evidence anchors and outcome review.
content_id: "75b785eb6527e9e4"
complexity: medium
produces: report
est_tokens: 3800
tags: [program, weekly-note, status, communication]
---
# Program Weekly Note Template

## Summary

**One-sentence:** Pinned weekly programme note template — headline, per-workstream progress, top-3 risk moves, decisions, sponsor asks with evidence anchors and outcome review.

**One-paragraph:** Multi-team programmes need a fixed-shape weekly note that turns status from folklore into a reviewable artefact. The template fixes a one-sentence headline, per-workstream progress with evidence links, the top-3 risks that moved, the decisions taken, and a numbered list of sponsor asks. Each weekly note links forward to last-week outcomes (status of prior asks + decisions). Output: a versioned note committed to programme knowledge space, reviewed for outcome closure at the next iteration.

**Ефективно для:**

- Multi-workstream programmes with sponsor + steering audience.
- Distributed programmes where async sponsor reading replaces synchronous status.
- Regulated programmes requiring weekly artefact evidence.
- Distressed projects where surface-area communication is the recovery lever.

## Applies If (ALL must hold)

- Programme spans ≥2 workstreams + has a sponsor audience.
- Notes are stored in a version-controlled or wiki space.
- Programme runs ≥6 weeks (review cadence pays off).
- Trigger event (weekly cadence) is scheduled.

## Skip If (ANY kills it)

- Single-workstream delivery — daily standup covers it.
- Programme < 6 weeks total — note cost exceeds value.
- Sponsor consumes status synchronously only — no async medium needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workstream pulse template | MD | PMO |
| Risk register | table | risk-management |
| Decision log | MD | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `risk-register` | Top-3 risks-moved section reads from the register. |
| `stakeholder-engagement` | Sponsor asks routed via engagement plan. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — fixed sections, evidence per progress line, top-3 risks-moved, numbered sponsor asks, last-week outcomes | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the note artefact | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: gather → draft → review → publish → close-loop | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping note state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-workstream-pulse` | haiku | Template fill from workstream inputs. |
| `synthesise-headline` | sonnet | One-sentence judgment requires cross-stream synthesis. |
| `outcome-review` | opus | Multi-week outcome pattern + closure synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-note.md` | Weekly note skeleton with fixed sections. |
| `templates/outcomes.md` | Last-week outcomes table. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-program-weekly-note-template.py` | Schema-validate the note JSON. | Pre-publish. |

## Related

- [[risk-register]]
- [[stakeholder-engagement]]
- [[project-closure-with-lessons-extraction]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the program-weekly-note-template input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
