---
slug: indie-mini-crm-notion
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A Notion-shaped mini-CRM for indie hackers tracking newsletter subscribers, affiliate partners, cold-DM outreach, and customer-success touches without a paid CRM.
content_id: "c7687893eeacbef2"
tags: [indie-hacker, crm, notion, newsletter, affiliate, outreach]
---
# Indie Mini-CRM (Notion)

## Summary

**One-sentence:** A Notion-shaped mini-CRM for indie hackers tracking newsletter subscribers, affiliate partners, cold-DM outreach, and customer-success touches without a paid CRM.

**One-paragraph:** Indie hackers operate a different shape than freelancers — fewer 1:1 client relationships, more many-to-many newsletter / community / affiliate flows. HubSpot doesn't fit, and a single spreadsheet collapses past ~50 contacts. This methodology defines a four-database Notion workspace (Contacts, Outreach, Partners, Touches) with linked relations, a one-screen "today" dashboard, and three rituals: morning outreach batch, weekly partner review, monthly community pulse. Mechanism: a closed contact-type enum (subscriber / customer / partner / prospect / VIP), a single "last_touch_date" pattern for stalling detection, and templated DM / email outreach with response-rate tracking. Primary output: a Notion workspace that survives 6 months of indie hustle without becoming a graveyard of half-tagged contacts.

## Applies If (ALL must hold)

- operator runs an indie product (paid newsletter, micro-SaaS, info product) with ≥ 50 contacts across channels
- monthly revenue ≥ $200 (overhead exceeds value below this)
- operator has Notion workspace OR is willing to set one up
- operator does outbound (DMs, email outreach, affiliate sourcing) ≥ weekly
- operator currently tracks contacts in Twitter DMs, Gmail labels, spreadsheets, or memory

## Skip If (ANY kills it)

- operator has a paying CRM (HubSpot, Pipedrive, Close, ConvertKit Creator with CRM) — switching cost beats gain
- pure 1:1 client business (freelance) — use `freelancer-personal-crm-minimal` instead
- &gt; 5,000 contacts — Notion performance degrades; move to Airtable or PostgreSQL
- team of ≥ 2 — needs multi-user permissions; Notion's are too coarse for delicate role splits
- pure paid-traffic operation (no manual outreach) — CRM overhead isn't justified

## Prerequisites (must be true before starting)

- Notion workspace (free tier OK)
- export of existing contacts (Twitter, newsletter platform, Gmail labels) in CSV
- decision on contact-type taxonomy (default: subscriber / customer / partner / prospect / VIP)
- recurring calendar slot for morning outreach batch + weekly partner review

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/growth-newsletter-growth` | Subscribers data feeds Contacts table |
| `solo/marketing/content-marketer/growth-onboarding-emails` | Triggered when contact becomes customer |
| `solo/pm/project-manager/freelancer-personal-crm-minimal` | Peer for the 1:1 freelance case |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: four-database schema, closed contact-type enum, last_touch tracking, outreach response-rate, monthly community pulse | ~1000 |
| `content/02-output-contract.xml` | essential | Per-database fields, linked relations, today-dashboard requirements | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (over-tagging, ghost contacts, automation overdose, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `notion_schema_scaffold` | haiku | Bootstrap 4 databases with closed-enum properties |
| `outreach_template_draft` | sonnet | Personalized DM / email templates per contact type |
| `stall_detector_summary` | sonnet | Find contacts with no touch in 30+ days, by type |
| `monthly_pulse_synth` | sonnet | Roll up monthly subscriber + partner stats into one-screen view |

## Templates

| File | Purpose |
|------|---------|
| `templates/notion-schema.md` | Database properties for Contacts / Outreach / Partners / Touches |
| `templates/outreach-templates.md` | Cold-DM and warm-follow-up templates |
| `templates/today-dashboard.md` | Linked-view "today" dashboard recipe |
| `templates/monthly-pulse.md` | Monthly review template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/csv-import-mapper.py` | Map CSV columns to Notion DB fields | Initial seeding |
| `scripts/stall-detector.py` | Flag contacts past stall threshold by type | Morning batch ritual |

## Related

- parent skill: `solo/marketing/content-marketer/`
- peer methodology: `growth-newsletter-growth`, `freelancer-personal-crm-minimal`
- external: [Notion CRM templates](https://www.notion.so/templates/category/crm) · [Indie Hackers community](https://www.indiehackers.com/)
