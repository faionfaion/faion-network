# Feature Launch Checklist

## Summary

**One-sentence:** Produces a 20-item GTM checklist artefact for a new product feature: messaging, assets, channels, support enablement, success metrics — gated by a named owner and a launch date.

**One-paragraph:** Feature Launch Checklist produces a checklist artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated checklist ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo SaaS founder shipping a feature in ≤4 weeks who needs one canonical artefact that prevents the eight classic missed-asset / missed-channel launch bugs.

## Applies If (ALL must hold)

- New product feature is shipping in ≤4 weeks
- Feature has at least one user-visible touchpoint (UI, API, billing change)
- There is a named launch owner

## Skip If (ANY kills it)

- Internal-only refactor with no user-visible surface
- Bug-fix release — use changelog, not launch checklist
- Launch already shipped — use post-launch retro instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | doc | product backlog |
| Target launch date | ISO date | roadmap |
| Available distribution channels | list | marketing inventory |
| Pricing/packaging impact | spec | billing module |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `first-5-paying-customers-checklist` | Adjacent — converts launch reach into revenue. |
| `growth-product-hunt-launch` | If PH is in the channel mix, plug in the PH playbook. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-20-items-mandatory, r2-named-launch-owner, r3-launch-date-fixed, r4-channel-min-3, r5-success-metric-pre-declared, r6-support-enabled | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-feature-launch-checklist` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-feature-launch-checklist` | haiku | Schema check + threshold checks; deterministic. |
| `review-feature-launch-checklist` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature-launch-checklist.json` | JSON skeleton conforming to the output contract schema. |
| `templates/feature-launch-checklist.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-launch-checklist.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[first-5-paying-customers-checklist]]
- [[growth-product-hunt-launch]]
- [[growth-hacker-news-launch]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
