# Subscription Lifecycle Edge Cases

## Summary

**One-sentence:** Wires the 8 subscription edge cases (trial-to-paid, upgrade, downgrade, proration, failed renewal, cancel-then-resubscribe, EU VAT, refunds) into a single tested runbook with Stripe webhook coverage and dunning policy.

**One-paragraph:** Wires the 8 subscription edge cases (trial-to-paid, upgrade, downgrade, proration, failed renewal, cancel-then-resubscribe, EU VAT, refunds) into a single tested runbook with Stripe webhook coverage and dunning policy. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Subscription Lifecycle Edge Cases on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Solo SaaS with active subscription billing.
- Stripe (or equivalent) wired for webhooks.
- EU customers in revenue mix → VAT applies.
- Owner has ≥1 paying customer in trial-to-paid transition.

## Skip If (ANY kills it)

- Pre-billing prototype.
- One-time payment product — no lifecycle.
- Enterprise invoicing only — no self-service flow.
- Stripe Tax not configured — fix that first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stripe webhooks live | endpoint URL | Stripe dashboard |
| Subscription product + price config | JSON | Stripe |
| Email transactional pipeline | Postmark / Resend | Self |
| Customer DB + sub-id mapping | schema | Backend |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/solo-saas-legal-docs-pack` | Legal preconditions for billing. |
| `pro/dev/api-developer/webhook-handling` | Webhook robustness. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-subscription-lifecycle-edge-cases` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-subscription-lifecycle-edge-cases` | haiku | Schema check + threshold checks; deterministic. |
| `review-subscription-lifecycle-edge-cases` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/subscription-lifecycle-edge-cases.json` | JSON skeleton conforming to the output contract schema. |
| `templates/subscription-lifecycle-edge-cases.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-subscription-lifecycle-edge-cases.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[solo-saas-legal-docs-pack]]
- [[product-launch]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
