# Go-to-Market Strategy

## Summary

**One-sentence:** Five-question GTM spec: define ONE ICP + anti-ICP, craft For/Who/Is/Unlike/We positioning, select 2-3 channels, choose sales motion by ACV, plan phased launch.

**One-paragraph:** Five-question GTM spec: define ONE ICP + anti-ICP, craft For/Who/Is/Unlike/We positioning, select 2-3 channels, choose sales motion by ACV, plan phased launch. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Before product launch — GTM strategy gate.
- Перед серйозним budget commit на marketing.
- При перейті між sales motions (PLG → sales-led або зворотньо).
- Кожні 6 місяців як strategy retrospective.

## Applies If (ALL must hold)

- Product complete enough для зовнішнього launch.
- Доступ до competitive landscape data.
- >= 1 quarter runway для viable GTM execution.

## Skip If (ANY kills it)

- Pre-product (alpha) — це product strategy, не GTM.
- Pure internal tool — GTM irrelevant.
- Already executing successful GTM — це optimization context, не strategy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-skeleton.md` | Go-to-Market Strategy skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Go-to-Market Strategy. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-gtm-strategy.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[growth-brand-positioning]]
- [[growth-product-hunt-launch]]
- [[growth-press-coverage]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
