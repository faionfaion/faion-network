---
slug: solo-content-calendar-template
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "b8c8ad778492f598"
summary: One-asset-per-week content calendar template anchored to the ICP's pain ladder — enforces cadence + topic relevance, no team, no editorial calendar tool.
---
# Solo Content Calendar Template

## Summary

**One-sentence:** A 12-row content calendar template — one shippable asset per week — pinned to the ICP's pain ladder and enforced by a CI-style cadence check.

**One-paragraph:** Existing content-calendar playbooks describe how a team plans a quarter. Solo founders need a stripped-down version: one row per week, one asset per row, pinned to a specific ICP pain (validated from research). The template defines required columns (week_iso, pain_ref, asset_type, target_keyword OR distribution_channel, publish_date, status), a forcing rule that next week's row must be `drafted` by Friday or this week's writing block is replaced with backfill, and a quarterly review that retires assets whose pain reference is no longer in the top-5 ICP problems. Anchored to "Weekly content & SEO atomic push" for the solo SaaS builder.

## Applies If (ALL must hold)

- Solo founder with a documented ICP (or willing to commit to one within 1 week).
- Content is a chosen growth channel (SEO, build-in-public, newsletter, social).
- Founder commits to one writing block per week.
- A pain-ladder document or research bank exists (or `solo/marketing/icp-fit-scorecard-solo` is loaded).

## Skip If (ANY kills it)

- Pre-ICP — define the ICP first; cadence without aim wastes content.
- Paid acquisition is the only growth bet — pour the writing time into ad-creative instead.
- Founder is in a feature-launch sprint and committed to going dark for ≤4 weeks — pause the calendar, do not lower the cadence.

## Prerequisites

- ICP pain ladder (3–5 ranked pains) or `solo/marketing/icp-fit-scorecard-solo` output.
- Publishing surface ready (blog, newsletter, social profile).
- Weekly writing block on the calendar.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/AGENTS.md` | Parent group context |
| `solo/marketing/icp-fit-scorecard-solo` if present | Source for the pain ladder this calendar pins to |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every weekly row enforces | ~900 |

## Related

- parent skill: `solo/marketing/`
- triggering activity: `p1-solo-saas-builder/Weekly content & SEO atomic push`
- adjacent: `solo/marketing/content-marketer`, `solo/marketing/weekly-growth-review-rhythm`
