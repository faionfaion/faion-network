# Blended CAC Model

## Summary

**One-sentence:** Produces a blended customer-acquisition-cost report that reconciles platform CAC with channel-level marketing-mix lift and pins attribution windows before any data is read.

**One-paragraph:** Platform CAC routinely overstates performance vs blended CAC; this is the metric finance teams actually scrutinise. The methodology drives a first-principles blended-CAC + MMM-lite calculation: list every channel, total paid spend, total acquired customers, deduplicate cross-channel attribution via incremental lift estimate, and emit a single number plus a per-channel breakdown. Owner-signed, versioned, attribution windows pinned up front, sources cited per field. Output is the report finance, growth, and the board can argue from.

**Ефективно для:** growth marketers reconciling Meta vs Google vs organic CAC; founders preparing a CFO briefing; agencies presenting blended performance.

## Applies If (ALL must hold)

- Paid spend across two or more channels has been running for ≥30 days
- Conversion tracking is wired across all paid channels
- Finance or board reviewer will scrutinise the number
- Attribution window decision has not been frozen yet for this campaign

## Skip If (ANY kills it)

- Single-channel paid spend — platform CAC is the right metric, blended is redundant
- Less than 100 acquired customers in the window — too few data points for reliable blend
- Attribution debate already resolved upstream and frozen — this would re-litigate

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Per-channel paid spend totals | CSV / dashboard export | Meta Ads / Google Ads / LinkedIn Ads |
| Acquired-customer counts with channel tag | CSV | CRM / analytics warehouse |
| Lift / incrementality estimate | Number with method note | geo-test / holdout experiment |
| Attribution-window decision | Documented note | growth-team wiki |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/marketing-manager` | parent role context |
| [[content-attribution-model]] | downstream consumer of blended CAC |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect_channel_spend` | haiku | Mechanical extraction across dashboards |
| `compute_blended_cac` | sonnet | Bounded math with clear inputs |
| `reconcile_with_finance` | opus | Cross-input synthesis with finance pushback |

## Templates

| File | Purpose |
|------|---------|
| `templates/blended-cac-model.json` | JSON schema for the blended-CAC output contract |
| `templates/blended-cac-model.md` | Markdown report skeleton with per-channel table |
| `templates/_smoke-test.json` | Minimum-viable filled example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-blended-cac-model.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[content-attribution-model]]
- [[anti-slop-rubric]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether blended-cac-model applies: root question — "Is paid spend running across ≥2 channels for the same conversion event over ≥30 days?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-conversion-window, r6-incremental-lift.
