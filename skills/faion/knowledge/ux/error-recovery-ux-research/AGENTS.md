# Error Recovery — Nielsen Heuristic #9

## Summary

**One-sentence:** Produce plain-language error messages with three components — what happened, why, how to fix it — applied to every error surface in the product; emit an error-message spec artefact covering every error class.

**One-paragraph:** Nielsen's ninth heuristic: error messages should be in plain language (no jargon), precisely indicate the problem, and constructively suggest a solution. This methodology pins the three-component message format (what happened, why, how to fix it), enumerates every error class in the product, drafts messages per class, and validates them with users (especially non-technical ones) before ship. Output: an error-message spec artefact downstream copywriters, engineers, and i18n consume.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Form-heavy product where users routinely hit validation errors.
- API-driven product where backend errors propagate to the UI as opaque codes.
- Migration of legacy error strings into the design system.
- Quarterly UX health pass when support tickets cluster around confused error messages.

## Skip If (ANY kills it)

- The product is pre-launch with no real error surfaces yet.
- A < 90-day-old error-message spec already exists for the same surfaces.
- The decision is to PREVENT the error in the first place — use error-prevention (Heuristic #5) instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Error class inventory | list by source (validation, network, server, business-rule) | analytics + support tickets |
| Tone / voice guide | brand doc | content strategy |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/heuristic-evaluation` | parent Nielsen heuristics framework |
| `solo/ux/ux-researcher/error-prevention` | sibling heuristic (Heuristic #5) — prevention catches what recovery handles |

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
| `templates/error-recovery.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-error-recovery.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-recovery.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[heuristic-evaluation]]
- [[error-prevention]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
