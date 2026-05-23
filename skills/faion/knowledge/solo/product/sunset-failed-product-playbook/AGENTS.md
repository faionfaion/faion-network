---
slug: sunset-failed-product-playbook
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: End-to-end sunset playbook: refund policy, customer migration plan, domain reuse / archive, asset salvage, public retro — shutters a failing product gracefully and reclaims learning + leverage for the next bet.
content_id: "f8fabace1f007c94"
complexity: medium
produces: playbook-step
est_tokens: 3600
tags: [sunset-failed-product-playbook, shutdown, retro, solo]
---
# Sunset Failed Product Playbook

## Summary

**One-sentence:** End-to-end sunset playbook: refund policy, customer migration plan, domain reuse / archive, asset salvage, public retro — shutters a failing product gracefully and reclaims learning + leverage for the next bet.

**One-paragraph:** End-to-end sunset playbook: refund policy, customer migration plan, domain reuse / archive, asset salvage, public retro — shutters a failing product gracefully and reclaims learning + leverage for the next bet. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Sunset Failed Product Playbook on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Product has missed its kill threshold ≥2 quarters in a row.
- Active customer base ≤25 and not growing.
- Founder has accepted the verdict and committed to sunset.
- Continuing costs LLM / hosting / support > revenue.

## Skip If (ANY kills it)

- Product is profitable — don't sunset profitable bets.
- Founder hasn't accepted the verdict — do retro first.
- Contractual obligation extends beyond 30 days — fulfil first.
- Acquisition offer pending — pause sunset, evaluate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Customer count + revenue snapshot | dashboard | Stripe + analytics |
| Kill-threshold record | doc | Roadmap |
| Asset inventory (domain, code, docs) | table | Self |
| Migration / alternative product list | list | Research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/solo-go-no-go-criteria` | Verdict gate upstream. |
| `solo/comms/communicator/public-communication` | Retro post drafting. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-sunset-failed-product-playbook` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-sunset-failed-product-playbook` | haiku | Schema check + threshold checks; deterministic. |
| `review-sunset-failed-product-playbook` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sunset-failed-product-playbook.json` | JSON skeleton conforming to the output contract schema. |
| `templates/sunset-failed-product-playbook.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sunset-failed-product-playbook.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[solo-go-no-go-criteria]]
- [[product-launch]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
