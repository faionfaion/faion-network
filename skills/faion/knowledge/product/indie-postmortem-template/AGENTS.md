# Indie Postmortem Template

## Summary

**One-sentence:** Run a blameless solo-founder postmortem after a launch / outage / project-end: timeline, contributing factors, blast radius, lessons, and ≤3 follow-up actions — capped at 30 min.

**One-paragraph:** Adapts the SRE-style postmortem for a one-person team: blameless framing is automatic but rigor is not. The template forces a timeline reconstruction, factor classification, and ≤3 actionable follow-ups rather than a generic 'do better next time'. The 30-min cap keeps it sustainable so it actually happens.

**Ефективно для:**

- Solo founder after a failed launch / outage / abandoned project — wants the lesson without spending half a day or sinking into self-blame.

## Applies If (ALL must hold)

- Incident, failed launch, or abandoned project just ended.
- Founder has ≥30 min to spend on the postmortem.
- Follow-up actions can actually be picked up within 2 weeks.

## Skip If (ANY kills it)

- Trivial bug fix — no postmortem needed.
- Founder in active firefight — postmortem only after stabilisation.
- Repeating the same postmortem template that produced no change — try a different format.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event under review (link) | url | Incident log / launch doc |
| Timeline raw notes | markdown | Logs / chat |
| Calendar slot (30 min) | calendar event | Calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager/product-launch` | Launch context that may have triggered the postmortem. |
| `solo/product/product-operations/feedback-management` | Inputs that may surface during reconstruction. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-indie-postmortem-template` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-indie-postmortem-template` | haiku | Schema check + threshold checks; deterministic. |
| `review-indie-postmortem-template` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/indie-postmortem-template.json` | JSON skeleton conforming to the output contract schema. |
| `templates/indie-postmortem-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-indie-postmortem-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[product-launch]]
- [[feedback-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
