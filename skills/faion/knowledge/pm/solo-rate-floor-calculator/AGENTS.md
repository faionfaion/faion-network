# Solo Rate Floor Calculator

## Summary

**One-sentence:** Solo-specific effective-hourly calculator that loads target income with taxes, downtime, marketing time, benefits, and tooling cost to produce a defensible rate floor with 3 sensitivity bands below which engagements are mathematically unprofitable.

**One-paragraph:** Generic "billable hours" calculators (Kalzumeus, freelance-rate-calculator.com) assume an idealised solo operator with linear hours and zero non-billable overhead. In practice, ~40% of a solo's calendar is sales, admin, learning, and recovery time. This methodology asks for 7 inputs (target income, working weeks, billable %, tax rate, benefit cost, tooling cost, profit margin), runs a load formula, and emits a floor rate with 3 sensitivity bands (±10pp billable). Output: `RateFloor` object with floor_usd_per_hour, project_minimum_usd, defensible breakdown, and a prospect-safe defence narrative that does NOT leak personal income.

**Ефективно для:**

- Solo freelancer pricing hourly / fixed / retainer engagements.
- Quarterly review when burn or tax jurisdiction changes.
- Pre-proposal floor check before negotiating with a prospect.
- Calibrating "is this prospect's $X/hr a starvation rate?" without revealing personal numbers.

## Applies If (ALL must hold)

- Operator is solo (no W-2 income, no co-founder splitting revenue).
- Engagement type ∈ {hourly, fixed-price, retainer-with-hour-cap}.
- Operator has 6+ months of historical billable-vs-total time data OR is willing to estimate honestly.
- Operator is in a tax jurisdiction with a known effective rate (US, EU, UK, CA, AU).

## Skip If (ANY kills it)

- Operator has a stable W-2 and freelancing is side income — rate-floor logic doesn't apply.
- Operator is in an exotic tax regime without a stable effective rate.
- Engagement is value-based or equity-based — different methodology.
- Engagement is < 10 hours total — fixed micro-price, floor irrelevant.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target annual gross income (USD) | number | operator |
| Effective tax rate including SE / VAT loading | number 0-1 | tax advisor |
| Expected billable hours per year | number (or 6mo history) | operator |
| Tooling subscriptions (annual) | number USD | operator |
| Desired profit margin | number ≥ 0.15 | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo-time-tracking-discipline]] | Billable % input comes from time-tracking data. |
| [[side-project-financial-runway]] | Runway model feeds target income decision. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: honest billable %, all-in tax, downtime cap, profit margin ≥15%, sensitivity bands | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for RateFloor + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 6 modes: optimistic billable %, tax understated, benefits zeroed, fixed-price misuse, margin compression, narrative leaks income | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: inputs → cap → load → sensitivity → defence | ~800 |
| `content/05-examples.xml` | essential | Worked example: $120k target, US, 46 weeks | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `input_validation` | haiku | Range checks. |
| `floor_calculation` | sonnet | Deterministic math + cross-checks. |
| `sensitivity_analysis` | sonnet | Tabular scenarios. |
| `defense_narrative` | sonnet | Short explanation for prospect-facing use. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rate-floor.json` | Output schema skeleton |
| `templates/load-spreadsheet.csv` | Editable input grid |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-rate-floor-calculator.py` | Validate RateFloor artefact against 02-output-contract schema | Quarterly review or per major engagement |

## Related

- [[solo-time-tracking-discipline]]
- [[side-project-financial-runway]]
- [[status-report-templates-by-audience]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by operator state (W-2 vs full-time solo), tax jurisdiction, engagement type, and input completeness onto a rule from `content/01-core-rules.xml`. Walk it before quoting a prospect; the cap and margin branches block-or-approve in seconds.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rate-floor.json`

```json
{
  "floor_usd_per_hour": 0,
  "sensitivity": [
    {
      "band": "low",
      "billable_pct": 0.45,
      "floor_usd_per_hour": 0
    },
    {
      "band": "baseline",
      "billable_pct": 0.55,
      "floor_usd_per_hour": 0
    },
    {
      "band": "high",
      "billable_pct": 0.65,
      "floor_usd_per_hour": 0
    }
  ],
  "project_minimum_usd": 0,
  "breakdown": {
    "target_income_loaded": 0,
    "tax_load_pct": 0,
    "working_weeks": 46,
    "billable_pct": 0.55,
    "benefit_cost_usd": 0,
    "tooling_cost_usd": 0,
    "profit_margin_pct": 0.2
  },
  "defense_narrative": "Loaded rate accounting for downtime, taxes, tooling, and a 20% reinvestment margin standard for senior independent practice.",
  "inputs_warning": [],
  "computed_at": "YYYY-MM-DD"
}
```

### `templates/load-spreadsheet.csv`

```csv
field,value,unit,notes
target_income,120000,USD/yr,gross target
profit_margin,0.20,fraction,>= 0.15
tax_load,0.34,fraction,jurisdictional all-in (incl. SE / VAT)
benefit_cost,8000,USD/yr,health + retirement
tooling_cost,3000,USD/yr,subscriptions
working_weeks,46,weeks,<= 46
billable_pct,0.55,fraction,<= 0.55 unless 6mo history cited
```
