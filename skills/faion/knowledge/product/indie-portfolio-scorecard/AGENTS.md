# Indie Portfolio Scorecard

## Summary

**One-sentence:** Single scorecard view across multiple indie products: MRR, growth %, support load, founder hours/week, joy score — used to decide which products to grow, maintain, kill.

**One-paragraph:** Multi-product indie operators need a single scorecard to decide where to put attention. Faion's product-lifecycle methodologies skew enterprise. This methodology pins a purpose-built scorecard with five columns per product: MRR, growth % (90-day), support load (hours/week), founder hours/week, joy score (1-5). The scorecard is reviewed monthly. Decision rules: products with declining MRR + low joy → kill candidate; high MRR + low growth + low founder hours → maintain mode; high growth + high founder hours → grow mode.

**Ефективно для:**

- Indie operator with ≥2 live products.
- Founder running a portfolio that 'feels' wrong but can't be measured.
- Maker with bundled offers (course + tool + newsletter).
- Solo consultant productising offers across multiple SKUs.

## Applies If (ALL must hold)

- Operator runs ≥2 live products with billing data.
- MRR data is available per product.
- Operator owns the calendar to estimate hours/week.
- Monthly review slot is calendared.

## Skip If (ANY kills it)

- Single-product operator — scorecard adds no value.
- All products are pre-revenue — score the bets, not the products.
- Founder cannot self-rate joy honestly — talk to a coach first.
- Data quality is too poor (no MRR tracking) — fix tracking first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-product MRR series (90 days) | csv | billing system |
| Per-product support ticket counts | csv | support tool |
| Founder hours/week estimate | self-report | operator |
| Joy score (1-5) | self-report | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/multi-product-portfolio-management` | portfolio-management context |
| `solo/pm/tiny-bets-quarterly-cadence` | quarter-cadence link |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-indie-portfolio-scorecard` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/indie-portfolio-scorecard.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/indie-portfolio-scorecard.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-indie-portfolio-scorecard.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[multi-product-portfolio-management]]`
- `[[tiny-bets-quarterly-cadence]]`
- `[[kill-or-keep-criteria]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
