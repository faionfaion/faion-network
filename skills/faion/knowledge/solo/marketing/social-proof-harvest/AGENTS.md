---
slug: social-proof-harvest
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Generates a four-stage harvest playbook-step (detect → capture → consent → publish) that turns spontaneous public mentions into permissioned testimonials on a wall page."
content_id: "6d3b3e486aa876bc"
complexity: medium
produces: playbook-step
est_tokens: 4000
tags: [social-proof, testimonials, consent, harvest, wall]
---

# Social Proof Harvest

## Summary

**One-sentence:** Generates a four-stage harvest playbook-step (detect → capture → consent → publish) that turns spontaneous public mentions into permissioned testimonials on a wall page.

**Ефективно для:** Solo founders with ≥1 organic mention/week on public channels who leak 80% of social proof because moments fly past without capture.

**One-paragraph:** Existing testimonial methodologies cover the ASK pattern. They don't cover the HARVEST pattern: detect when someone mentions you in public, capture the quote with author identity, run a permission flow, and publish to the wall. This playbook-step defines the four-stage loop (detect → capture → consent → publish), the storage schema that lets one quote drive multiple surfaces, and the consent + citation rules that keep the harvest legal and credible.

## Applies If (ALL must hold)

- Product has ≥1 organic mention/week across public channels.
- Operator owns the website where the wall lives.
- A lightweight detection workflow (search alerts, Brand24, n8n scrape) can be set up.
- A single source-of-truth quote DB (Notion/Airtable/JSON) is chosen.

## Skip If (ANY kills it)

- Zero organic mentions — fix distribution first; harvest needs signal.
- B2B niche under NDA — switch to permissioned-customer-quote ASK pattern.
- Operator refuses to log consent — pattern is legally non-compliant without it.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| mention-detection workflow (saved search/scraper) | URL or workflow ID | self-managed |
| quote DB schema choice (Notion/Airtable/JSON) | string | founder decision |
| consent request template (DM + email variants) | markdown | internal copy bank |
| wall page template (HTML/MD) | template path | frontend repo |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/growth-customer-testimonials` | Adjacent ASK pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `classify_mention_relevance` | haiku | Bounded relevance filter. |
| `draft_consent_request` | sonnet | Personalised DM/email with quote in context. |
| `review_legal_exposure` | opus | Cross-input judgement on consent edge cases. |

## Templates

| File | Purpose |
|---|---|
| `templates/social-proof-harvest.json` | JSON Schema for the output contract. |
| `templates/social-proof-harvest.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-social-proof-harvest.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[growth-customer-testimonials]] — paired ASK pattern.
- [[shutdown-customer-email-pack]] — sunset-survey quote harvest variant.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
