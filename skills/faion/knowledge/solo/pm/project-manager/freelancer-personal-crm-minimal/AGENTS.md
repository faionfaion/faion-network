---
slug: freelancer-personal-crm-minimal
tier: solo
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Single-table CRM for solo freelancers: lead → qualified → proposal → signed → active → churned — ≤12 fields, weekly review.
content_id: "137ef1d51b4b0451"
complexity: medium
produces: spec
est_tokens: 3700
tags: ["crm", "freelancer", "pm", "solo", "pipeline"]
---
# Freelancer Personal CRM (Minimal)

## Summary

**One-sentence:** Single-table CRM for solo freelancers: lead → qualified → proposal → signed → active → churned — ≤12 fields, weekly review.

**One-paragraph:** Pins the minimum-viable CRM for solo freelancers: one table, 6 named pipeline stages, ≤12 fields per record, weekly review cadence. Output is a versioned spec covering schema + stage rules + review cadence + integration points (calendar + email). Avoids HubSpot bloat.

**Ефективно для:**

- Solo freelancer or contractor whose 'CRM' is a mess of emails + Notion pages + WhatsApp chats. One table, 6 stages, weekly Friday review keeps the pipeline visible without a full sales tool.

## Applies If (ALL must hold)

- Solo freelancer / consultant / contractor with ≥3 active prospects + clients
- Current pipeline tracked across multiple unstructured channels
- Founder commits ≥30 min/week to review

## Skip If (ANY kills it)

- Single ongoing client — overkill
- Already use HubSpot / Pipedrive successfully
- Inbound is purely platform-driven (Upwork / Fiverr) with no follow-up

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing prospect + client list | list | email + calendar |
| Calendar slot for weekly review | calendar event | calendar |
| Notion / Airtable / Google Sheet workspace | URL | tool admin |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/client-visibility-vs-velocity-tradeoff` | Peer methodology — pipeline stage drives cadence tier choice. |
| `solo/pm/indie-hacker-tax-and-legal-essentials` | Peer methodology — moving to Active triggers contract + tax registration. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-freelancer-personal-crm-minimal` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-freelancer-personal-crm-minimal` | haiku | Schema check + threshold checks; deterministic. |
| `review-freelancer-personal-crm-minimal` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelancer-personal-crm-minimal.json` | JSON skeleton conforming to the output contract schema. |
| `templates/freelancer-personal-crm-minimal.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-personal-crm-minimal.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[client-visibility-vs-velocity-tradeoff]]
- [[indie-hacker-tax-and-legal-essentials]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
