---
slug: cohort-based-mini-course-launch
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Cohort sizing + calendar + Maven/Podia/Circle ops + course-as-lead-magnet for a $99-$499 \u00d7 20-seat indie monetization sprint."
content_id: "463802a3e8a61b69"
complexity: medium
produces: playbook-step
est_tokens: 4000
tags: [cohort-based-mini-course-launch, product, solo, course, monetization]
---
# Cohort Based Mini Course Launch

## Summary

**One-sentence:** Cohort sizing + calendar + Maven/Podia/Circle ops + course-as-lead-magnet for a $99-$499 × 20-seat indie monetization sprint.

**One-paragraph:** Indie operators with an audience but no productised offer can run a $99-$499 mini-course in 6 weeks to test the audience-to-customer conversion before building software. This methodology pins: cohort size (≤20 seats), 4-6 live sessions, $99-$499 price band, lead-magnet teaser, Maven/Podia/Circle ops, post-cohort upsell hook. Output: a single 6-week launch playbook with named milestones (waitlist open, payment open, kickoff, sessions, graduation, upsell).

**Ефективно для:**

- Indie operator with ≥1k engaged audience members and no paid offer yet.
- Newsletter writer testing if subscribers will pay.
- Consultant productising a recurring 1:1 topic.
- Tool maker capturing 'how to use X' demand via paid teaching.

## Applies If (ALL must hold)

- Operator has an audience ≥500 (newsletter / community / followers).
- Operator can teach the topic without external curriculum work.
- 6 weeks of evening time are available for content + delivery.
- Payment platform (Stripe / Maven / Podia) is set up.

## Skip If (ANY kills it)

- Audience <500 — cohort fill rate will be too low.
- Topic requires ≥10 sessions to teach — too large for a mini-course.
- Operator cannot commit to live sessions — switch to async product.
- Audience has previously rejected a course offer in the last 90 days.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Audience platform metrics | csv / dashboard | newsletter / community |
| Topic outline (4-6 sessions) | md | operator notes |
| Payment platform account | Stripe / Maven / Podia | vendor |
| Calendar block for live sessions | weekly 1.5h slot | calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent operating context |
| `solo/marketing/content-marketer` | lead-magnet copy + sales sequence |
| `solo/product/distribution-first-ideation` | audience-first validation |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-cohort-based-mini-course-launch` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cohort-based-mini-course-launch.md` | Markdown skeleton for the playbook-step artefact, matching content/02-output-contract.xml |
| `templates/cohort-based-mini-course-launch.schema.json` | JSON Schema seed + filled fixture for the playbook-step artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cohort-based-mini-course-launch.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[demo-hypothesis-template]]`
- `[[distribution-first-ideation]]`
- `[[beta-cohort-communication]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
