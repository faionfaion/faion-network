# Facebook Ads Playbook

## Summary

**One-sentence:** Produces a Facebook-specific campaign spec: feed + Reels + Marketplace placement mix, account-warmup plan for new ad accounts, learning-phase budget envelope.

**One-paragraph:** Facebook (feed + Reels + Marketplace) is still the dominant Meta surface for B2C and small B2B. This methodology forces account-warmup discipline (avoid hard launches that flag the account), pins the placement mix to native Facebook surfaces (no off-platform Audience Network unless data proves otherwise), and ties learning-phase budget to ≥50 conv/wk per ad set.

**Ефективно для:**

- B2C або small B2B з main audience на FB feed/Reels.
- New ad accounts — warmup ramp до full budget.
- FB-specific placement mix (feed + Reels + Marketplace).
- Learning-phase budget envelope ≥50 conv/wk на ad set.

## Applies If (ALL must hold)

- B2C product or small B2B with main audience on FB feed / Reels.
- New ad account that requires warmup ramp.
- Facebook-specific placement strategy (feed + Reels + Marketplace).
- Learning-phase budget planning ≥50 conv/wk per ad set.

## Skip If (ANY kills it)

- Audience primarily on Instagram only — use instagram-ads methodology.
- B2B with LTV ≥ $5k Director-up — LinkedIn beats FB.
- Existing account with stable delivery — skip warmup ramp.
- Audience Network preferred — only with ≥30 days CPM/CPA data justifying it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Facebook Page + verified domain | dashboard | platform owner |
| Pixel + CAPI live | dashboard | ads-conversion-tracking |
| Creative inventory native to FB | library | creative |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-meta-campaign-setup` | Generic Meta campaign rules apply on top. |
| `pro/marketing/ppc-manager/ads-meta-creative` | Native-feed creative supplies FB-format variants. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for facebook-ads | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `warmup-schedule` | haiku | Mechanical ramp curve. |
| `placement-choice` | sonnet | Per-audience native placement set. |
| `aem-event-ranking` | sonnet | Rank 8 events by business value. |

## Templates

| File | Purpose |
|------|---------|
| `templates/fb-launch-plan.md` | Facebook launch plan Markdown skeleton. |
| `templates/warmup-schedule.csv` | Warmup schedule CSV (days, % of target budget). |
| `templates/fb-launch-plan.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-facebook-ads.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-campaign-setup]]
- [[ads-meta-creative]]
- [[ads-meta-reporting]]
- [[instagram-ads]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
