# PH Launch Day Runbook

## Summary

**One-sentence:** Hour-by-hour, PT-anchored Product Hunt launch-day runbook covering comment-back ritual, conversion logging, and energy-refuel cadence — produces a launch-day execution log artefact.

**One-paragraph:** Hour-by-hour, PT-anchored Product Hunt launch-day runbook covering comment-back ritual, conversion logging, and energy-refuel cadence — produces a launch-day execution log artefact. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- A Product Hunt launch is scheduled within the next 14 days.
- The 4-week prep deck (hunter confirmed, assets ready, hype list ≥50) is complete.
- The operator is launching solo or with one helper (not a 5-person team).
- The operator can clear the calendar for ≥14 hours on launch day.

## Skip If (ANY kills it)

- Operator is doing a quiet stealth launch (no scoreboard pressure) — runbook overhead does not pay back.
- A paid agency is running the launch — hand them the runbook, do not micromanage in parallel.
- Prep is incomplete — this is the day-of runbook, not the prep guide; use `feature-launch-checklist` first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the PH Launch Day Runbook task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `solo/sdd/sdd/AGENTS.md` | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/launch-day-log.md` | Markdown launch-day log: timestamped slots PT-anchored, comment-class triage table, signup conversion log. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ph-launch-day-runbook.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[ph-maker-dm-template]]
- [[post-launch-conversion-drip]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
