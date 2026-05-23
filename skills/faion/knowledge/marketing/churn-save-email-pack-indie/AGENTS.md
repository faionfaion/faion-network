# Churn Save Email Pack Indie

## Summary

**One-sentence:** Generates a 5-email churn-save pack — apology, pause, downgrade, 50% rescue, exit-interview — opinionated for indie $20/mo subscriptions where every save matters.

**One-paragraph:** Generates a 5-email churn-save pack — apology, pause, downgrade, 50% rescue, exit-interview — opinionated for indie $20/mo subscriptions where every save matters.

**Ефективно для:**

- Indie hacker running a $10-$30/mo subscription with manual save attempts.
- Newsletter → paid funnel where churn is the main growth leak.
- Pre-cancellation moment where one targeted email saves the customer.

## Applies If (ALL must hold)

- Product is a subscription with ≥30 active paying customers.
- Cancellation flow exists where save emails can fire.
- Email infrastructure can send per-trigger automations.
- Brand voice is documented.

## Skip If (ANY kills it)

- Self-serve checkout with no cancellation flow — instrument first.
- Enterprise contract — save plays are sales calls, not emails.
- Free tool with no paid tier.
- Already running a working churn-save sequence — replace, not duplicate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Active subscriber count | int | billing system |
| Cancellation events | json | last 90d cancellations |
| Brand voice doc | path | brand-voice-consistency-system output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| brand-voice-consistency-system | Voice doc gates each email's tone. |
| audience-to-paid-conversion-loop | Funnel context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-five-email-sequence, r2-pause-before-discount, r3-named-owner, r4-exit-interview-mandatory, r5-version-on-change | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Churn Save Email Pack Indie artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: discount-first, no-exit-interview, voice-off-tone | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-churn-save-email-pack-indie` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-churn-save-email-pack-indie` | sonnet | Bounded structural check against the output contract. |
| `review-churn-save-email-pack-indie` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/churn-save-email-pack-indie.json` | JSON skeleton matching the output contract. |
| `templates/churn-save-email-pack-indie.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-churn-save-email-pack-indie.py` | Validate Churn Save Email Pack Indie output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[brand-voice-consistency-system]]
- [[audience-to-paid-conversion-loop]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
