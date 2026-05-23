# AI Product Marketing Patterns

## Summary

**One-sentence:** AI-product marketing pattern library: model-claim discipline, demo→spec gap, trust-and-safety messaging, pricing narrative, evals-as-marketing-asset.

**One-paragraph:** AI-product marketing pattern library: model-claim discipline, demo→spec gap, trust-and-safety messaging, pricing narrative, evals-as-marketing-asset. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`playbook-step`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Product has a user-facing AI feature (LLM, vision, agent).
- Marketing copy or launch is being written / rewritten.
- Org has appetite to differentiate from generic 'AI-powered' positioning.

## Skip If (ANY kills it)

- AI is incidental to the product (back-office only); marketing surface doesn't depend on it.
- Pre-revenue tinker product — positioning is premature.
- Generic 'AI-powered' tagline is the explicit strategy (mass-market commodity play).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Positioning canvas | Markdown | positioning-canvas |
| Model + eval data | Spreadsheet / report | ML team |
| Pricing model | Markdown | finance |
| Trust + safety policy | Markdown | compliance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist/positioning-canvas` | Underlying positioning framework. |
| `pro/marketing/growth-marketer/launch-playbook` | Launch cadence that consumes these patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pattern_pick` | sonnet | Match pattern to product context. |
| `claim_discipline_review` | opus | Audit copy for unverifiable claims. |
| `eval_to_asset` | sonnet | Turn eval results into marketing asset. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-library.md` | Inventory of patterns with examples. |
| `templates/claim-discipline-checklist.md` | Copy review checklist. |
| `templates/eval-asset.md` | Eval-as-marketing-asset template. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-product-marketing-patterns.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/marketing/`
- `[[positioning-canvas]]`
- `[[launch-playbook]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-product-marketing-patterns applies: root question — "Is the product user-facing AI with a marketing surface AND a non-commodity positioning intent?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
