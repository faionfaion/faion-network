---
slug: timeboxed-refactor-session-template
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a 2-hour refactor session checklist — scope, exit criteria, abort triggers, commit cadence — so refactor blocks ship a measurable change without scope creep.
content_id: "f44a608e495c38af"
complexity: light
produces: checklist
est_tokens: 4200
tags: ["refactor", "timebox", "session-template", "dev", "solo"]
---
# Timeboxed Refactor Session Template

## Summary

**One-sentence:** Generates a 2-hour refactor session checklist — scope, exit criteria, abort triggers, commit cadence — so refactor blocks ship a measurable change without scope creep.

**One-paragraph:** Generates a 2-hour refactor session checklist — scope, exit criteria, abort triggers, commit cadence — so refactor blocks ship a measurable change without scope creep.

**Ефективно для:**

- Solo developer running a daily/weekly 2-hour refactor block.
- Pairing slot for refactoring with explicit timebox.
- Pre-refactor planning where scope creep is the primary risk.

## Applies If (ALL must hold)

- Refactor target module is named in advance.
- Block duration is fixed (default 2h).
- Test suite exists and runs in <5 minutes.
- Git workflow allows commits during the block.

## Skip If (ANY kills it)

- Refactor needs >2 weeks — use a refactor epic, not this template.
- Test suite missing — add tests first.
- Greenfield prototype with no shipped users — refactor freely without ceremony.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Module path | string | git path to module |
| Refactor goal | string | ≤140 chars one-sentence goal |
| Test runtime | seconds | current test-suite runtime |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| weekly-branch-hygiene-checklist | Session commit/rebase discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-named-goal, r2-fixed-timebox, r3-abort-triggers, r4-commit-cadence, r5-exit-criteria | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Timeboxed Refactor Session Template artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: scope-creep, no-commits, vague-exit | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-timeboxed-refactor-session-template` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-timeboxed-refactor-session-template` | sonnet | Bounded structural check against the output contract. |
| `review-timeboxed-refactor-session-template` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/timeboxed-refactor-session-template.json` | JSON skeleton matching the output contract. |
| `templates/timeboxed-refactor-session-template.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-timeboxed-refactor-session-template.py` | Validate Timeboxed Refactor Session Template output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[weekly-branch-hygiene-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
