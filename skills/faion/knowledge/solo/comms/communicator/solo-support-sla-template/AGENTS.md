---
slug: solo-support-sla-template
tier: solo
group: comms
domain: communicator
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "21780d1bc0ca3328"
summary: Solo-SaaS support SLA tiers (free/paid/enterprise) with reply-time bands and canned-reply templates that protect founder calendar while signalling responsiveness.
tags: [support, sla, customer-success, solo-saas, templates]
---

# Solo Support SLA Template

## Summary

**One-sentence:** Solo-SaaS support SLA tiers (free/paid/enterprise) with reply-time bands and canned-reply templates that protect founder calendar while signalling responsiveness.

**One-paragraph:** Enterprise support tooling (Zendesk, Intercom, Help Scout) ships with SLA configuration UI assuming a support team. Solo SaaS founders inherit either "zero SLA" (chaos, churn from feeling unheard) or "I reply in &lt; 1 hour always" (founder burnout, work nights). This methodology defines three default tiers (Community 72h business hours, Paid 24h business hours, Enterprise 4h business hours + Slack channel) with canned-reply skeletons, a tier-routing rule based on customer status, and an explicit "after-hours" boundary. Output: a 1-page SLA page for the website + 4 canned-reply templates + Help Scout/Intercom routing rules.

## Applies If (ALL must hold)

- operator runs a solo SaaS or solo-led service with ≥ 20 active users
- support volume ≥ 5 messages/week (below this an SLA is theatre)
- operator has ≥ 1 inbound channel (email, in-app chat, Discord)
- operator has a publicly visible "support" page or footer link

## Skip If (ANY kills it)

- operator runs a 2-3 person team — use proper helpdesk SLA + on-call rotation
- product is dev-tool with technical CSAT (e.g. Sentry) — community Slack rules dominate
- support volume &lt; 5/week — handle ad-hoc; no formal SLA needed
- operator already burned out — fix burnout first, SLA later

## Prerequisites

- list of all support inbound channels and current response times (real numbers, last 30 days)
- distinction between tiers (paid plan IDs, free plan IDs)
- operator's working hours and timezone
- one prior week of support transcripts (anonymised) for canned-reply tuning

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter/communication-templates` | Shared canned-reply structure |
| `solo/marketing/conversion-optimizer/solo-lead-qualification-rubric` | Triages support requests that are actually sales inquiries |
| `solo/pm/project-manager/solo-time-tracking-discipline` | Time budget for support work feeds the rate-floor |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: tiering, business-hours boundary, canned-reply discipline, escalation, churn-signal | ~900 |
| `content/02-output-contract.xml` | essential | `SLAPolicy` schema + canned reply schema | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: tier creep, after-hours leakage, snark, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tier_classification_from_ticket` | haiku | Lookup against customer table |
| `canned_reply_draft` | sonnet | Template fill + tone matching |
| `escalation_decision` | sonnet | Bounded judgment |
| `policy_drafting` | sonnet | Synthesis from inputs |

## Templates

| File | Purpose |
|------|---------|
| `templates/sla-policy.md` | Public SLA page |
| `templates/canned-replies.yaml` | 4 canned reply skeletons |
| `templates/sla-policy.json` | Machine-readable policy |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/audit-reply-times.py` | Compares actual reply times vs SLA bands | Weekly inbox sweep |

## Related

- parent skill: `solo/comms/communicator/`
- peer methodologies: `solo-time-tracking-discipline`, `customer-support-workflows`
- external: [Help Scout — Solo Support Setup](https://www.helpscout.com/solo-founder-support/) · [Patrick McKenzie — On Auto-Replies](https://www.kalzumeus.com/) · [Intercom SLA primer](https://www.intercom.com/help/en/articles/16-set-up-slas)
