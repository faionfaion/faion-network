---
slug: error-prevention
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Eliminate error-prone conditions before they occur using six strategies (constraints, defaults, suggestions, validation, confirmation, affordances); produce an audit spec artefact mapping each error class in the product to a prevention strategy."
content_id: "63a5c419599d76c8"
complexity: medium
produces: spec
est_tokens: 4800
tags: ["error-prevention", "form-design", "input-validation", "user-experience", "heuristic-5"]
---
# Error Prevention — Nielsen Heuristic #5

## Summary

**One-sentence:** Eliminate error-prone conditions before they occur using six strategies (constraints, defaults, suggestions, validation, confirmation, affordances); produce an audit spec artefact mapping each error class in the product to a prevention strategy.

**One-paragraph:** Nielsen's fifth heuristic: even better than good error messages is a careful design that prevents errors from happening in the first place. This methodology enumerates six prevention strategies — constraints (block invalid input), defaults (start in the most useful state), suggestions (autocomplete, recent values), validation (real-time + on-submit), confirmation (destructive actions), affordances (the control looks like its function) — audits the product's current error classes against the six, and produces a prioritised spec of which strategy to apply per error.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Form-heavy product where user error rates degrade conversion.
- Destructive-action surfaces (delete, cancel subscription, send) where mistakes cost user trust.
- Quarterly UX health pass when support tickets cluster around "I made a mistake and could not undo it".
- Onboarding a new designer to Nielsen's heuristic set.

## Skip If (ANY kills it)

- The product has no live error data yet — instrument first, audit after.
- A < 90-day-old prevention audit already exists for the same surface.
- The issue is recovery (after the error happens) — use error-recovery (Heuristic #9) instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Error class inventory | list with frequency | analytics + support tickets |
| Form / control inventory | list of inputs by screen | design ops |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/heuristic-evaluation` | parent Nielsen heuristics framework |
| `solo/ux/ux-researcher/error-recovery` | sibling heuristic (Heuristic #9) — recovery handles errors prevention does not catch |

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
| `templates/error-prevention.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-error-prevention.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-prevention.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[heuristic-evaluation]]
- [[error-recovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
