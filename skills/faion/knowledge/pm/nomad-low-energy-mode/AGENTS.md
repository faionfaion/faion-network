# Nomad Low-Energy Mode

## Summary

**One-sentence:** Pre-defined low-energy operating mode for nomad founders: tasks allowed, comms allowed, blockers escalation rules — keeps the business alive during travel / illness / family.

**One-paragraph:** Pins a pre-declared 'low-energy mode' (≤2 hrs/day capacity) for the nomad founder: which tasks proceed, which pause, which comms get auto-replies, which trigger escalation. Output is a versioned spec activated by a single switch, deactivated on return. Avoids ad-hoc decision-making while travelling.

**Ефективно для:**

- Nomad founder facing travel days, sick days, family weeks, time-zone shifts. One switch from 'normal' to 'low-energy' that the business survives without daily founder decisions.

## Applies If (ALL must hold)

- Founder travels OR operates across timezones ≥6 weeks/year
- ≥1 paying customer or active contractor depends on founder responsiveness
- Founder already has a 'normal mode' operating rhythm (standup, 1:1s, reviews)

## Skip If (ANY kills it)

- Salaried single-employer setup — no founder operating rhythm
- Pre-revenue with no customers / contractors to manage
- Founder fully delegated; ops continue without low-energy switch

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Normal-mode rhythm doc (standup / 1:1 / reviews) | doc | ops doc |
| Auto-reply policy (email + Slack) | doc | comms |
| Escalation contact (co-founder / VA / lawyer if applicable) | table | people doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/client-visibility-vs-velocity-tradeoff` | Peer methodology — low-energy mode adjusts client cadence per tier. |
| `solo/pm/async-standup-methodology` | Peer methodology — async standup persists in low-energy mode. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-nomad-low-energy-mode` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-nomad-low-energy-mode` | haiku | Schema check + threshold checks; deterministic. |
| `review-nomad-low-energy-mode` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nomad-low-energy-mode.json` | JSON skeleton conforming to the output contract schema. |
| `templates/nomad-low-energy-mode.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nomad-low-energy-mode.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[client-visibility-vs-velocity-tradeoff]]
- [[async-standup-methodology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
