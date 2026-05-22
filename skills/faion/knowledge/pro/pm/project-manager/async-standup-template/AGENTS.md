---
slug: async-standup-template
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "2460f47ce1bb897e"
summary: Three-field written-Slack daily standup (Yesterday, Today, Blocker) for 1-3 person cross-timezone teams, with blocker-routing SLA and silence-detection rule.
tags: [async-standup, slack, remote, cross-timezone, micro-agency, outsourcing]
---

# Async Standup Template

## Summary

**One-sentence:** Three-field written-Slack daily standup (Yesterday, Today, Blocker) for 1-3 person cross-timezone teams, with blocker-routing SLA and silence-detection rule.

**One-paragraph:** Replaces the verbal scrum standup for contractor and cross-timezone setups where synchronous meetings cost a half-day per person. Mechanism: one Slack thread per day in a dedicated channel; every contributor posts a strictly-shaped 3-field message within their local working window; blockers are auto-tagged and routed to a named owner with a 12-hour response SLA; missed posts trigger a silence-detector ping. Primary output: a daily searchable thread that the PM can scan in under 5 minutes.

## Applies If (ALL must hold)

- team_size ≤ 3 active contributors per project (or single-team within larger org)
- timezone_gap_between_any_two_members ≥ 4 hours
- communication_platform ∈ {Slack, Microsoft Teams, Discord, Mattermost}
- engagement_duration ≥ 2 weeks (one-shot tasks don't need a cadence)

## Skip If (ANY kills it)

- team is fully co-located in one timezone — verbal standup is faster
- team is &gt; 6 people — needs Scrum daily or a different ceremony, not this template
- everyone is async-only with deep-work norm (no expectation of same-day reply) — replace with weekly written update
- the project is &lt; 5 working days — standup overhead exceeds value

## Prerequisites

- dedicated standup channel (e.g., #proj-foo-standup) with topic set to the template format
- named blocker-owner per team (PM or lead) with @-mention configured
- working-hours posted per contributor in profile or pinned note
- Slack/Teams workflow (Workflow Builder, Bot) optional but recommended for shape enforcement

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/communications-management` | Sets the comms-plan framing this template lives inside |
| `pro/pm/pm-agile/scrum-ceremonies-setup` | The synchronous baseline this template replaces for distributed teams |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: post shape, response SLA, blocker routing, silence detection, weekly digest | ~1000 |
| `content/02-output-contract.xml` | essential | Standup-post schema, forbidden patterns, weekly digest contract | ~600 |
| `content/03-failure-modes.xml` | essential | 6 LLM/agent failure modes when drafting or summarizing async standups | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `personal_standup_draft` | haiku | Template fill from a contributor's daily log; low cost |
| `blocker_routing` | sonnet | Judgment on which @-owner gets the blocker |
| `weekly_digest_synthesis` | sonnet | Cross-day synthesis across ≤5 days of threads |

## Templates

| File | Purpose |
|------|---------|

## Scripts

| File | Purpose |
|------|---------|

## Related

- parent skill: `pro/pm/project-manager/SKILL.md`
- peer methodologies: `pro/pm/pm-agile/scrum-ceremonies-setup`, `pro/pm/project-manager/communications-management`
- external: [GitLab async handbook — daily standup](https://about.gitlab.com/handbook/) · [Doist async-first communication guide](https://doist.com/blog/) · [Basecamp Shape Up "hill chart" updates] · [Slack Workflow Builder daily standup template]
