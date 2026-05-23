---
slug: anti-roadmap-template
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Quarterly 'what we will NOT ship' list \u2014 explicit deferred / declined / killed items with rationale and revisit triggers, paired with the roadmap to absorb stakeholder pressure."
content_id: "06795c229e5a4444"
complexity: medium
produces: report
est_tokens: 4700
tags: [anti-roadmap-template, product, solo, roadmap, no-list]
---
# Anti Roadmap Template

## Summary

**One-sentence:** Quarterly 'what we will NOT ship' list — explicit deferred / declined / killed items with rationale and revisit triggers, paired with the roadmap to absorb stakeholder pressure.

**One-paragraph:** Roadmap methodologies focus on what we WILL ship; the costly skill is publishing what we explicitly will NOT ship. This methodology produces a one-page anti-roadmap per quarter listing every deferred / declined / killed item with: why-not rationale (single sentence), revisit trigger (metric or event), owner, expiration date. The anti-roadmap is signed by the PM and the top sponsoring stakeholder; future asks pointing at killed items are first checked against the anti-roadmap entry, not re-litigated.

**Ефективно для:**

- Solo PM facing constant 'what about X?' from stakeholders.
- Founder who repeatedly revisits the same killed ideas.
- Product team with no documented 'no' policy.
- Indie operator running portfolio decisions under inbox pressure.

## Applies If (ALL must hold)

- Roadmap exists or is being authored this quarter.
- There are ≥3 declined / deferred items the team needs to communicate.
- PM (or operator) can require a sponsor sign-off on the no-list.
- Stakeholders are surfacing repeat 'why not X' questions.

## Skip If (ANY kills it)

- Roadmap is empty (pre-planning) — author roadmap first.
- Team has ≤2 stakeholders and informal alignment suffices.
- All declines are confidential (M&A, security) — handle out of band.
- Anti-roadmap from last quarter is still current — refresh, do not redo.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current roadmap | md / Productboard / Linear | roadmap tool |
| Last-quarter requests log | csv / spreadsheet | support + sales tickets |
| Sponsor stakeholder name + handle | string | engagement charter |
| Quarter calendar window | ISO dates | release calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent solo-PM product operating context |
| `solo/product/kill-criteria-template` | format for revisit triggers |

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
| `draft-anti-roadmap-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/anti-roadmap-template.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/anti-roadmap-template.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-anti-roadmap-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[kill-criteria-template]]`
- `[[backlog-hygiene-cron-checklist]]`
- `[[friction-to-backlog]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
