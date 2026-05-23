# Customer Support Ops

## Summary

**One-sentence:** Generates a self-serve-first support spec: FAQ + knowledge base before async channel, SLA tiered by plan (Free 24-48h, Paid 4-24h, Enterprise 1-4h), and weekly ticket-pattern review feeding product roadmap.

**One-paragraph:** Customer Support Ops produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder with ≥20 monthly tickets across mixed-plan customers who needs a self-serve-first support spec with tiered SLAs and weekly pattern review — before async channels eat all founder hours.

## Applies If (ALL must hold)

- ≥20 support tickets / month across all channels
- Pricing has ≥2 tiers (free + paid, or trial + paid)
- Founder commits to weekly ticket-pattern review

## Skip If (ANY kills it)

- <20 tickets / month — ad-hoc inbox is enough
- Single-tier free product — different shape
- Enterprise-only with named CSM per account — different methodology

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Ticket history (last 90 days) with plan + topic + time-to-close | CSV | support tool |
| Pricing tiers + entitlements | doc | billing |
| Existing FAQ / KB inventory | URLs | docs site |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `ops-automation-workflow` | Ticket patterns become automation candidates. |
| `objection-bank` | Top objection patterns surface as support tickets. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-self-serve-first, r2-sla-tiered-by-plan, r3-canned-reply-coverage-60-pct, r4-weekly-pattern-review, r5-named-owner, r6-no-pii-in-canned-replies | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ops-customer-support` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-ops-customer-support` | haiku | Schema check + threshold checks; deterministic. |
| `review-ops-customer-support` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-customer-support.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ops-customer-support.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-customer-support.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[ops-automation-workflow]]
- [[objection-bank]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
