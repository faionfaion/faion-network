# Live Ticket Drafting (Shared-Screen Pattern)

## Summary

**One-sentence:** Pattern: BA drafts tickets live on a shared screen during elicitation, contributor signs off in-session, eliminating async clarification rounds.

**One-paragraph:** Live Ticket Drafting (Shared-Screen Pattern) pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Outsource engagements with timezone-overlap windows (less than 4 hours overlap).
- Complex domains where written requirements drift from intent quickly.
- First sprints of a new engagement establishing common ticket shape.
- High-stakes tickets (compliance, money) where late clarification is expensive.

## Applies If (ALL must hold)

- BA writes Jira / Linear / ADO tickets from elicitation sessions.
- Sessions average more than 1 clarification round per ticket after the fact.
- Contributors are available for synchronous review.
- Screen-share tooling exists and is permitted by client security policy.

## Skip If (ANY kills it)

- Contributors are unavailable for synchronous review (extreme timezone offset, async-only culture).
- Client security policy prohibits shared-screen viewing of internal systems.
- Engagement is informal — async ticket drafting is fine.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Elicitation session agenda | markdown | BA prep |
| Ticket template | yaml / markdown | Team ticket convention |
| Screen-share permissions | policy doc | Client security |
| Contributor calendar holds | calendar invite | Session organiser |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-live-ticket-drafting-shared-screen-pattern` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/live-ticket-drafting-shared-screen-pattern.md` | Markdown playbook-step template with required sections |
| `templates/live-ticket-drafting-shared-screen-pattern.schema.json` | JSON Schema for the structured playbook-step record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-live-ticket-drafting-shared-screen-pattern.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
