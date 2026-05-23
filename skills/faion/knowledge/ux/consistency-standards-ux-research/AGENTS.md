# Consistency and Standards

## Summary

**One-sentence:** Apply Nielsen Heuristic #4 across five layers (internal, external, visual, functional, verbal) via a design system and consistency audits; produce an audit spec artefact counting distinct variations per UI element and recommending consolidation.

**One-paragraph:** Users should not have to wonder whether different words, situations, or actions mean the same thing. This methodology applies Nielsen's Heuristic #4 across five layers: internal (same product), external (industry conventions), visual (colour, typography, spacing), functional (interaction patterns), and verbal (terminology). Output is a consistency-audit spec artefact counting distinct variations per UI element (e.g., '7 different button styles for the same action'), prioritising consolidations by user impact, and recommending design-system codification.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Pre-design-system audit when the product has grown without a system.
- Quarterly consistency check on a mature design system.
- Onboarding a new designer who needs the canonical variation inventory.
- Post-merger / post-acquisition unification work.

## Skip If (ANY kills it)

- The product is < 3 months old and the design system has not yet been seeded.
- A current consistency audit < 90 days old exists for the same surface.
- The change is a single-page polish — full audit is overkill.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| UI surface inventory | list of screens / components | design ops |
| Industry convention reference | platform guidelines (iOS HIG, Material, WCAG) | public docs |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/heuristic-evaluation` | parent Nielsen heuristics methodology |
| `solo/ux/ux-researcher/content-audit-process` | sibling lens for verbal/content consistency |

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
| `templates/consistency-standards.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-consistency-standards.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-consistency-standards.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[heuristic-evaluation]]
- [[content-audit-process]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
