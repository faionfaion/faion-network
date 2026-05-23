# Meta Ads Campaign Setup

## Summary

**One-sentence:** Produces a Meta (Facebook/Instagram) campaign setup spec: objective, CBO/ABO structure, ad-set layering, placement strategy, naming convention, learning-phase plan.

**One-paragraph:** Meta auction punishes new campaigns hard during the learning phase. This methodology forces objective alignment with conversion goal, sets a clean Advantage Campaign Budget (CBO) vs Ad-Set Budget (ABO) decision, defines a 3-ad-sets-per-campaign cap (anti-fragmentation), pins automatic placements unless we have CPM data justifying otherwise, and emits a launch plan + naming convention that survives the learning phase.

**Ефективно для:**

- Launch нового Meta-кампейну з ясним conversion event та pixel.
- Перехід з ABO → CBO коли є ≥50 conversions/тиждень.
- Кампанії з 3-5 ad sets — anti-fragmentation cap.
- Pixel/CAPI installed і верифікований.

## Applies If (ALL must hold)

- New Meta campaign launch with a defined conversion event + verified pixel.
- Migration from Ad-Set Budget (ABO) to Campaign Budget Optimization (CBO).
- Portfolio cleanup: collapsing 10+ tiny ad sets into 3-5 sized correctly.
- Performance hand-off where naming + structure must survive personnel change.

## Skip If (ANY kills it)

- Pixel not installed or fires <10 events/day — auction has no signal to optimize on.
- Budget under $20/day per ad set — never exits learning phase.
- Brand-only awareness work with no conversion goal — different methodology.
- More than 5 ad sets per campaign planned — fragmentation kills delivery.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pixel + CAPI installation report | JSON / dashboard | ads-conversion-tracking methodology |
| Conversion event definition | schema doc | RevOps / GA4 owner |
| Budget envelope | JSON / table | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Conversion event must be defined + firing before campaign can exit learning phase. |
| `pro/marketing/ppc-manager/ads-meta-targeting` | Audience strategy is a downstream input to ad-set layering. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for ads-meta-campaign-setup | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 1100 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `structure-decision` | sonnet | ABO/CBO + ad-set cap reasoning. |
| `naming` | haiku | Mechanical concat per convention. |
| `learning-phase-plan` | sonnet | Volume → budget envelope reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/campaign-spec.md` | Meta campaign launch spec Markdown skeleton. |
| `templates/naming-checklist.md` | Naming convention checklist. |
| `templates/campaign-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-meta-campaign-setup.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-targeting]]
- [[ads-meta-creative]]
- [[ads-conversion-tracking]]
- [[facebook-ads]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
