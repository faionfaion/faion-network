# Feedback Management

## Summary

Systematic pipeline for collecting feedback from multiple channels, categorizing it against a locked taxonomy, aggregating patterns by topic and segment, linking top clusters to backlog items, and closing the loop with users when their requests ship. The pipeline runs: Collect → Categorize → Analyze → Prioritize → Act → Close Loop. Taxonomy is code-versioned; changes require a migration and re-tag run.

## Why

Feedback scattered across support tickets, in-app forms, app store reviews, sales calls, and social creates a situation where loudest voices dominate decisions and quiet churners go unheard. Without a structured system, important signals drown in noise, users feel unheard, and teams build for vocal minorities. Centralizing, weighting by segment/ARR (not raw mention count), and closing the loop converts feedback from a complaint queue into a product intelligence channel.

## When To Use

- Feedback arriving from 3+ channels and a human can no longer triage in real time.
- You want a daily/weekly digest of categorized, deduplicated, prioritized requests linked to backlog items.
- Automated close-the-loop emails needed when a requested feature ships.
- Sentiment tracking against a release or pricing change is required.

## When NOT To Use

- Fewer than 20 feedback items per week — manual handling beats pipeline overhead.
- High-stakes B2B accounts where every quote requires named-customer context — keep human in the loop end-to-end.
- Regulated industries (medical, finance) where verbatim handling has compliance constraints — PII redaction first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-feedback-pipeline.xml` | Source types, categorization taxonomy (by type and topic), 6-step process, agent workflow, and prompt patterns. |
| `content/02-feedback-patterns.xml` | Concrete examples (monthly review, app store response strategy), antipatterns, and agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feedback-log.md` | Raw feedback table with category breakdown by month, top requests with segment and status. |
| `templates/feedback-responses.md` | Three response templates: feature shipped, not planned, needs more info. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/triage.py` | Single-item triage: normalizes text, computes dedup hash, calls LLM with strict JSON schema, validates topic against taxonomy. |
