# Product Hunt Launch System

## Summary

**One-sentence:** Generates a four-phase Product Hunt launch spec: 4-8 week pre-list build, niche hunter selection (≥1000 followers), launch timing (12:01 AM PT Tue-Thu), 1-hour response SLA — engineered for top-5 placement.

**One-paragraph:** Product Hunt Launch System produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder targeting consumer / prosumer / SaaS audience on Product Hunt who needs a 4-phase launch spec with email list, hunter, launch-day asset matrix, and engagement SLA before the launch window opens.

## Applies If (ALL must hold)

- Product fits PH audience (SaaS, consumer, prosumer, dev-tool)
- Founder has 4-8 weeks runway pre-launch
- Has not been launched on PH previously (or last launch >6 months ago)

## Skip If (ANY kills it)

- Audience is enterprise IT — PH is wrong channel
- Product launches in <4 weeks — too short for pre-list
- B2B niche with <100 addressable users — payoff too small

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Email list with ≥500 launch-day subscribers (target) | list | ESP |
| Hunter contact (≥1000 PH followers, ideally niche-aligned) | person | PH discover |
| Launch assets: gallery, gif, tagline, FAQ | files | marketing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `growth-hacker-news-launch` | Sibling launch channel. |
| `feature-launch-checklist` | Parent — PH is one channel inside the wider launch. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-pre-list-500-min, r2-niche-hunter-1000-followers, r3-launch-12-01-am-pt-tue-thu, r4-respond-within-1-hour, r5-asset-matrix-complete, r6-no-bot-upvotes | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-growth-product-hunt-launch` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-growth-product-hunt-launch` | haiku | Schema check + threshold checks; deterministic. |
| `review-growth-product-hunt-launch` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-product-hunt-launch.json` | JSON skeleton conforming to the output contract schema. |
| `templates/growth-product-hunt-launch.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-product-hunt-launch.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[growth-hacker-news-launch]]
- [[feature-launch-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
