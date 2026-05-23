---
slug: beta-charter-template
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Pre-launch beta charter pinning cohort size, success metric, duration, exit criteria, and graduation conditions \u2014 signed by founder + first beta user."
content_id: "18b4dc8ae6e619b0"
complexity: medium
produces: spec
est_tokens: 4700
tags: [beta-charter-template, product, solo, beta, launch]
---
# Beta Charter Template

## Summary

**One-sentence:** Pre-launch beta charter pinning cohort size, success metric, duration, exit criteria, and graduation conditions — signed by founder + first beta user.

**One-paragraph:** Beta programs without a charter drift into never-ending free tiers or burn out the founder with support. This methodology produces a one-page charter that pins: cohort size (≤20 for solo SaaS), beta duration (28-56 days), single success metric + threshold, NPS sample, exit/graduation conditions, weekly broadcast cadence, founder reply SLA. The charter is signed by the founder + the first beta user before recruiting opens; later beta users see the signed charter on join.

**Ефективно для:**

- Solo SaaS founder pre-launch with 5-20 prospective beta users.
- Course creator running a closed cohort before public launch.
- Indie maker rolling out a new tool to existing newsletter subscribers.
- Tech lead launching an internal beta of a new platform feature.

## Applies If (ALL must hold)

- Product is pre-public-launch (no paid users yet OR explicit beta tag).
- Founder can dedicate ≥1h/week to beta support during the program.
- ≥5 prospective beta users are identified and engaged.
- A single success metric is articulatable.

## Skip If (ANY kills it)

- Product already has paying customers and 'beta' is a marketing label.
- Cohort would be >50 — beta becomes a launch; use a different methodology.
- Founder cannot commit to weekly broadcast — beta will go silent.
- Success metric is unclear or contested — define metric first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Beta candidate list | csv with name + handle + segment | prospect / waitlist |
| Product brief | md, 1 page | founder |
| Success metric draft | 1 sentence | founder |
| Founder calendar slot | weekly 1h block | calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent operating context |
| `solo/product/beta-cohort-communication` | weekly broadcast templates |
| `solo/product/discovery-research-handoff-template` | evidence shape for the founding hypothesis |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-beta-charter-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/beta-charter-template.md` | Markdown skeleton for the spec artefact, matching content/02-output-contract.xml |
| `templates/beta-charter-template.schema.json` | JSON Schema seed + filled fixture for the spec artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-beta-charter-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[beta-cohort-communication]]`
- `[[cohort-based-mini-course-launch]]`
- `[[mvp-instrumentation-checklist]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
