---
slug: indie-hacker-tax-and-legal-essentials
tier: solo
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Checklist of tax + legal essentials for indie hackers operating a paying SaaS: entity, VAT, sales tax, contracts, ToS, privacy, data-retention.
content_id: "4f1e3f743d9fcd43"
complexity: medium
produces: checklist
est_tokens: 3700
tags: ["legal", "tax", "indie", "saas", "compliance", "solo"]
---
# Indie Hacker Tax and Legal Essentials

## Summary

**One-sentence:** Checklist of tax + legal essentials for indie hackers operating a paying SaaS: entity, VAT, sales tax, contracts, ToS, privacy, data-retention.

**One-paragraph:** Pins the minimum legal posture before charging credit cards: entity choice / VAT-MOSS / sales-tax nexus / customer ToS / privacy policy / data-retention / processor-agreements. Output is a versioned spec naming each item with status, evidence, and review date. Not legal advice — the methodology produces an inventory the founder takes to a lawyer.

**Ефективно для:**

- Indie founder about to flip on Stripe live mode, or already 30 days post-flip and realising they never registered for sales tax. Produces a one-page legal inventory ready for a 30-min lawyer review.

## Applies If (ALL must hold)

- Charging customers (real money, not 'donations') OR planning to ≤30 days
- Operating from a defined jurisdiction (knowable tax-residency)
- ≥1 customer is in a different jurisdiction (almost always true for SaaS)

## Skip If (ANY kills it)

- Pre-revenue side project with no monetisation plan
- Already running a CFA / lawyer-reviewed compliance program
- Regulated industry (HIPAA, finance, biometric) — needs specialist counsel

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tax-residency country + state / region | doc | personal record |
| Customer location distribution (last 30 days) | table | Stripe / payment processor |
| List of data processors (Stripe, Cloudflare, OpenAI, hosting, email) | table | stack inventory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/freelancer-personal-crm-minimal` | Peer methodology — provides client contracts inventory. |
| `solo/pm/outsource-onboarding-one-pager-template` | Peer methodology — contractor agreements feed into the legal inventory. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-indie-hacker-tax-and-legal-essentials` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-indie-hacker-tax-and-legal-essentials` | haiku | Schema check + threshold checks; deterministic. |
| `review-indie-hacker-tax-and-legal-essentials` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/indie-hacker-tax-and-legal-essentials.json` | JSON skeleton conforming to the output contract schema. |
| `templates/indie-hacker-tax-and-legal-essentials.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-indie-hacker-tax-and-legal-essentials.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[outsource-onboarding-one-pager-template]]
- [[freelancer-personal-crm-minimal]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
