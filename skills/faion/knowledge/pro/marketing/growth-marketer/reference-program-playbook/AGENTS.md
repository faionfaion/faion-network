---
slug: reference-program-playbook
tier: pro
group: growth-marketer
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "75710d5f0a427e9e"
summary: Operational playbook for converting existing happy clients into reference assets — named references, case studies, peer calls, and warm introductions — as the primary acquisition channel for micro-agencies.
tags: [reference-selling, referrals, micro-agency, retention, b2b-services]
---

# Reference Program Playbook

## Summary

**One-sentence:** Reference-selling system that converts happy clients into named references, case studies, and peer calls — the #1 acquisition channel for micro-agencies.

**One-paragraph:** Most micro-agency growth happens via word-of-mouth and reference calls, yet the methodology corpus only covers affiliate and influencer programs. This playbook fills that gap with a five-stage operational system: (1) qualify which clients can reference, (2) earn the reference asset (case study, quote, willingness-to-call), (3) catalogue references by buyer-archetype and outcome class, (4) deploy references in the sales cycle at the right friction point, (5) retire stale or fatigued references. It pins the legal/comms guardrails (NDA, logo permission, disclosure), the cadence (no more than 2 reference calls per client per quarter), and the asymmetric value-exchange (the reference gets something concrete: peer connection, exposure, training credit). Output: a `references.yaml` registry, asset library, and a sales-cycle deployment rule per prospect stage. Mechanism: a structured reference program with explicit consent, fatigue limits, and matched buyer-archetype routing.

## Applies If (ALL must hold)

- agency_or_consultancy_model with ≥5 happy clients (retained ≥6 months, NPS ≥ 8)
- service_business with deals ≥ $10k where social proof shortens the sales cycle
- prospects routinely ask for "people we can talk to" before signing
- founder has authority over client comms and can sign off on disclosure

## Skip If (ANY kills it)

- product-led growth SaaS with no human sales cycle — reference calls don't fit the funnel
- < 5 referenceable clients — there is nothing to deploy; focus on client outcomes first
- highly regulated industries (defence, classified gov work) where references cannot be disclosed — use redacted case studies via privileged channels instead
- founder is unwilling to ask for references — no system works without the asking step

## Prerequisites

- Roster of all current and former clients (CRM export with engagement length and NPS or qualitative satisfaction signal)
- Clear understanding of buyer archetypes from `gtm-strategist/ideal-customer-profile`
- Permission/consent process drafted with legal (or templates from this playbook)
- Storage for reference assets (Notion DB, Airtable, simple repo)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist/ideal-customer-profile` | Reference-to-prospect matching uses buyer archetypes |
| `pro/marketing/conversion-optimizer/case-study-production` | Case-study production handoff |
| `pro/pm/project-manager/client-success-cadence` | NPS / health signal feeds reference qualification |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: asymmetric value-exchange, fatigue cap, archetype-matched routing, consent-on-record, expiry | ~1000 |
| `content/02-output-contract.xml` | essential | references.yaml schema, asset taxonomy, sales-cycle deployment rules | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: reference burnout, archetype mismatch, stale logos, leaking unflattering references, etc. | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `eligible_reference_shortlist` | haiku | Filter CRM by NPS/tenure; cheap |
| `case_study_first_draft` | sonnet | Bounded narrative writing from client interview |
| `reference_archetype_match` | sonnet | Match prospect buyer-archetype to best reference in library |
| `reference_thank_you_drafts` | haiku | Templated outreach with personalisation |

## Templates

| File | Purpose |
|------|---------|
| `templates/reference-request-email.md` | Initial ask with value-exchange options |
| `templates/case-study-interview-guide.md` | 30-minute interview to extract case study |
| `templates/references.schema.yaml` | Schema for the references registry |
| `templates/peer-call-brief.md` | Brief sent to the reference before a peer call |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/fatigue-check.py` | Flags references called > 2 times this quarter | Before adding a reference to a new sales loop |
| `scripts/reference-router.py` | Given prospect archetype, returns top-3 matched references with freshness score | At opportunity-creation in CRM |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodologies: `affiliate-program-design`, `case-study-production`, `nps-program`, `customer-advisory-board`
- external: [Reichheld — The Ultimate Question 2.0](https://www.netpromotersystem.com/) · [Forrester reference-selling research](https://www.forrester.com/) · [Bain NPS](https://www.bain.com/insights/topics/customer-experience/)
