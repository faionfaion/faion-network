---
slug: stack-mandate-tradeoff-frame
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Trade-off framing methodology for an outsource senior dev writing an ADR inside a client-mandated stack — names the constraint as policy, frames options within the stack, and uses costed mitigations instead of "we recommend a different stack" language.
content_id: "c068944ac0e39f29"
tags: [software-architect, adr, stack-mandate, outsource, p4-outsource, tradeoff, client-architecture]
---
# Stack Mandate Trade-off Frame

## Summary

**One-sentence:** An ADR-writing methodology for senior outsource devs operating inside a client-mandated stack: frame trade-offs as options *within* the mandate (not against it), cite the mandate as policy, and propose costed mitigations rather than stack replacement.

**One-paragraph:** Generic quality-attribute methodologies (e.g., ATAM, QAW) assume the architect has freedom to pick the stack. Outsource senior devs almost never do — the client has standardised on AWS-EKS-Java-Postgres, or Azure-Functions-C#-SQL, and that decision is non-negotiable. Writing an ADR that says "consider switching to X" gets the dev disqualified from future engagements. This methodology codifies the different reasoning style needed: cite the mandate as an explicit constraint at the top, enumerate options whose first axis is "within mandate", show trade-offs in the language the client already uses (e.g., "additional EKS node groups" not "consider Nomad"), and where a trade-off is genuinely painful, propose costed mitigations the client can buy rather than implying their stack is wrong. The ADR is judged by a client architect, not the team — its job is to persuade inside the client's worldview, not from outside it.

## Applies If (ALL must hold)

- Client has documented or verbally established a mandated stack (vendor, language, infra) the engagement MUST use.
- The dev is producing an ADR or decision memo that goes to a client architect or CTO.
- A genuine trade-off exists (latency vs cost, complexity vs delivery date, etc.) — not a pure implementation memo.
- The dev has at least 3 viable options *within* the mandated stack.

## Skip If (ANY kills it)

- Greenfield internal product where the dev picks the stack — use `quality-attributes-analysis` instead.
- Client has invited an explicit stack-review engagement — different deliverable, different framing.
- Decision is reversible at low cost (e.g., a config flag) — over-engineered for the value.
- Only one option exists within the mandate — there is no trade-off to frame; write an implementation note.

## Prerequisites

- Written or quotable statement of the client's stack mandate.
- List of 3+ candidate options inside the mandate.
- Quality attribute the trade-off acts on (latency, cost, security, etc.), with a target value if known.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/architecture-proposal-document-template` | ADR baseline structure this specialises. |
| `geek/sdd/adr-consequence-evidence-binding` | ADR consequence-evidence linking conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: mandate-as-constraint, options-within-mandate axis, client-lexicon enforcement, costed-mitigation pattern, no-replacement-suggestion. | ~900 |

## Related

- parent skill: `pro/dev/software-architect/`
- peer: `architecture-proposal-document-template`, `technology-evaluation-rubric`, `cost-modeling-at-design-time`
- external: ATAM (Architecture Tradeoff Analysis Method) — generic baseline being specialised here for mandated stacks
