---
slug: agency-to-agency-referral
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Codifies inbound + outbound peer-agency referral relationships (capacity overflow, out-of-niche, conflict-of-interest) \u2014 the highest-conversion lead source for a micro-agency, made repeatable with named partners, kick-back terms, and a review cadence."
content_id: "49f723349f5f5512"
complexity: medium
produces: spec
est_tokens: 5000
tags: [agency, referral, partnership, biz-dev, marketing]
---
# Agency-to-Agency Referral

## Summary

**One-sentence:** Codifies inbound + outbound peer-agency referral relationships (capacity overflow, out-of-niche, conflict-of-interest) — the highest-conversion lead source for a micro-agency, made repeatable with named partners, kick-back terms, and a review cadence.

**One-paragraph:** Codifies inbound + outbound peer-agency referral relationships (capacity overflow, out-of-niche, conflict-of-interest) — the highest-conversion lead source for a micro-agency, made repeatable with named partners, kick-back terms, and a review cadence. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Agency has a stable niche and gets ≥ 1 out-of-niche request per month worth referring.
- Founder has 5+ hours/month to invest in maintaining peer-agency relationships.
- Cash-flow can support 10-20% kick-back terms on first-engagement referrals.

## Skip If (ANY kills it)

- Pre-niche agency — peers cannot route reliably to you without a clear positioning.
- Solo freelancer with no referral capacity to give back — relationship will not be symmetric.
- Cash-flow cannot fund a kick-back program — start with no-payment-just-relationship and revisit.

**Ефективно для:**

- Мікро-агенція з достатньою niche-фокусом щоб мати out-of-niche запити що варто перенаправляти.
- Команди в нішових категоріях (legaltech, fintech) — peers мають overflow для перенаправлення.
- Засновники що хочуть стабільне 30-50% inbound від referral (не від cold outreach).
- Маленькі агенції що готові віддавати 10-20% kick-back від першого контракту peer-agency.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing-manager` | Parent role context — agency operating discipline. |
| `solo/marketing/content-marketer` | Adjacent role context — content + portfolio surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-to-agency-referral.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[agency-niche-positioning]]
- [[agency-case-study-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
