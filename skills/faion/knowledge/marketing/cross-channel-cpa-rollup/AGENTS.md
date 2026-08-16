# Cross-Channel CPA Rollup

## Summary

**One-sentence:** Single normalized weekly CPA rollup across paid channels — last non-direct click default, gross spend incl. fees, dedup customer ID, organic baseline, 90-day cohort lens.

**One-paragraph:** Attribution mess is the dominant pain in pro-tier growth marketing: Meta claims the conversion, Google claims the same user, LinkedIn says it nurtured, and the CPA the business actually pays is unknowable. This methodology pins five things: a single attribution model (last non-direct click default + view-through caveat); channel-level cost normalization (gross spend incl. agency fees); deduplication via a unifying customer ID; an organic+referral baseline so paid is not credited for organic conversions; a per-channel cohort lens (cohort retention over 90 days, not single-touch CPA). Output: a weekly rollup report (spreadsheet + dashboard) with consistent columns across the team.

**Ефективно для:**

- Multi-channel paid ads — ≥2 channels одночасно з різними CPA claims.
- Quarterly бюджетне ре-allocation — потрібен чесний внутрішній CPA для рішень.
- Audit агентства / contractor — гарантує що звітні цифри не cherry-picked.
- Перевірка cannibalization branded paid → organic.

## Applies If (ALL must hold)

- Business runs ≥ 2 paid channels concurrently.
- A unifying customer ID exists (email, user ID, anonymized identifier).
- Weekly or biweekly paid-ads review is a standing ritual.
- Attribution disputes between channels have been a recurring topic.

## Skip If (ANY kills it)

- Single-channel business (only Google Ads or only one referral source) — no rollup needed.
- Pre-paid stage with no spend yet — set up the framework but populate later.
- Pure brand-building campaign with no direct-response goal — CPA is not the right metric.
- Highly regulated industry where attribution data crosses consent boundaries — consult privacy counsel first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tracking layer | GA4 / Segment / server-side tagging | analytics infra |
| Per-channel spend export | API or weekly CSV | ad platform |
| Customer / conversion record store | CRM or warehouse | source-of-truth |
| Data destination | Sheets / Looker Studio / Metabase | BI tool |
| Attribution policy doc | Markdown, versioned | growth team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[utm-taxonomy-discipline]] | Source/medium tagging consistency assumed. |
| [[multi-touch-attribution-modeling]] | Background on attribution-model trade-offs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: single attribution model, gross spend, dedup ID, organic baseline, cohort lens | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the rollup row + required columns + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: double-count, missing fees, view-through abuse, branded cannibalization, missing cohort, silent policy change | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: pull spend → pull conversions → dedup → attribute → compute incrementality → publish | 700 |
| `content/05-examples.xml` | essential | Worked weekly rollup for a 3-channel business | 500 |
| `content/06-decision-tree.xml` | essential | Tree mapping observable signals (branded share, view-through %, dedup coverage) to the rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pull-spend-per-channel` | haiku | Mechanical from APIs / CSVs. |
| `dedup-and-attribute` | sonnet | Bounded logic: pick the last non-direct touch. |
| `cohort-retention-summary` | opus | Cross-channel synthesis over 90-day window. |
| `lint-rollup-row` | haiku | Schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rollup-sheet.csv` | Weekly columns: channel, gross spend, attributed conversions, CPA, view-through count, 90d cohort retention. |
| `templates/attribution-policy.md.j2` | Pinned attribution model + view-through window + appeal process. |
| `templates/attribution-policy.md` | Pinned attribution model + view-through window + appeal process. Generated from `templates/attribution-policy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/rollup-row.json` | JSON example matching the output contract. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cross-channel-cpa-rollup.py` | Validate one rollup-row JSON against the schema | Weekly, before publish. |

## Related

- [[utm-taxonomy-discipline]]
- [[multi-touch-attribution-modeling]]
- [[daily-ads-anomaly-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes the agent from the observable signal (e.g. "view-through count > attributed conversions", "branded share > 30%") to the rule that gates the fix. Use it before publishing a rollup that looks too rosy or too dire — the explanation is usually a rule violation upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rollup-sheet.csv`

```csv
week,channel,gross_spend_usd,self_reported_conversions,attributed_conversions,view_through_count,cpa_gross,incremental_over_organic,cpa_incremental,cohort_d30_retention,cohort_d60_retention,cohort_d90_retention,attribution_policy_version,notes
2026-W20,Meta-paid,4800.00,51,32,18,150.00,22,218.18,0.71,,,1.2.0,Includes $600 agency fee
2026-W20,Google-search,3200.00,42,28,4,114.29,21,152.38,0.83,,,1.2.0,
2026-W20,Organic,0,,60,,0,60,0,0.84,,,1.2.0,
```

### `templates/rollup-row.json`

```json
{
  "week": "2026-W20",
  "channel": "Meta-paid",
  "gross_spend_usd": 4800.0,
  "attributed_conversions": 32,
  "self_reported_conversions": 51,
  "view_through_count": 18,
  "cpa_gross": 150.0,
  "incremental_over_organic": 22,
  "cpa_incremental": 218.18,
  "cohort_d30_retention": 0.71,
  "cohort_d60_retention": null,
  "cohort_d90_retention": null,
  "attribution_policy_version": "1.2.0",
  "notes": "Includes $600 agency fee."
}
```
