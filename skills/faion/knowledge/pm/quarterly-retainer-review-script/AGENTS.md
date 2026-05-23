# Quarterly Retainer Review Script

## Summary

**One-sentence:** 45-min scripted QBR converting utilization data into renewal commitment: 10-min data → 15-min outcomes → 10-min blockers → 10-min renewal; named decision exit; 24h follow-up email.

**One-paragraph:** A 45-minute scripted quarterly review call for retainer clients (1-10 retainers, micro-agency). Four segments: data-only 10 min (hours used/bought, SLA %, deliverables) → outcomes 15 min → blockers 10 min → renewal 10 min. Call ends with one of four explicit decisions named aloud: continue / scale up / scope down / terminate (or deferred with a named date ≤14 days). Scope deltas written live into decision-record JSON. Follow-up email within 24h. Numbers anchor the conversation; advocacy/discount-anchoring deferred to segment 4.

**Ефективно для:**

- Micro-agency founder (1-10 retainer clients) with quarterly cadence
- Retainer ≥$2k/month — overhead justified
- Client is decision-maker for renewal (not procurement gatekeeper)
- Tracked utilization data exists (Toggl, Harvest, Clockify)

## Applies If (ALL must hold)

- You operate a retainer-based service business with ≥3 active retainer clients
- Retainer contracts have a renewal/review cadence (monthly, quarterly, or semi-annually)
- You track hours, deliverables, and SLA adherence per client
- The client is the decision-maker for renewal (not a procurement gatekeeper)

## Skip If (ANY kills it)

- One-shot project work — use a project-closure script instead
- Corporate enterprise sales-led renewal (procurement-driven, 90-day cycle)
- Pre-launch / first quarter of a new retainer — use kickoff review
- Retainer < $2k/month — overhead exceeds value
- Client delinquent on payments — collections call comes first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Utilization data | JSON / CSV | Toggl / Harvest / Clockify export |
| Previous QBR notes | Markdown | if Q2+ — track promises kept vs broken |
| Deliverables shipped | list | artefact links per deliverable |
| Next-quarter capacity forecast | YAML | team capacity planner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[project-closure]] | Closure script if decision is terminate |
| [[scope-management]] | Scope-delta language for scale_up / scope_down |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 45-minute-cap, named-decision-exit, data-over-narrative, scope-delta-written, 24h-follow-up | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `slide_deck_first_draft` | sonnet | Template fill from utilization data |
| `talking_points_draft` | sonnet | Per-segment bullets, low ambiguity |
| `decision_framework_synthesis` | opus | Cross-input judgement when data is mixed |
| `follow_up_email_draft` | haiku | Template fill: decision + scope delta + next-quarter date |

## Templates

| File | Purpose |
|------|---------|
| `templates/qbr-deck.md` | 6-slide outline: cover / status / outcomes / blockers / renewal options / next quarter |
| `templates/qbr-talking-points.md` | Verbatim opening, transition, and closing lines for each segment |
| `templates/decision-record.json` | Renewal decision schema (continue / scale_up / scope_down / terminate / deferred_with_date) |
| `templates/follow-up-email.md` | 1-page recap email — sent within 24h of call |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/build-qbr-deck.py` | Pull utilization + SLA + deliverables → populate qbr-deck.md | 48h before QBR call |
| `scripts/validate-quarterly-retainer-review-script.py` | Verify decision-record.json shape + call_duration_minutes cap + follow_up lag | Post-call; pre-renewal |

## Related

- parent skill: `pro/pm/project-manager/`
- [[project-closure]]
- [[scope-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
