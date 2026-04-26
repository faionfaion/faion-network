# Feedback Management

## Summary

A six-stage pipeline (Collect → Categorize → Analyze → Prioritize → Act → Close Loop) for turning scattered user input into systematic product decisions. Sources range from support tickets to app-store reviews; each item is tagged by type, topic, segment, and sentiment using a fixed taxonomy. Aggregation is weighted by ARR/retention risk, not raw mention count. Every decision closes the loop with a user-facing response.

## Why

Without a structured system, feedback is dominated by the loudest voices, scattered across channels, and never linked to backlog items. Users feel unheard; PMs lack signal on what to build next. A centralized pipeline with a fixed taxonomy and mandatory close-loop step converts feedback from noise into a ranked priority input that feeds directly into roadmap sessions.

## When To Use

- Inbound feedback volume exceeds human triage capacity (&gt;20 items/day across channels).
- Multiple disconnected sources (support tickets, app store, in-app widget, social, sales) need a single canonical store.
- Recurring monthly review cycle must surface patterns, rank by segment and revenue, and link to backlog items.
- Close-loop emails to specific requesters are repetitive but high-leverage.
- Pre-roadmap sessions where PM needs "top 10 themes from last 90 days with verbatim citations."

## When NOT To Use

- Pre-PMF with &lt;5 feedback items/week — direct human reading is faster and richer.
- High-stakes strategic decisions (pivot, kill) where verbatim nuance matters more than count.
- Compliance-bound feedback (HIPAA, GDPR DSAR text) where LLM ingestion needs DPA review first.
- Single-channel products where the channel tool's native AI already handles categorization.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline.xml` | Six-stage pipeline, feedback sources table, categorization taxonomy, processing rules. |
| `content/02-examples.xml` | Monthly review example and app-store review response strategy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feedback-log.md` | Feedback log with by-category summary, top requests table, trends section. |
| `templates/response-templates.md` | Three close-loop email templates: Shipped, Not Planned, More Info Needed. |
| `templates/triage-feedback.sh` | Bash: pipes feedback lines to Claude Haiku triage agent, emits JSONL. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/triage-feedback.sh` | Categorizes feedback items via Claude API; emits one JSON object per item with type, topic, segment, sentiment, confidence. |
