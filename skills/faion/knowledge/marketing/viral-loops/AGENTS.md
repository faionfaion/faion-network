# Viral Loops and Types

## Summary

**One-sentence:** Five viral-loop archetypes (Word-of-Mouth / Inherent / Incentivized / Content / Outbreak) with K-factor ranges and product-fit conditions — pick ONE primary.

**One-paragraph:** Five viral-loop archetypes (Word-of-Mouth / Inherent / Incentivized / Content / Outbreak) with K-factor ranges and product-fit conditions — pick ONE primary. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Consumer / prosumer products із потенційно вірусним механізмом sharing.
- Перед інвестиціями в виральний loop — pick правильний archetype спочатку.
- Якщо K-factor < 0.3 і команда хоче інвестувати — спершу archetype, потім mechanics.
- При перейті з paid acquisition focus до organic / viral.

## Applies If (ALL must hold)

- Product має natural share moment (output, social hook, multi-user collaboration).
- Team готова інвестувати > 1 quarter у виральний механізм.
- Baseline активного use вже виміряний — viral працює тільки на retained users.

## Skip If (ANY kills it)

- B2B enterprise з 100% closed-network sales — virality irrelevant.
- Low-retention product — virality поверх leaky bucket втрачає економіку.
- Already running 2+ viral loops simultaneously — це stacking issue, не archetype pick.

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
| `pro/marketing/growth-marketer` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
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
| `templates/decision-record-skeleton.md` | Viral Loops and Types skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Viral Loops and Types. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-viral-loops.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[viral-metrics]]
- [[viral-optimization]]
- [[growth-loops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
