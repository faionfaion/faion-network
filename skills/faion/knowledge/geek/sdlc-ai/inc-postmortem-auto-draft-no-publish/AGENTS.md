# Postmortem Auto-Draft, Never Auto-Publish

## Summary

When an incident is resolved, an LLM agent (Rootly, incident.io, FireHydrant pattern) drafts the postmortem from structured signals — Slack channel transcript, alert + deploy timeline, ChatOps `/incident actionitem` calls, linked PRs — into a fixed template (`Summary / Timeline / Impact / Root Cause Hypothesis / Contributing Factors / Action Items`) with `tone=blameless`. The draft lands as a *non-published* document assigned to the incident commander; humans edit, accept the root-cause framing, and publish. The agent must never auto-publish, never invent facts beyond the structured signal set, and must mark every speculative claim `(hypothesis)`.

## Why

Postmortems get skipped because writing the timeline is the painful 80% of the work; auto-drafting that 80% turns "we never wrote it up" into "we edited a draft in 30 minutes" — Rootly published a 5x throughput improvement with this exact split. But auto-publishing is the failure mode that kills trust: an LLM that picks the wrong root cause and posts it to the org-wide doc destroys the postmortem's value as a learning artifact and exposes legal risk in regulated incidents. Forcing a human-publish step keeps the speed without the misattribution. Marking hypotheses inline preserves the difference between "the deploy correlates with the alert" (fact) and "the deploy caused the outage" (hypothesis under review).

## When To Use

- Teams that currently skip postmortems because writing them is painful.
- Incident-management tools with an autodraft API (Rootly, incident.io, FireHydrant, PagerDuty) or a custom pipeline over Slack + alert + deploy data.
- Engineering cultures that have already adopted blameless postmortem norms.
- Regulated environments where a fast, accurate first-draft helps meet 72-hour reporting windows (EU NIS2, SOC2 incident reporting).

## When NOT To Use

- Highly regulated incidents (legal, safety, financial) where every sentence must be authored by a human from scratch.
- Tiny teams (≤5 engineers) where the human writes faster than they can review an LLM draft.
- Teams without a structured timeline source (no Slack channel per incident, no alerts, no deploy log) — the agent will hallucinate without grounding.

## Content

| File | What's inside |
|------|---------------|
| `content/01-no-auto-publish-rule.xml` | Auto-draft yes, auto-publish no; required template sections; hypothesis marking. |
| `content/02-grounded-timeline-only.xml` | Timeline lines must be derived from the structured signal set, citing source IDs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/postmortem-template.md` | Six-section blameless template the agent fills in. |
| `templates/draft_postmortem_prompt.txt` | Prompt fragment that enforces no-publish, hypothesis tagging, and citation format. |
