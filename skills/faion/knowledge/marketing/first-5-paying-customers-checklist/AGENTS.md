# First 5 Paying Customers Checklist

## Summary

**One-sentence:** Operating checklist artefact that bridges shipped-MVP to first 5 paid charges — the single biggest survival cliff for solo SaaS — with offer, channel, outreach quota, and pricing baseline.

**One-paragraph:** First 5 Paying Customers Checklist produces a checklist artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated checklist ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder with a shipped MVP and 0 paid customers who needs a focused 6-week artefact covering offer, outreach quota, channel, and pricing pilot to cross the first-revenue cliff.

## Applies If (ALL must hold)

- MVP is shipped and demoable (not vaporware)
- Zero paying customers today
- Founder has ≥6 weeks of focused runway available

## Skip If (ANY kills it)

- Already have ≥5 paying customers — use audience-to-paid-conversion-loop
- Pre-MVP / pre-product — use product-validation methodologies first
- Open-source side project with no paid intent

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Working MVP URL | URL | deployment |
| Ideal customer profile (ICP) | doc | product brief |
| Price point hypothesis | USD/month | pricing log |
| Outreach channel list (≥2) | list | marketing inventory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `audience-to-paid-conversion-loop` | Once 5 paid customers exist this is the next methodology. |
| `growth-cold-outreach` | Cold outreach is one of the channels used here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-zero-to-five-paid, r2-outreach-quota-daily, r3-pricing-not-free, r4-one-icp-only, r5-weekly-review-with-numbers, r6-named-owner-solo-counts | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-first-5-paying-customers-checklist` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-first-5-paying-customers-checklist` | haiku | Schema check + threshold checks; deterministic. |
| `review-first-5-paying-customers-checklist` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/first-5-paying-customers-checklist.json` | JSON skeleton conforming to the output contract schema. |
| `templates/first-5-paying-customers-checklist.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-first-5-paying-customers-checklist.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[audience-to-paid-conversion-loop]]
- [[growth-cold-outreach]]
- [[ops-pricing-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
