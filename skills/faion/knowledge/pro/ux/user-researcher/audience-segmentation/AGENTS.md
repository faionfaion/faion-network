# Audience Segmentation

## Summary

A structured process to divide a potential market into distinct, mutually exclusive groups using two to three differentiating dimensions (demographic, behavioural, psychographic, or needs-based), score each segment against six weighted attractiveness criteria, and select at most one primary target for pre-traction products. Segments are maintained as YAML/JSON for reproducible quarterly re-scoring.

## Why

"Everyone is our customer" erodes paid-acquisition efficiency and message resonance. Segmentation makes targeting trade-offs explicit and falsifiable: by scoring Size, Growth, Reachability, Profitability, Fit, and Competition with fixed weights, teams can defend their choice of primary segment without relying on intuition. Demographic-only segmentation is the most common failure mode — it yields lookalikes that do not predict purchase.

## When To Use

- Pre-launch positioning when the team is debating which buyer to target first.
- Post-launch when "everyone is our customer" is eroding paid-acquisition efficiency.
- Pricing-tier design that needs distinct buying behaviours and willingness-to-pay levels.
- Pivoting into a new market where the prior segmentation no longer maps.
- Product-tier or product-line decisions (free/pro/enterprise; consumer/SMB/mid-market).

## When NOT To Use

- Pre-traction MVPs with fewer than 50 customers — use one persona, not segment matrices.
- Strict niche businesses where the entire ICP fits one segment by design.
- Account-based sales motions where named accounts replace segmentation.
- Ephemeral campaigns — A/B-test creatives instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Four segmentation types, five-step process, attractiveness scoring rubric |
| `content/02-examples.xml` | Two worked examples (CRM tool, online course) with antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/segmentation-analysis.md` | Full segmentation analysis doc with scoring table and target strategy |
| `templates/segment-profile-card.md` | Single-segment profile card for stakeholder communication |
| `templates/segment.py` | k-means clustering on usage features, emits segments.json |
