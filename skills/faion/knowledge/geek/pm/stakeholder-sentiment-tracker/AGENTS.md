---
slug: stakeholder-sentiment-tracker
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Methodology for an ongoing per-stakeholder sentiment trend (supportive / cautious / hostile) built from emails, chat threads, and meeting transcripts — gives the PM early warning weeks before a sponsor goes red.
content_id: "ee051f615d10fd84"
tags: [project-manager, sentiment-tracker, distressed-project, ai-assisted, stakeholder-management, early-warning, rag]
---
# Stakeholder Sentiment Tracker

## Summary

**One-sentence:** A weekly AI-assisted methodology that ingests each stakeholder's text artefacts (emails, chat threads, meeting transcripts) and produces a `supportive | cautious | hostile` classification with a trend chart, giving the PM a 2-4 week head-start before a sponsor publicly turns red.

**One-paragraph:** A static stakeholder register identifies who matters, but says nothing about how their support is trending. On distressed projects, sponsors do not announce that they are going hostile — they go quiet, then mildly critical, then quietly route their team to a competitor. By the time it lands in a status meeting, the PM has lost 4-6 weeks. This methodology defines: an opt-in scope of source artefacts per stakeholder (with retention and consent rules), a fixed classification rubric (supportive / cautious / hostile, with concrete linguistic markers), a weekly run that produces a per-stakeholder score AND a trend line, and an alarm policy — two consecutive weeks of decline OR one week's classification as hostile triggers a documented PM action plan. The output lives in the rescue runbook and is the canonical early-warning artefact for `distressed-project-diagnostic-script`.

## Applies If (ALL must hold)

- Project is either on a 90-day rescue track OR has at least one sponsor whose engagement is critical to renewal.
- Written consent or organisational policy permits the PM to ingest the named source artefacts for sentiment tracking.
- The PM has access to per-stakeholder text streams (email aliases, Slack DMs, meeting transcripts) — not just public channels.
- A scheduling primitive (cron, scheduled remote agent) is available to run the weekly pipeline.

## Skip If (ANY kills it)

- No consent to ingest the artefacts — the methodology is non-negotiable on consent.
- Stakeholder pool is fluid (changes weekly) — register is not stable enough to track trends.
- Project length under 8 weeks — trend signal needs at least 4 weekly data points to be useful.
- Pure internal team with no external sponsors and no political risk — overhead exceeds value.

## Prerequisites

- Stable stakeholder register with at least the top 5 stakeholders.
- Per-stakeholder source list (emails, channel IDs, transcript folders) with consent documented.
- Storage location for weekly outputs (`rescue/sentiment/<date>.md` or equivalent).
- Pre-defined classification rubric file (closed vocabulary + markers).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/distressed-project-diagnostic-script` | This is the early-warning input to that script's rescue plan. |
| `geek/ai/rag-engineer/` | Underlying retrieval + classification mechanics for text artefacts. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: consent-first, fixed three-class rubric, weekly cadence, two-week decline alarm, action-plan attachment. | ~900 |

## Related

- parent skill: `geek/pm/project-manager/`
- peer: `distressed-project-diagnostic-script`, `client-trust-rebuild-comms-templates`, `incident-comms-templates-internal-external`
- external: NPS / sentiment-analysis methodology (Reichheld); FRAML-style risk monitoring patterns
