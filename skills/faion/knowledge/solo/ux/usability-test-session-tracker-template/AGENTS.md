---
slug: usability-test-session-tracker-template
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a per-session usability-test tracker artefact that normalises task success/failure logging across many moderation sessions."
content_id: "9bff924abd2880b3"
complexity: medium
produces: spec
est_tokens: 4800
tags: ["usability-test-session-tracker-template", "ux", "solo", "usability", "session-tracker"]
---
# Usability Test Session Tracker Template

## Summary

**One-sentence:** Produces a per-session usability-test tracker artefact that normalises task success/failure logging across many moderation sessions.

**One-paragraph:** Per-session usability-test moderation produces ad-hoc notes that drift between moderators; this methodology pins the schema for one session's tracker — participant id, task list, per-task success/failure, observed friction, severity, and a named owner who can be chased. Output: a versioned spec artefact validated against the JSON Schema in 02-output-contract.xml, consumed downstream by aggregate analysis or heuristic-evaluation reviews.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- the engagement runs ≥1 moderated usability test session this cycle.
- a single accountable moderator owns each session and signs off the tracker.
- downstream consumer (research lead, dev, product) will read the tracker without re-watching the session.
- task list and success criteria were defined before the session started.

## Skip If (ANY kills it)

- the session is an unmoderated remote test — use a different aggregation method.
- no task list exists yet — write the task list (use-case-mapping) first.
- the team is already using a working tracker template < 90 days old.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Session task list | Markdown checklist | use-case-mapping output or research plan |
| Named moderator | name + email | engagement charter |
| Participant id | opaque id (P01, P02, ...) | recruiting roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/usability-testing` | parent methodology for designing the test protocol |
| `solo/ux/user-researcher/use-case-mapping` | supplies the task list this tracker logs against |

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
| `templates/usability-test-session-tracker-template.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-usability-test-session-tracker-template.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-usability-test-session-tracker-template.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[usability-testing]]
- [[use-case-mapping]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
