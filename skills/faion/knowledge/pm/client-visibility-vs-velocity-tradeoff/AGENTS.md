# Client Visibility vs Velocity Tradeoff

## Summary

**One-sentence:** Decision framework for solo / agency PMs trading client status updates against engineering velocity: how much, how often, what shape.

**One-paragraph:** Pins the visibility-vs-velocity tradeoff: each client update unit (Slack message / weekly email / standup invite) carries a velocity cost. Output is a versioned spec sizing the right cadence by client risk profile, contract value, and current sprint phase.

**Ефективно для:**

- Solo dev or agency PM on a $5K-50K project who keeps getting pinged 'how's it going?' on Slack. Picks a fixed cadence + format per client tier and reclaims 4-8 hrs/week.

## Applies If (ALL must hold)

- ≥1 active paying client expecting status updates
- Velocity is measured (sprint, kanban, or hours)
- Current visibility load >2 ad-hoc touches/week per client

## Skip If (ANY kills it)

- Salaried single-employer work (no client tier model)
- Internal-only project — no external client
- Client is in crisis-recovery mode — visibility budget is unlimited

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Active client roster with contract value + risk tier | table | CRM |
| Last 4 weeks of visibility touchpoints (messages, calls, emails) | log | calendar + Slack export |
| Velocity measurement of choice (points, hours, milestone count) | metric | PM tool |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/freelancer-personal-crm-minimal` | Peer methodology — client tier comes from the CRM. |
| `solo/pm/async-standup-methodology` | Peer methodology — internal cadence that this trades against client cadence. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-client-visibility-vs-velocity-tradeoff` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-client-visibility-vs-velocity-tradeoff` | haiku | Schema check + threshold checks; deterministic. |
| `review-client-visibility-vs-velocity-tradeoff` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-visibility-vs-velocity-tradeoff.json` | JSON skeleton conforming to the output contract schema. |
| `templates/client-visibility-vs-velocity-tradeoff.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-visibility-vs-velocity-tradeoff.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[freelancer-personal-crm-minimal]]
- [[async-standup-methodology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
