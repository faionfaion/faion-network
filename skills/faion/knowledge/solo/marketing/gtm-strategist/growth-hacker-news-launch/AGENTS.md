---
slug: growth-hacker-news-launch
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Show HN launch spec: 4-week reputation runway, non-hypey title, post timing window, 24-48h engagement plan, sanity-check on title and karma threshold — for developer-audience products with substance.
content_id: "eb103542f8df58ad"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["hacker-news", "product-launch", "developer-audience", "solo"]
---
# Hacker News Launch Strategy

## Summary

**One-sentence:** Generates a Show HN launch spec: 4-week reputation runway, non-hypey title, post timing window, 24-48h engagement plan, sanity-check on title and karma threshold — for developer-audience products with substance.

**One-paragraph:** Hacker News Launch Strategy produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo developer founder shipping a dev-tool / OSS / SaaS who needs a Show HN launch spec with reputation runway, title rules, and engagement plan — to avoid the 'flagged after 2 hours' fate.

## Applies If (ALL must hold)

- Product is dev-tool, OSS, SaaS, or research aimed at HN audience
- Founder has or can build ≥4 weeks of authentic HN participation
- Demo URL works on day-of-launch without auth

## Skip If (ANY kills it)

- Non-developer audience (consumer, fashion, finance retail) — HN is wrong room
- No working demo / login wall — HN flags it instantly
- Built specifically for HN attention without product-market signal — refocus first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| HN account with ≥4 weeks of authentic activity | account | news.ycombinator.com |
| Working demo URL (no signup wall) | URL | deployment |
| Substance-first title draft | string | founder copy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `growth-product-hunt-launch` | Adjacent launch channel. |
| `growth-indiehackers-strategy` | Pre-launch community presence. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-reputation-runway-4-weeks, r2-title-substance-not-hype, r3-post-time-window-tue-thu-am-et, r4-engagement-window-24-48h, r5-demo-no-auth-wall, r6-one-shot-or-relaunch-after-month | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-growth-hacker-news-launch` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-growth-hacker-news-launch` | haiku | Schema check + threshold checks; deterministic. |
| `review-growth-hacker-news-launch` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-hacker-news-launch.json` | JSON skeleton conforming to the output contract schema. |
| `templates/growth-hacker-news-launch.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-hacker-news-launch.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[growth-product-hunt-launch]]
- [[growth-indiehackers-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
