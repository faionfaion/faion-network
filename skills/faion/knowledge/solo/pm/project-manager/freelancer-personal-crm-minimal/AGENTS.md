---
slug: freelancer-personal-crm-minimal
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A 30-minute-to-setup personal CRM in Notion / Airtable / plaintext covering leads, active clients, follow-up cadence, and payment reliability for solo freelancers.
content_id: "137ef1d51b4b0451"
tags: [freelancer, crm, solo, notion, airtable, follow-up, pipeline]
---
# Freelancer Personal CRM (Minimal)

## Summary

**One-sentence:** A 30-minute-to-setup personal CRM in Notion / Airtable / plaintext covering leads, active clients, follow-up cadence, and payment reliability for solo freelancers.

**One-paragraph:** Defines the minimum-viable schema and operating rituals a solo developer needs to never drop a lead, never forget a follow-up, and never let an unpaid invoice age past 45 days — without HubSpot or any team-shaped tool. Mechanism: three flat tables (Leads, Clients, Invoices) with five mandatory fields each, two recurring rituals (Monday 30-min review, Friday 15-min cash check), and a deterministic state machine for every lead. Primary output: a single dashboard view that answers three questions in 60 seconds — "who owes me a reply", "who owes me money", "what is my next 30-day cash forecast".

## Applies If (ALL must hold)

- operator is a solo freelancer or contractor with no sales support
- active pipeline ≥ 3 simultaneous leads OR ≥ 2 active clients
- operator currently tracks leads in chat windows, inbox flags, or sticky notes
- monthly revenue from freelance work ≥ $500 (otherwise overhead exceeds value)
- operator has access to one of: Notion, Airtable, Google Sheets, plaintext editor

## Skip If (ANY kills it)

- operator already runs HubSpot / Pipedrive / Close — switching cost dwarfs gain
- operator is a team of ≥ 3 with shared pipeline — needs multi-user permissions
- operator has < 3 leads/quarter — a single text file is enough
- engagements are subscription / SaaS (no lead-to-deal flow) — use churn cohort instead

## Prerequisites (must be true before starting)

- decision on workspace tool: Notion, Airtable, Google Sheets, or plain markdown
- list of currently-active leads (≥ 3) and clients (≥ 1) to seed the tables
- current invoice ledger (any format) for the last 90 days
- calendar slot reserved for Monday-morning 30-minute weekly review (recurring)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/capacity-fit-calculator` | Lead-qualification gate uses capacity output |
| `solo/marketing/content-marketer/growth-onboarding-emails` | Triggered when lead transitions to client |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: schema minimalism, state machine, follow-up cadence, payment alarm, weekly ritual | ~1000 |
| `content/02-output-contract.xml` | essential | Required fields per table, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detectors and repairs | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `setup_schema_from_template` | haiku | Mechanical scaffold of three tables in chosen tool |
| `weekly_review_summarizer` | sonnet | Read pipeline state, surface stalled leads + overdue invoices |
| `lead_state_transition_advisor` | sonnet | Decide whether a lead moves stage based on last-touch evidence |

## Templates

| File | Purpose |
|------|---------|
| `templates/notion-schema.md` | Notion database properties for Leads / Clients / Invoices |
| `templates/weekly-review-checklist.md` | Monday 30-min ritual script |
| `templates/follow-up-cadence.md` | Default 3-7-14-30 day follow-up rules |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/invoice-aging-check.py` | Flag invoices > 30 days unpaid | Friday cash check ritual |
| `scripts/lead-stall-detector.py` | Flag leads with no contact > 14 days | Monday weekly review |

## Related

- parent skill: `solo/pm/project-manager/`
- peer methodology: `solo/pm/capacity-fit-calculator/`
- external: [Stripe Invoice API docs](https://docs.stripe.com/api/invoices) · [Notion CRM templates](https://www.notion.so/templates/category/crm)
