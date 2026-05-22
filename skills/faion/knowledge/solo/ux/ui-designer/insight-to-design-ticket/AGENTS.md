---
slug: insight-to-design-ticket
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A bridge protocol that converts research insights (interview tags, friction map findings) into ranked, design-ready backlog tickets.
content_id: "10eb2145dba12f56"
tags: [ux,research,backlog,insight,ticket,design,prioritization]
---
# Insight to Design Ticket

## Summary

**One-sentence:** A bridge protocol that converts research insights (interview tags, friction map findings) into ranked, design-ready backlog tickets.

**One-paragraph:** Research insights frequently die between the synthesis report and the backlog because no one translates "users feel anxious during checkout" into a sized, prioritized ticket designers can pick up tomorrow. This methodology defines the format of a "design ticket" output: one insight per ticket, evidence quote, affected user moment, severity, suggested-not-mandated direction, and a one-line acceptance criterion. Mechanism: a closed insight-to-ticket transformation with required fields, an ICE-shaped prioritization vote with the PM/researcher pair, and a "loss horizon" that retires un-pulled tickets after 90 days so the backlog doesn't become a graveyard. Primary output: a per-insight ticket in the design backlog with a documented chain back to the research evidence.

## Applies If (ALL must hold)

- research artifacts (interview transcripts, friction maps, usability findings) exist for a feature
- operator can author tickets in the team's tracker (Linear, Jira, GitHub, Notion)
- design backlog exists as a distinct queue OR will be created
- ≥ 1 designer has bandwidth to pull tickets from the backlog
- PM or product owner participates in prioritization

## Skip If (ANY kills it)

- research is ongoing and synthesis hasn't been done — wait for completion
- single-designer single-PM team that already direct-edits — overhead exceeds value
- pure visual-polish project with no behavioral hypotheses
- crisis hotfix flow where insights skip directly to design (no backlog handoff needed)
- regulated-design workflow (FDA, medical) — needs heavier traceability than this provides

## Prerequisites (must be true before starting)

- tagged insights from research synthesis (each insight has ≥ 3 evidence quotes)
- list of affected user moments / personas
- ticket-tracker permissions for the converter
- agreed-upon ICE rubric (Impact / Confidence / Ease per insight)
- 90-day loss horizon policy approved by team

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/user-interviews` | Source of tagged insights |
| `pro/ux/ux-researcher/journey-mapping` | Affected user-moment context |
| `pro/marketing/growth-marketer/growth-experiment-design` | Optional: insights with hypothesis hooks may also become experiments |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: one insight per ticket, evidence required, suggested-not-mandated direction, ICE before queue, 90-day loss horizon | ~1000 |
| `content/02-output-contract.xml` | essential | Ticket schema, required fields, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (solution-as-insight, evidence loss, graveyard backlog, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `insight_extractor` | sonnet | Parse synthesis report into discrete insights |
| `ticket_draft_per_insight` | sonnet | Convert each insight into ticket fields |
| `ice_scoring_synth` | sonnet | Score Impact / Confidence / Ease with documented rationale |
| `loss_horizon_sweeper` | haiku | Tag tickets older than 90 days as "retire_candidate" |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-ticket-skeleton.md` | One-insight-per-ticket template |
| `templates/ice-rubric.md` | Impact / Confidence / Ease scale per insight type |
| `templates/loss-horizon-policy.md` | Retirement criteria + appeal process |
| `templates/evidence-link-format.md` | How to reference transcript IDs + timestamps |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/insight-to-ticket.py` | Generate tickets from tagged-insight JSON | After research synthesis |
| `scripts/backlog-graveyard-sweep.py` | Identify tickets past loss horizon | Quarterly |

## Related

- parent skill: `solo/ux/ui-designer/`
- peer methodology: `solo/research/researcher/user-interviews`, `pro/ux/ux-researcher/journey-mapping`
- external: [Erika Hall, Just Enough Research](https://abookapart.com/products/just-enough-research) · [Tomer Sharon, validating insights](https://www.tomersharon.com/)
