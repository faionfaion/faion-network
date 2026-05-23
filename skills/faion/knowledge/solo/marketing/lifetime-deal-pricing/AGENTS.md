---
slug: lifetime-deal-pricing
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Indie LTD-pricing kit: floor/cap math, scarcity ladder, refund-policy guardrails — produces a versioned spec for an AppSumo/Gumroad LTD that does not torch future MRR."
content_id: "557594bb3c2e17b9"
complexity: medium
produces: spec
est_tokens: 4900
tags: [marketing, solo, pricing, lifetime-deal, indie]
---
# Lifetime Deal Pricing

## Summary

**One-sentence:** Indie LTD-pricing kit: floor/cap math, scarcity ladder, refund-policy guardrails — produces a versioned spec for an AppSumo/Gumroad LTD that does not torch future MRR.

**One-paragraph:** Indie LTD-pricing kit: floor/cap math, scarcity ladder, refund-policy guardrails — produces a versioned spec for an AppSumo/Gumroad LTD that does not torch future MRR. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- An indie operator is preparing or refreshing an AppSumo / Gumroad / standalone Lifetime Deal campaign within the next 90 days.
- The product has a recurring-SaaS analog and the operator can quantify steady-state CAC + LTV before pricing the LTD.
- A named owner exists who will publish the LTD-pricing spec and own the runbook through campaign close.
- An auditable source-of-truth for usage caps, refund policy, and roadmap commitments is available (docs / dashboard / ToS draft).

## Skip If (ANY kills it)

- Operator wants ongoing subscription pricing — use `ops-pricing-strategy` + `ops-subscription-models` instead.
- Product has no recurring-SaaS analog (one-off purchase already) — LTD pricing is meaningless.
- Roadmap commitments cannot be capped — LTD without a usage cap converts paying users into liabilities.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Lifetime Deal Pricing task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `solo/sdd/sdd/AGENTS.md` | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ltd-pricing-spec.md` | Markdown skeleton: floor/cap math, scarcity ladder, refund-policy block, post-LTD migration plan. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lifetime-deal-pricing.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[ph-launch-day-runbook]]
- [[post-launch-conversion-drip]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
