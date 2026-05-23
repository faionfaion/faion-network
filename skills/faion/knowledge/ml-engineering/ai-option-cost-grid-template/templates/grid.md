<!-- purpose: skeleton AI option cost grid (Markdown) -->
<!-- consumes: vendor pricing + dev cost + eval set scores per option -->
<!-- produces: filled grid in this layout, ready for sign-off -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: small -->

# AI Option Cost Grid — `<project-name>`

**template_version:** 1.1.0
**decision_owner:** `<role:person>`
**eval_set_hash:** `<hex>`
**last_reviewed:** `<YYYY-MM-DD>`

## Options

| option_name | family | dev_cost_usd | infra_cost_usd_per_1k_calls | latency_p95_ms | quality_score | vendor_lock_risk | ttv_weeks | maintenance_load |
|-------------|--------|-------------:|----------------------------:|---------------:|--------------:|------------------|----------:|------------------|
| `<opt-1>`   | prompt-eng | `<n>` | `<n>` | `<n>` | `<n>` | low/medium/high | `<n>` | low/medium/high |
| `<opt-2>`   | rag | `<n>` | `<n>` | `<n>` | `<n>` | low/medium/high | `<n>` | low/medium/high |
| `<opt-3>`   | sft | `<n>` | `<n>` | `<n>` | `<n>` | low/medium/high | `<n>` | low/medium/high |

## N/A reasons

| option | column | reason |
|--------|--------|--------|
| `<opt>` | `<col>` | `<why>` |

## Recommendation

`<≥20-char narrative justifying the chosen option, citing the columns that drove the call>`

## Discarded options

- `<option>` — `<one-line reason>`

## Worked example

See `templates/grid.md` filled instance under `examples/` once first instance is authored.
