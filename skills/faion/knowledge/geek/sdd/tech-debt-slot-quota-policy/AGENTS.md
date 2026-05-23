---
slug: tech-debt-slot-quota-policy
tier: geek
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an owner-signed quota policy that reserves a percent of each sprint's slot budget for tech debt, blocking sprints that violate the quota.
content_id: "6d5d8cde4f00bcc2"
complexity: medium
produces: config
est_tokens: 3400
tags: ["sdd", "tech-debt", "quota", "policy", "sprint"]
---
# Tech Debt Slot Quota Policy

## Summary

**One-sentence:** Produces an owner-signed quota policy that reserves a percent of each sprint's slot budget for tech debt, blocking sprints that violate the quota.

**One-paragraph:** Tech Debt Slot Quota Policy produces a config that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- 20%/sprint reserved для tech debt — quota enforced.
- Block sprints, де debt block empty.
- Visible tradeoff: feature тиск проти debt quota.
- Quarterly review: чи quota correct?
- Onboarding: junior бачить, що debt не optional.

## Applies If (ALL must hold)

- Team has a working tech-debt register.
- Sprint capacity model exists (slots, not hours).
- Tech lead owns debt quota number.

## Skip If (ANY kills it)

- No tech-debt register exists — establish one first.
- Single-developer project — quota is personal discipline.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tech-debt register | Markdown / JSON | tech lead |
| Capacity model | YAML | PM |
| Debt quota number | YAML | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[sprint-capacity-from-complexity-tags]] | quota expressed in slots from this model |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-tech-debt-slot-quota-policy` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/debt-quota.yml` | YAML debt-quota policy with owner + quarterly review log |
| `templates/debt-quota.schema.json` | JSON Schema for the quota policy |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-slot-quota-policy.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[sprint-capacity-from-complexity-tags]]
- [[pm-tech-lead-grooming-agenda]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
