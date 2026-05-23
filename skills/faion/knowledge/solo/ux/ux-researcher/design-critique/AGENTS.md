---
slug: design-critique
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Structured conversation analysing a design against defined goals and principles; produces an actionable feedback spec artefact where every comment is specific, principle-grounded, and converted into a tracked decision."
content_id: "8b7a846ace9e56ef"
complexity: medium
produces: spec
est_tokens: 4800
tags: ["design-critique", "feedback", "design-review", "team-collaboration", "design-process"]
---
# Design Critique

## Summary

**One-sentence:** Structured conversation analysing a design against defined goals and principles; produces an actionable feedback spec artefact where every comment is specific, principle-grounded, and converted into a tracked decision.

**One-paragraph:** Without structure, design reviews become opinion battles where feedback is vague, ideas die from personal preferences, and designs do not improve. This methodology pins the critique format: presenter states goals + constraints + open questions; reviewers give specific observations (grounded in heuristics or research, not taste) before recommendations; decisions are tracked with owner + due-date; no anonymous 'I just don't like it'. Output: a critique decision-log spec downstream design iterations and stakeholders read instead of re-litigating.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Weekly or sprint-based design reviews on shipped or near-shipping work.
- Senior-IC mentorship sessions where the goal is teaching critique skill.
- Cross-discipline reviews (design + eng + product) before commit.
- Onboarding a new designer to the team's critique norms.

## Skip If (ANY kills it)

- The design is at sketch / divergence stage — premature critique kills exploration.
- Only one reviewer is available — that's a 1:1 review, not a critique.
- The decision being made is a launch / no-launch question — that's a stage-gate review, not a critique.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Design artefact | Figma file / prototype / static | presenter |
| Goals + constraints + open questions | one paragraph | presenter |
| Reviewer roster | 3-6 people | design ops |
| Named facilitator | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/heuristic-evaluation` | supplies the heuristics critique observations cite |
| `solo/ux/ux-researcher/consistency-standards` | supplies consistency criteria for cross-product critiques |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-critique.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-design-critique.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-critique.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[heuristic-evaluation]]
- [[consistency-standards]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
