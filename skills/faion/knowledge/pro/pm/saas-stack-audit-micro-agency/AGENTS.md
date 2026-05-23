---
slug: saas-stack-audit-micro-agency
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 60-minute quarterly SaaS audit sized for 1-10 person agencies; typed inventory + 5 classification buckets (keep / consolidate / downgrade / suspend / cancel) + signed kill-list + before/after savings tracked.
content_id: "e3dc8cfc257a2c43"
complexity: medium
produces: report
est_tokens: 3300
tags: [pm, pro, saas, audit, finops, micro-agency]
---
# SaaS Stack Audit (Micro-Agency)

## Summary

**One-sentence:** A 60-minute quarterly audit that produces a typed inventory of every SaaS subscription, classifies each into one of 5 buckets (keep / consolidate / downgrade-seat / suspend / cancel), yields a signed kill-list, and tracks before/after spend — sized for a 1–10 person agency where tool sprawl quietly bleeds $200–1000/month.

**One-paragraph:** Existing ops-financial-basics covers bookkeeping but not tool sprawl, which is the single most common silent leak for micro-agencies. Owners onboard a tool per project, never offboard, and a year later pay for three project-management tools, two file-shares, and a forgotten Loom Pro seat. This methodology defines audit inputs (corporate card statement, browser-bookmarks export, last-login report), five classification buckets, an explicit "feels-important-but-no-evidence" override rule, and the kill-list signing process. Output: typed `SaaSAuditReport` per quarter with measured spend before/after.

**Ефективно для:**

- Quarterly SaaS stack audit for 1-10 person agencies.
- Surfacing forgotten subscriptions ($200-1k/mo silent leak).
- Documenting kill-list with founder signature + savings forecast.
- Tracking realised savings into next-quarter inventory.

## Applies If (ALL must hold)

- Agency has ≥ 5 distinct SaaS subscriptions.
- ≥ 1 quarter since previous audit OR first-ever audit.
- Access to last 3 months card / accounting export filtered to recurring SaaS.
- Tier == pro or higher.

## Skip If (ANY kills it)

- Agency has formal procurement / FinOps process — extend it, don't duplicate.
- Major project ramp this week — defer audit to post-ramp (new tools settling).
- Annual contracts dominate and none within 60-day renewal window — defer to renewal.
- < 5 subscriptions — overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 3-month SaaS charges from card / accounting | CSV | finance |
| Active client engagements list | YAML | CRM |
| Last-login report per vendor (where available) | per-vendor | admin panels |
| Founder / ops-lead 60-min block | calendar | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[vendor-margin-defense-checklist]] | Margin signal correlates with SaaS-stack bleed. |
| [[retainer-renewal-decision-rule]] | Per-client retainer review consumes per-client SaaS attribution. |
| [[rpo-rto-negotiation-guide]] | Disaster-recovery tier choices interact with SaaS spend. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: full-stack-inventory, classification-bucket, evidence-required-to-keep, kill-list-signed, savings-tracked-next-quarter | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `SaaSAuditReport` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 5-step: inventory → classify → sign kill-list → execute → review next quarter | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: usage + revenue tie + duplicate? → keep / consolidate / downgrade / suspend / cancel | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-puller` | haiku | Mechanical pull from card export. |
| `classifier` | sonnet | Per-tool judgment on bucket. |
| `kill-list-drafter` | sonnet | Diplomatic but firm copy for cancellation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | SaaSAuditReport skeleton |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `SaaSAuditReport` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-saas-stack-audit-micro-agency.py` | Validate `SaaSAuditReport`: full-stack inventory, classification per tool, evidence on keeps, signed kill-list | Pre-merge |
| `scripts/staleness-check.py` | Flag audits whose `last_reviewed` > 90 days | Weekly cron |

## Related

- [[vendor-margin-defense-checklist]]
- [[retainer-renewal-decision-rule]]
- [[rpo-rto-negotiation-guide]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observed signals (last_login_days, tied_to_revenue, duplicate_tool, monthly_cost) to one of 5 buckets. Every leaf references a rule from `01-core-rules.xml`.
