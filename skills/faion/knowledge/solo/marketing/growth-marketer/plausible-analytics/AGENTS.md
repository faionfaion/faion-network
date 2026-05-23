---
slug: plausible-analytics
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Plausible Analytics configuration artefact: script install snippet, goal events, custom dimensions, alerts, and per-site shared link policy — privacy-first, cookieless, GDPR-clean.
content_id: "bf9bde4ea34c5b46"
complexity: medium
produces: config
est_tokens: 4200
tags: ["analytics", "plausible", "privacy", "gdpr", "config", "solo"]
---
# Plausible Analytics Setup

## Summary

**One-sentence:** Generates a Plausible Analytics configuration artefact: script install snippet, goal events, custom dimensions, alerts, and per-site shared link policy — privacy-first, cookieless, GDPR-clean.

**One-paragraph:** Plausible Analytics Setup produces a config artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated config ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder running Gatsby/React/static site who needs privacy-first analytics with goals + alerts wired in ≤1 hour without GDPR overhead or cookie banner debt.

## Applies If (ALL must hold)

- Site is static or SPA (Gatsby, Next, React, Hugo, Astro)
- Founder wants GDPR-clean analytics without cookie banner
- Domain ownership / DNS control to add subdomain (optional but recommended)

## Skip If (ANY kills it)

- Need user-level session replay or fingerprint — wrong tool (use PostHog)
- Already on GA4 with consent banner stack — switch out of scope
- Internal app where analytics is forbidden

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Site URL | URL | deployment |
| DNS access (for subdomain script proxy) | creds | registrar |
| List of conversion events (signup, paid, demo) | list | product brief |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `ops-dashboard-setup` | Plausible widgets feed the dashboard. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-script-loaded-once, r2-goals-declared-upfront, r3-no-pii-in-custom-props, r4-subdomain-or-proxy, r5-shared-link-per-stakeholder | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-plausible-analytics` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-plausible-analytics` | haiku | Schema check + threshold checks; deterministic. |
| `review-plausible-analytics` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/plausible-analytics.json` | JSON skeleton conforming to the output contract schema. |
| `templates/plausible-analytics.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-plausible-analytics.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[ops-dashboard-setup]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
