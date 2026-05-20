---
slug: saas-stack-audit-micro-agency
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: SaaS Stack Audit (Micro-Agency): a 60-minute quarterly review that catches duplicate / unused SaaS tools draining $200-1k/mo from a small services firm.
content_id: "50bd3e2296e468a2"
tags: [saas-stack-audit-micro-agency, pm, pro]
---
# SaaS Stack Audit (Micro-Agency)

## Summary

**One-sentence:** A 60-minute quarterly audit that produces a typed inventory of every SaaS subscription, flags duplicates / dormant tools, and yields a signed kill-list — sized for a micro-agency (1–10 people) where tool sprawl quietly bleeds $200–1000/month.

**One-paragraph:** Existing ops-financial-basics covers bookkeeping but does not cover tool sprawl, which is the single most common silent leak for micro-agencies. Owners onboard a tool per project, never offboard, and a year later pay for three project-management tools, two file-shares, and a forgotten Loom Pro seat. This methodology defines the audit inputs (corporate card statement, browser-bookmarks export, last-login report where the vendor provides one), the five classification buckets (keep, consolidate, downgrade-seat, suspend, cancel), the override rule for "feels-important-but-no-evidence", and the kill-list signing process. Output is a typed audit record per quarter with measured spend before/after.

## Applies If (ALL must hold)

- the agency has at least 5 distinct SaaS subscriptions (below this, the audit is overhead)
- at least one quarter since previous audit, OR first-ever audit
- access to corporate card statement and/or accounting export covering ≥3 months
- tier == pro or higher

## Skip If (ANY kills it)

- the agency has formal procurement / FinOps process — extend it, do not duplicate
- a major project ramp is starting this week — defer audit to post-ramp (new tools settling)
- annual contracts dominate the stack and none are within 60 days of renewal — defer to renewal window

## Prerequisites

- last 3 months of card / accounting export filtered to recurring SaaS charges
- list of active client engagements (for "is this tool tied to a paying client?" check)
- last-login report per vendor where available
- founder / ops lead 60-minute focused block

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill |
| `solo/marketing/content-marketer` | provides context on which tools tie to revenue-generating workflow |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: full-stack-inventory, classification-bucket, evidence-required-to-keep, kill-list-signed, savings-tracked-next-quarter | ~1100 |

## Related

- parent skill: `pro/pm/project-manager`
- upstream playbook: `p5-micro-agency-founder/Vendor / tool consolidation review`
- sibling methodology: `pro/pm/vendor-management-pm`
