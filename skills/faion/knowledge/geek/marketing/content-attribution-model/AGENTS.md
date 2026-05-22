---
slug: content-attribution-model
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a content-attribution report mapping each long-form piece to first-touch, lift-test, and assisted-conversion contribution, with attribution windows pinned and the owner accountable."
content_id: "eb89b802fceefc3f"
complexity: deep
produces: report
est_tokens: 2900
tags: [content-attribution, multi-touch, growth, content-marketing, geek]
---

# Content Attribution Model

## Summary

**One-sentence:** Produces a content-attribution report mapping each long-form piece to first-touch, lift-test, and assisted-conversion contribution, with attribution windows pinned and the owner accountable.

**One-paragraph:** Tying long-form content to downstream revenue is a multi-touch attribution problem distinct from paid-ad attribution. Faion already covers ads attribution; this methodology fills the content side: per-piece first-touch counts (from UTM + GA4), assisted conversions (data-driven attribution), and where possible a lift estimate from a content-holdout group. Output is a ranked content portfolio with revenue contribution per piece, owner-signed, attribution windows pinned, and a refresh cadence.

**Ефективно для:** B2B content teams justifying budget to finance; SaaS growth teams ranking their content portfolio; agencies reporting content ROI to clients.

## Applies If (ALL must hold)

- Long-form content (blog, newsletter, podcast, video) has been running for ≥90 days
- UTM tagging is consistent across owned channels
- Conversion event is wired and visible in analytics
- Finance or content lead will use the report to make budget decisions

## Skip If (ANY kills it)

- Less than 90 days of consistent UTM tagging — too noisy for stable attribution
- Single-piece content (one launch post) — overkill for one artefact
- Pure brand / awareness content with no conversion event — measure differently

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Per-piece UTM + GA4 export | CSV | analytics warehouse |
| Data-driven attribution model output | CSV | GA4 / Adobe Analytics |
| Content inventory with publish dates | YAML / sheet | CMS export |
| Optional: content holdout / lift test | Note + estimate | growth experiment log |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/marketing-manager` | parent role context |
| [[blended-cac-model]] | feeder of paid-channel CAC |

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
| `collect_per_piece_data` | haiku | Mechanical extraction across UTM + analytics |
| `rank_by_revenue` | sonnet | Bounded scoring with typed inputs |
| `write_executive_summary` | opus | Cross-piece narrative for finance/board |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-attribution-model.json` | JSON schema for the attribution report |
| `templates/content-attribution-model.md` | Markdown skeleton with per-piece table |
| `templates/_smoke-test.json` | Minimum-viable filled example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-content-attribution-model.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[blended-cac-model]]
- [[anti-slop-rubric]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether content-attribution-model applies: root question — "Is the portfolio measured against a single conversion event with ≥90 days of UTM-tagged data?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision, r6-window-pinned.
