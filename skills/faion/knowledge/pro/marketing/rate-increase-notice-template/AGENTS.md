---
slug: rate-increase-notice-template
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Rate Increase Notice Template — pinned template for the technical freelancer: fixed shape + named owner + evidence anchors + outcome review, so quarterly portfolio rebalance (cash, clients, capacity) stops being folklore and starts being a reviewable operating tool.
content_id: "b2e51e1d022a66fe"
complexity: medium
produces: spec
est_tokens: 4400
tags: [marketing, pro, template, rate, increase, notice]
---
# Rate Increase Notice Template

## Summary

**One-sentence:** Rate Increase Notice Template — pinned template for the technical freelancer: fixed shape + named owner + evidence anchors + outcome review, so quarterly portfolio rebalance (cash, clients, capacity) stops being folklore and starts being a reviewable operating tool.

**One-paragraph:** In growth and marketing, the technical freelancer runs quarterly portfolio rebalance (cash, clients, capacity) on a recurring cadence — but the corpus only covers the upstream concepts, not the artefact that closes the loop. Plain-language, low-friction rate-increase letter that minimizes churn — neither pricing-strategy nor difficult-conversations gives the exact artefact. `rate-increase-notice-template` pins the artefact: a fixed shape, named owner, evidence anchors, and a published review cadence. It is loaded when the technical freelancer starts the block named in the trigger and produces a committed artefact reviewed against outcomes at the next iteration. Mechanism: rule-bound output contract + per-application evidence + outcome review. Primary output: a versioned, owned, evidence-anchored template committed to the team's knowledge space.

**Ефективно для:**

- Щорічного підвищення ставки існуючим клієнтам без втрати договору.
- Команди з ≥3 клієнтів — фіксована форма + named owner + версія.
- Outcome-review після кожного циклу: чи лист справді конвертує без churn.
- Plain-language шаблон проти боротьби з ad-hoc "листами з підвищенням".

## Applies If (ALL must hold)

- the block this methodology unblocks is on the operating cadence: - `p3-technical-freelancer/Quarterly portfolio rebalance (cash, clients, capacity)`
- the technical freelancer owns the artefact (or escalates ownership to a named role).
- the team uses a version-controlled or wiki-style space where the artefact lives.
- the methodology's trigger event fires at a published cadence (event, threshold, or schedule).

## Skip If (ANY kills it)

- one-shot work with no recurrence — write a single doc, not a versioned artefact.
- team has < 3 instances per year — the review cadence costs more than it returns.
- regulated context that mandates a different shape (use the regulator's template instead).
- no named owner is available — defer until ownership is resolved; an anonymous artefact rots.

## Prerequisites

- access to the repository / knowledge space that will host the artefact.
- a named owner accountable for refresh and outcome review.
- the upstream methodologies in `Assumes Loaded` are already routine for the technical freelancer.
- the trigger event is observable (alert, ticket, calendar slot, threshold crossing).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/rate-raise-conversation-script` | Upstream — the live conversation that follows this written notice. |
| `pro/marketing/retainer-pricing-methodology` | Upstream — the pricing model the new rate maps to. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/rate-increase-notice-template.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/rate-increase-notice-template.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rate-increase-notice-template.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/`
- [[rate-raise-conversation-script]]
- [[retainer-pricing-methodology]]
- [[solo-retainer-reactivation-cadence]]
- external: see Christensen, Gawande, Kahneman, Allspaw and the empirical sources cited in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

