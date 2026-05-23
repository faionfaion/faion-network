# Paid Acquisition Growth Strategy

## Summary

**One-sentence:** Produces a paid-acquisition growth plan: CAC/LTV math, channel-mix gate, payback-window target, scaling cadence + decision gates per channel.

**One-paragraph:** Multi-channel paid acquisition strategy gated on unit economics. Methodology computes CAC ceiling from LTV × target payback, picks initial channel mix per audience-fit (Meta + Google for B2C; LinkedIn + Google for B2B; X for niche tech), defines per-channel scaling cadence (+20%/wk while CAC stable), and gates further spend on CAC < ceiling + 14-day stable performance.

**Ефективно для:**

- Unit economics defined: LTV, gross margin, payback window.
- Channel-mix decision: Meta+Google для B2C, LinkedIn+Google для B2B.
- Scaling cadence: +20%/wk while CAC stable.
- Gate на CAC < ceiling + 14-day stable performance.

## Applies If (ALL must hold)

- Product with defined LTV + gross margin + payback target.
- Pre-launch / launch growth planning across 2+ channels.
- Scaling existing campaigns past current spend bucket.
- Investor / board reporting on paid growth efficiency.

## Skip If (ANY kills it)

- No LTV / margin data — cannot compute CAC ceiling; gather data first.
- Single-channel campaigns with no scaling pressure — channel methodology fits better.
- Brand-only spend (no acquisition KPI) — different brief.
- Spend < $5k/mo total — overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Unit economics | JSON / sheet | finance |
| Audience-channel fit hypothesis | doc | GTM |
| Tracking + attribution stack | report | ads-attribution-models |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Conversion + value priority drive CAC measurement. |
| `pro/marketing/ppc-manager/ads-attribution-models` | Attribution choice determines what CAC means. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for growth-paid-acquisition | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cac-ceiling` | haiku | Mechanical LTV × margin × payback share. |
| `channel-mix` | sonnet | Audience-fit × budget allocation. |
| `stop-loss-policy` | haiku | Apply standard 30% / 14-day rule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-plan.md` | Paid acquisition growth plan Markdown skeleton. |
| `templates/unit-economics.csv` | Unit economics CSV header. |
| `templates/growth-plan.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-paid-acquisition.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-conversion-tracking]]
- [[ads-attribution-models]]
- [[ads-budget-optimization]]
- [[ads-linkedin-ads]]
- [[facebook-ads]]
- [[google-ads-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
