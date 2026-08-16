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
| `templates/growth-plan.md.j2` | Paid acquisition growth plan Markdown skeleton. |
| `templates/growth-plan.md` | Paid acquisition growth plan Markdown skeleton. Generated from `templates/growth-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/unit-economics.csv` | Unit economics CSV header. |
| `templates/growth-plan.json` | Schema-conformant sample artefact used by validator self-test. |
| `templates/campaign-plan.md.j2` | Single paid-acquisition campaign plan working document — goals, audiences, creative, tracking, kill/scale criteria. |
| `templates/campaign-plan.md` | Single paid-acquisition campaign plan working document — goals, audiences, creative, tracking, kill/scale criteria. Generated from `templates/campaign-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/weekly-ads-report.md.j2` | Weekly cross-channel paid-acquisition performance report — spend, CPA, ROAS, learnings, next-week actions. |
| `templates/weekly-ads-report.md` | Weekly cross-channel paid-acquisition performance report — spend, CPA, ROAS, learnings, next-week actions. Generated from `templates/weekly-ads-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/unit-economics.csv`

```csv
metric,value,unit
ltv,2400,USD
gross_margin_pct,0.7,ratio
payback_months,6,months
cac_ceiling,280,USD
```

### `templates/growth-plan.json`

```json
{
  "unit_economics": {
    "ltv": 2400,
    "gross_margin_pct": 0.7,
    "payback_months": 6,
    "cac_ceiling": 280
  },
  "channel_mix": [
    {
      "channel": "meta",
      "fit_rationale": "B2C SMB on FB+IG",
      "weekly_budget": 1500
    },
    {
      "channel": "google_search",
      "fit_rationale": "high-intent demand capture",
      "weekly_budget": 1000
    }
  ],
  "scaling_plan": {
    "weekly_ramp_pct": 20,
    "stability_days": 14
  },
  "stop_loss": {
    "cac_breach_pct": 30,
    "auto_pause_days": 14
  }
}
```
