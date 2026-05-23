# Agency Decline Templates

## Summary

**One-sentence:** Generates a graceful 'no' template pack — bad-fit, capacity, price, scope, timeline — so an indie consultant declines work in minutes while protecting positioning and seeding referrals.

**One-paragraph:** Generates a graceful 'no' template pack — bad-fit, capacity, price, scope, timeline — so an indie consultant declines work in minutes while protecting positioning and seeding referrals.

**Ефективно для:**

- Solo consultant getting bad-fit leads weekly.
- Pre-launch positioning where decline emails shape the brand.
- Capacity-throttled period where every 'no' must seed a referral.

## Applies If (ALL must hold)

- Operator receives ≥2 bad-fit leads / week.
- Brand voice is documented.
- Operator wants to maintain referral network with declined leads.
- Decline volume justifies templates (>5/month).

## Skip If (ANY kills it)

- First decline ever — write freeform, extract a template after.
- One-off bespoke ask — template constrains the wrong axes.
- Local cultural norms not encoded — start from local norms.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Lead inventory | list | last 90d declined leads |
| Brand voice doc | path | brand-voice-consistency-system output |
| Referral partner list | list | named partners for hand-offs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| brand-voice-consistency-system | Voice doc gates each template. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-five-decline-templates, r2-protect-positioning, r3-seed-referral, r4-named-owner, r5-version-bumped | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Agency Decline Templates artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: just-not-fit, dead-end-decline, freeform-every-time | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-agency-decline-templates` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-agency-decline-templates` | sonnet | Bounded structural check against the output contract. |
| `review-agency-decline-templates` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agency-decline-templates.json` | JSON skeleton matching the output contract. |
| `templates/agency-decline-templates.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-decline-templates.py` | Validate Agency Decline Templates output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[brand-voice-consistency-system]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
