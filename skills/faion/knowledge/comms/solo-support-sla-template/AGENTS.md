# Solo Support SLA Template

## Summary

**One-sentence:** Generates a tiered solo-SaaS support SLA (Community 72h / Paid 24h / Enterprise 4h) with canned-reply templates and an after-hours boundary policy.

**One-paragraph:** Enterprise support tooling assumes a team; solo SaaS founders inherit either chaos ('zero SLA') or burnout ('I reply <1h always'). This methodology emits three default tiers — Community (72h business hours), Paid (24h business hours), Enterprise (4h business hours + Slack) — with canned-reply skeletons, a tier-routing rule keyed to customer status, and an explicit after-hours boundary. Output: a 1-page SLA page, 4 canned-reply templates, and Help-Scout/Intercom routing rules.

**Ефективно для:**

- Solo SaaS founder with ≥20 active users drowning in inbox.
- Indie hacker scaling from 0 to first paying tier.
- Founder protecting evenings/weekends without losing trust.
- Setting expectations on a Pricing page's SLA row.

## Applies If (ALL must hold)

- Operator runs solo SaaS or solo-led service with ≥20 active users.
- Support volume ≥5 messages/week (below that SLA is theatre).
- Operator has ≥1 inbound channel (email, in-app chat, Discord).
- Operator has a publicly visible 'support' page or footer link.

## Skip If (ANY kills it)

- Operator runs a 2-3 person team — use a real helpdesk SLA + rotation.
- Product is dev-tool with technical CSAT (e.g. Sentry) — community Slack rules dominate.
- Support volume &lt;5/week — handle ad-hoc.
- Operator already burned out — fix burnout first, SLA later.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Channel inventory | all inbound channels + current response times | operator |
| Tier definitions | free vs paid vs enterprise plan IDs | billing |
| Working hours | operator timezone + on/off-days | operator |
| Sample transcripts | 1 week anonymised for canned-reply tuning | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo-testimonial-extraction-script]] | downstream — happy ticket → testimonial |
| [[stakeholder-communication]] | mode-selection for escalations |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tier-classification` | haiku | Lookup against customer table. |
| `canned-reply-draft` | sonnet | Template fill + tone matching. |
| `escalation-decision` | sonnet | Bounded judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sla-policy.md` | Public SLA page skeleton |
| `templates/canned-replies.yaml` | 4 canned reply skeletons |
| `templates/sla-policy.json` | Machine-readable policy |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-support-sla-template.py` | Validate solo-support-sla-template artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[solo-testimonial-extraction-script]]
- [[stakeholder-communication]]
- [[feedback]]

## Decision tree

See `content/06-decision-tree.xml`. Gates on support volume and team size. Below 5/week or above 1 person the methodology refuses to apply; otherwise 3-tier SLA emitted.
