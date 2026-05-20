---
slug: inc-postmortem-auto-draft-no-publish
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When an incident is resolved, an LLM agent (Rootly, incident.
content_id: "0d4ad416bdac868c"
tags: [postmortem, incident-response, auto-draft, blameless, hypothesis-marking]
---
# Postmortem Auto-Draft, Never Auto-Publish

## Summary

**One-sentence:** When an incident is resolved, an LLM agent (Rootly, incident.

**One-paragraph:** When an incident is resolved, an LLM agent (Rootly, incident.io, FireHydrant pattern) drafts the postmortem from structured signals — Slack channel transcript, alert + deploy timeline, ChatOps /incident actionitem calls, linked PRs — into a fixed template (Summary / Timeline / Impact / Root Cause Hypothesis / Contributing Factors / Action Items) with tone=blameless. The draft lands as a non-published document assigned to the incident commander; humans edit, accept the root-cause framing, and publish. The agent must never auto-publish, never invent facts beyond the structured signal set, and must mark every speculative claim (hypothesis).

## Applies If (ALL must hold)

- Teams that currently skip postmortems because writing them is painful.
- Incident-management tools with an autodraft API (Rootly, incident.io, FireHydrant, PagerDuty) or a custom pipeline over Slack + alert + deploy data.
- Engineering cultures that have already adopted blameless postmortem norms.
- Regulated environments where a fast, accurate first-draft helps meet 72-hour reporting windows (EU NIS2, SOC2 incident reporting).

## Skip If (ANY kills it)

- Highly regulated incidents (legal, safety, financial) where every sentence must be authored by a human from scratch.
- Tiny teams (5 or fewer engineers) where the human writes faster than they can review an LLM draft.
- Teams without a structured timeline source (no Slack channel per incident, no alerts, no deploy log) — the agent will hallucinate without grounding.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
