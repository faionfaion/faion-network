---
slug: single-page-case-study-generation
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Single Page Case Study Generation — a service-engagement case-study template (problem / approach / outcome / numbers / pull-quote / NDA fallback) for technical freelancers productizing recurring work.
content_id: "7270e757141eeee0"
complexity: medium
produces: report
est_tokens: 4000
tags: [single-page-case-study-generation, marketing, pro]
---
# Single Page Case Study Generation

## Summary

**One-sentence:** A one-page case-study template tuned for service engagements (not SaaS feature launches) with six required slots — problem, approach, outcome, numbers, pull-quote, NDA-safe fallback — so every finished freelance project becomes a reusable sales asset within a week of delivery.

**One-paragraph:** Every finished engagement is a sales asset, but freelancers never write it up because there is no template. The case-study mentions in product/product-lifecycle are SaaS-feature-launch flavor, not service-engagement flavor. This methodology codifies the six required slots, the NDA-redaction fallback (so confidential clients still produce a usable anonymous case), and a one-week-from-delivery deadline so the write-up happens while results and quotes are still fresh.

**Ефективно для:**

- Закритого freelance-проекту: 7 днів на драфт, 14 на публікацію.
- NDA-fallback версія: industry + size + role без імен.
- Шість обов'язкових слотів (problem/approach/outcome/numbers/quote/NDA).
- Outcome-review: чи кейс справді конвертує prospects на discovery-call.

## Applies If (ALL must hold)

- the engagement is delivered, paid, and the client is reachable for quote/permission
- there is at least one quantitative outcome (revenue, latency, time, cost) you can defend with evidence
- the case study will be used as a sales asset (site, proposal pack, LinkedIn pin)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the client refuses both named and anonymous publication (one-line internal log only)
- the engagement produced no measurable outcome you can stand behind
- a SaaS-style feature-launch case study is what you actually need (different template)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Operating-trigger event | log / calendar / ticket | upstream observability |
| Methodology preconditions checklist | YAML | this methodology's `templates/single-page-case-study-generation.md` |
| Named owner contact | string | team RACI / org chart |
| Write-access to artefact store | URL | team's knowledge space |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/proposal-from-discovery-template` | Upstream artefact template that anchors this methodology's recurring loop. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)
| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 5 testable rules: six required slots, numeric outcome floor, pull-quote from client, NDA fallback, one-week deadline |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour at the next iteration? |

## Templates

| File | Purpose |
|------|---------|
| `templates/single-page-case-study-generation.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/single-page-case-study-generation.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-single-page-case-study-generation.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- upstream playbook: `p3-technical-freelancer/Productize a recurring engagement into a fixed-scope offer`
- parent skill: `pro/marketing/`
- related methodology: `pro/marketing/testimonial-capture-microsurvey`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

