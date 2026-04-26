# Threads Growth

## Summary

A conversation-first growth system for Threads: post 5+ short punchy posts per day,
reply thoughtfully to large accounts to drive discovery, and adapt content from Instagram
or Twitter to Threads' casual tone. No links in posts — Threads suppresses promotional
content. No official third-party posting API as of 2026; all posting is manual.

## Why

Threads rewards authenticity signals — genuine disagreement, admitted uncertainty, and
follow-up questions outperform polished takes. One early, thoughtful reply on a 100K-follower
post outperforms five standalone posts for discovery. The platform is tied to Instagram:
cross-promoting from Instagram Stories ("join the conversation on Threads") is the fastest
follower import mechanism, and any Instagram account restriction affects Threads access.

## When To Use

- Generating daily post batches (20-30 drafts) across hot takes, this-or-that, fill-in-blank,
  experience stories, and predictions
- Drafting reply templates for a specific niche (to be edited and sent by a human)
- Planning a cross-platform content flow from Instagram or Twitter to Threads
- Repurposing Twitter/X thread content into Threads-native conversational format
- Writing a Month 2-3 optimization plan: which post types to double down on

## When NOT To Use

- Automated posting or replying — no official API for write access; all posting is manual
- Engagement pod coordination — Threads community strongly penalizes inauthentic engagement
- Generating long-form content — Threads punishes long posts; max 300 characters is target
- Accounts without an Instagram presence — Threads account depends on Instagram; fix that first
- Generating posts that mimic trends without knowing current platform culture

## Content

| File | What's inside |
|------|---------------|
| `content/01-conversation-strategy.xml` | Reply formula, conversation-starter types, cross-platform synergy rules |
| `content/02-growth-patterns.xml` | Common mistakes, metrics benchmarks, scaling milestones |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-post-batch.txt` | Agent prompt: 20 Threads post drafts across all conversation-starter types |
| `templates/adapt-twitter-thread.py` | Strip tweet numbering, split into ≤3 Threads-native posts, append question |
