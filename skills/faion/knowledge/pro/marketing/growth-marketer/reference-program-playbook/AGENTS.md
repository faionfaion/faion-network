---
slug: reference-program-playbook
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Operational playbook converting happy clients into named references, case studies, peer calls, and warm introductions — the #1 acquisition channel for micro-agencies.
content_id: "c05f8f81d582b180"
complexity: deep
produces: playbook-step
est_tokens: 4200
tags: [reference-selling, referrals, micro-agency, case-studies, b2b-services]
---
# Reference Program Playbook

## Summary

**One-sentence:** Operational playbook converting happy clients into named references, case studies, peer calls, and warm introductions — the #1 acquisition channel for micro-agencies.

**One-paragraph:** Operational playbook converting happy clients into named references, case studies, peer calls, and warm introductions — the #1 acquisition channel for micro-agencies. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Мікро-агенції (1-10 person) з 5+ delivered engagements готові формалізувати referral funnel.
- Перед запуском paid acquisition — щоб не палити бюджет коли warm channel underused.
- При переході з founder-led sales до repeatable funnel.
- Для founders що відмовляються від cold outreach — reference selling — це organic alternative.

## Applies If (ALL must hold)

- >= 5 closed engagements з verifiable client outcomes.
- Founder здатний особисто запитати reference у named clients.
- Existing relationships дозволяють case study + peer call asks.

## Skip If (ANY kills it)

- Pre-launch / 0 delivered work — nothing to reference.
- All client work під strict NDA без можливості case study / named reference.
- Founder unwilling to ask — reference selling vimagaye direct ask.

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
| `pro/marketing/growth-marketer` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/playbook-step-skeleton.md` | Reference Program Playbook skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Reference Program Playbook. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reference-program-playbook.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[agency-niche-positioning]]
- [[growth-referral-programs]]
- [[agency-discovery-call-scorecard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
