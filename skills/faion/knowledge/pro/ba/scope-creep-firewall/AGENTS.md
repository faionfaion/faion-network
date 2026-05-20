---
slug: scope-creep-firewall
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Scope-Creep Firewall: an explicit per-engagement change-request methodology tuned for solo operators that converts incoming asks into typed change orders instead of absorbed work.
content_id: "f3a78df578243016"
tags: [scope-creep-firewall, ba, pro]
---
# Scope-Creep Firewall

## Summary

**One-sentence:** A per-engagement methodology that stands up an explicit "everything new lands here" intake, classifies each ask in 5 minutes, and routes it to either no-op (already in scope), change-order, or backlog — so a solo operator never absorbs a creep silently.

**One-paragraph:** Scope creep is the #1 freelancer profit leak. Existing methodologies cover request impact rubrics and email phrasings, but a solo operator needs a single named gate — the firewall — that every new ask passes through, with a fixed time budget per classification and a strict default of "this is a change order until proven otherwise". This methodology defines the firewall's three-question intake, the classification SLA (≤5 minutes per ask), the four routing outcomes (in-scope-clarified, no-op-already-delivered, change-order-required, backlog-deferred), and the weekly summary report sent to the client. Output is a per-ask firewall record and a per-engagement creep-trend that tells the operator whether this engagement is healthy, slipping, or terminal.

## Applies If (ALL must hold)

- the engagement has a written scope (SOW, proposal, statement of work)
- the operator is solo or works with ≤2 collaborators (no PMO buffer between client and delivery)
- engagement length 4 weeks or longer (shorter engagements use a lighter intake)
- tier == pro or higher

## Skip If (ANY kills it)

- the engagement is explicitly time-and-materials with no scope cap and unlimited budget — there is no scope to defend
- the operator's client uses a formal change-control process the operator is participating in — adopt that, do not parallel
- the operator is in the final 5 business days of the engagement — switch to handover mode

## Prerequisites

- the engagement SOW reference
- a single inbound channel declared as the firewall (a tag in the ticket tracker, an email rule, a Slack channel — pick one)
- the change-order rate card or template
- 5 minutes per business day reserved for firewall triage

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill |
| `pro/ba/change-request-impact-rubric` | downstream rubric for accepted change orders |
| `pro/ba/scope-creep-email-language-pack` | phrasing pack for the outbound side of routing |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: single-intake, three-question-classifier, 5min-triage-budget, change-order-default, weekly-summary-to-client, creep-trend-tracked | ~1200 |

## Related

- parent skill: `pro/ba/business-analyst`
- upstream playbook: `p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)`
- companion methodology: `pro/ba/scope-creep-email-language-pack`
