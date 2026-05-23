# Google Ads Reporting Dashboards

## Summary

**One-sentence:** Generates a Google Ads dashboard spec: required custom-column preset, weekly + monthly + stakeholder views, automated alerts on CPA / IS / CR breaches, segment-by-default reports.

**One-paragraph:** Reporting layer over Google Ads. Locks the custom-column preset (impr, clicks, CTR, CPC, conv, CPA, ROAS, conv-value, IS, QS), defines 3 views (operator weekly / executive monthly / stakeholder summary), wires automated alerts on CPA breach, IS drop, or conversion-rate decline, and forces every report to ship segment breakdowns + a top-5 action queue.

**Ефективно для:**

- Існуючий звітний шар над Google Ads.
- 3 views: operator weekly / executive monthly / stakeholder summary.
- Automated alerts на CPA breach / IS drop / CR decline.
- Mandatory segment breakdowns у кожному звіті.

## Applies If (ALL must hold)

- Existing account with ≥30 days of data and 3+ campaigns.
- Stakeholder reporting cadence is weekly + monthly.
- Account spends ≥ $5k/mo (justifies dashboard overhead).
- Multi-stakeholder visibility — operator + executive + finance.

## Skip If (ANY kills it)

- Small accounts <$1k/mo — manual Sheet suffices.
- Single-campaign accounts — overhead exceeds value.
- Awareness-only campaigns with no conversion KPI.
- Newly launched account <30 days — no baseline to alert against.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Google Ads access | OAuth | platform owner |
| KPI target table | JSON | finance |
| Stakeholder map | doc | RevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-google-reporting` | Operator weekly methodology supplies the per-week pull. |
| `pro/marketing/ppc-manager/google-ads-optimization` | Optimization cycle consumes the alerts. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for google-ads-reporting | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `view-design` | sonnet | Per-audience abstraction level. |
| `alert-thresholds` | haiku | Standard 4 thresholds. |
| `action-queue-distillation` | sonnet | Rank top-5 from many findings. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dashboard-spec.md` | Dashboard spec Markdown skeleton with 3 views + alerts. |
| `templates/alerts-spec.json` | Alerts spec JSON. |
| `templates/dashboard-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-google-ads-reporting.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-google-reporting]]
- [[google-ads-optimization]]
- [[ads-budget-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
