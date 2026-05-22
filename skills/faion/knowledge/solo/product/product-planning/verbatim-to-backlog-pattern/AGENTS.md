---
slug: verbatim-to-backlog-pattern
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5f41f355a092bf27"
summary: Bridges Mom-Test verbatim customer quotes to prioritised backlog cards via a 4-step transform (extract → cluster → frame → prioritise) that keeps the customer's words attached to every story.
tags: [continuous-discovery, mom-test, backlog, prioritisation, solo-saas]
---

# Verbatim to Backlog Pattern

## Summary

**One-sentence:** Bridges Mom-Test verbatim customer quotes to prioritised backlog cards via a 4-step transform (extract → cluster → frame → prioritise) that keeps the customer's words attached to every story.

**One-paragraph:** Continuous-discovery methodologies tell solo SaaS builders to "talk to users"; backlog-management methodologies tell them to "prioritise by value". Nothing connects the two — so verbatim customer pain quotes turn into vague PM-language cards ("improve onboarding") that lose the original signal. This methodology codifies a 4-step transform: (1) EXTRACT pain statements from interview/inbox/Discord with timestamps, (2) CLUSTER similar pains by embedding similarity, (3) FRAME each cluster as a backlog card in Job-Story format with ≥ 2 verbatim quotes attached, (4) PRIORITISE by frequency × severity × strategic fit. Output: `BacklogCard` records with verbatim attachment links + RICE score.

## Applies If (ALL must hold)

- solo SaaS post-launch with ≥ 5 paying / active users
- ≥ 20 customer touchpoints in trailing 60 days (interviews, support tickets, Discord)
- backlog tool with custom-field support (Linear, GitHub Projects, Notion DB)
- operator wants prioritisation defensible by quote evidence

## Skip If (ANY kills it)

- pre-launch (no real customer voice yet) — use problem-validation, not this
- internal tool / no external users — backlog driven by stakeholders, not pattern
- single-user / wedge B2B engagement — N=1 doesn't cluster
- operator already has &gt; 200 cards in backlog — clean backlog first; this adds noise

## Prerequisites

- collection of customer touchpoints (transcripts, support tickets, Discord exports, DM threads)
- backlog tool with verbatim quote field (Linear's description, Notion DB column)
- embedding model API access (OpenAI, Voyage, Anthropic-via-Claude)
- prior 30 days of historical touchpoints for baseline

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/continuous-discovery` | Provides the touchpoint stream this methodology consumes |
| `pro/product/product-manager/backlog-management` | Provides the destination backlog format |
| `pro/research/researcher/jobs-to-be-done` | Job-Story framing borrowed from JTBD |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-step transform, verbatim attachment, cluster threshold, RICE prioritisation, anti-PM-language | ~1000 |
| `content/02-output-contract.xml` | essential | `BacklogCard` + cluster schemas | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: lossy paraphrase, cluster collapse, PM-rewrite, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pain_extraction_from_transcripts` | sonnet | Quote-mining bounded by Mom-Test r1 |
| `cluster_pains_by_embedding` | haiku | Mechanical embedding + clustering |
| `job_story_framing` | sonnet | Synthesis bounded by template |
| `rice_score_compute` | sonnet | Numeric model with explicit inputs |

## Templates

| File | Purpose |
|------|---------|
| `templates/backlog-card.json` | Output schema |
| `templates/job-story.md` | "When &lt;trigger&gt;, I want &lt;motivation&gt;, so I can &lt;outcome&gt;" frame |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/weekly-extract-cluster.py` | Process week's touchpoints into pain clusters | Cron Mon 10:00 |
| `scripts/backlog-card-pr.py` | Compose PR adding cards to backlog tool | After clustering |

## Related

- parent skill: `solo/product/product-planning/`
- peer methodologies: `continuous-discovery`, `backlog-management`, `jobs-to-be-done`
- external: [Rob Fitzpatrick — The Mom Test](https://momtestbook.com/) · [Teresa Torres — Continuous Discovery Habits](https://www.producttalk.org/continuous-discovery-habits/) · [Sean McBride / Marty Cagan on opportunity solution trees](https://www.svpg.com/) · [Intercom — Job Stories vs User Stories](https://www.intercom.com/blog/jobs-to-be-done-product-design/)
