# Ads Attribution Models

## Summary

**One-sentence:** Configures attribution comparison (platform-reported / GA4-modeled / warehouse-deduped) across paid channels, with variance thresholds and quarterly geo-holdout incrementality tests.

**One-paragraph:** Each ad platform claims its own conversions with different windows + logic, so platform totals exceed actual sales by 30-80%. This methodology configures a unified comparison layer (platform / GA4 / warehouse) with 15% variance threshold for investigation, quarterly geo-holdout incrementality tests, and an auto-generated variance report. Output: attribution config spec + reconciliation pipeline + variance report template + incrementality test plan.

**Ефективно для:**

- Multi-channel paid manager з > $5k/mo і attribution mess.
- Quarterly budget review: defensible reconciled numbers замість platform sums.
- Geo-holdout incrementality test для true-incremental lift per channel.
- Auto-generated weekly variance report для exec audience.

## Applies If (ALL must hold)

- Multi-channel paid programs (2+ platforms) where totals don't match warehouse.
- GA4 + BigQuery (or equivalent warehouse) operational.
- Quarterly budget review cadence requiring defensible numbers.
- Marketing owner can authorize geo-holdout tests (2-4 weeks regional spend off).

## Skip If (ANY kills it)

- Single-channel paid spend — last-click works.
- No warehouse — implement ads-analytics-setup first.
- Spend < $5k/month — variance smaller than measurement error.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ads-attribution-models` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton with 5-line header |
| `templates/output.json` | JSON sidecar with __faion_header__ |
| `templates/_smoke-test.yaml` | Minimum viable filled config |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.
| `templates/attribution-analysis.md.j2` | legacy template for ads-attribution-models — attribution-analysis |
| `templates/attribution-analysis.md` | legacy template for ads-attribution-models — attribution-analysis Generated from `templates/attribution-analysis.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-attribution-models.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config.yaml`

```yaml
artefact_id: <SLUG-YYYY-Qx>
template_version: 1.1.0
owner: <named-owner@example>
platform: <ga4|google-ads|meta|linkedin>
settings:
  # platform-specific keys; reference 02-output-contract.xml for schema
  example_key: example_value
verification:
  verified_at: <ISO-8601>
  verified_by: <named>
  evidence: <DebugView screenshot path | CRM cross-check report path>
```

### `templates/output.json`

```json
{
  "artefact_id": "<SLUG-YYYY-Qx>",
  "template_version": "1.1.0",
  "owner": "<named-owner@example>",
  "platform": "<ga4|google-ads|meta|linkedin>",
  "settings": {
    "example_key": "example_value"
  },
  "verification": {
    "verified_at": "<ISO-8601>",
    "verified_by": "<named>",
    "evidence": "<DebugView screenshot path>"
  }
}
```

### `templates/_smoke-test.yaml`

```yaml
artefact_id: ads-config-2026-Q2
template_version: 1.1.0
owner: analytics-eng@faion.net
platform: ga4+google-ads+meta
settings:
  consent_mode_v2: true
  bq_link: true
  attribution_window_days: 30
  event_id_dedup: true
  utm_convention: lowercase-controlled-vocab
verification:
  verified_at: 2026-05-22T14:00Z
  verified_by: analytics-eng@faion.net
  evidence: evidence/ads-config-2026-Q2/debug.png
```
