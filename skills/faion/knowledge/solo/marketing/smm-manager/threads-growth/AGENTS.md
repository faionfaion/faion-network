---
slug: threads-growth
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Generates a conversation-first Threads growth playbook-step (≥5 short posts/day + replies to large accounts + adapted IG/X content in casual tone)."
content_id: "b5e3aefc41974123"
complexity: medium
produces: playbook-step
est_tokens: 4000
tags: [threads, meta, conversation, growth, social-media]
---

# Threads Growth

## Summary

**One-sentence:** Generates a conversation-first Threads growth playbook-step (≥5 short posts/day + replies to large accounts + adapted IG/X content in casual tone).

**Ефективно для:** Solo creators with existing IG/X audiences who need a Threads presence without doubling content workload — leans on adaptation + reply-density.

**One-paragraph:** Threads rewards conversational density. This methodology produces a daily playbook-step: ≥5 short punchy posts, thoughtful replies to large accounts for discovery, and content adapted (not copy-pasted) from existing IG or X to Threads' casual tone. Output is a daily batch + reply-target list consumed by Meta's native scheduler.

## Applies If (ALL must hold)

- An existing audience exists on IG or X (≥1k followers) to seed Threads cross-promotion.
- Operator can spend 20-30 minutes/day on Threads.
- Buyers / audience are on Meta platforms.
- Operator can adapt voice from formal (X) to casual (Threads).

## Skip If (ANY kills it)

- No IG or X audience to cross-promote — Threads is hard to grow from zero.
- Buyers are not on Meta (e.g., dev-tools B2B targeting backend engineers).
- Operator refuses casual register — Threads suppresses corporate tone.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| existing IG or X audience snapshot | follower count + URL | platform export |
| daily 20-30 min Threads slot | calendar block | self-managed |
| adaptation guide (X → Threads, IG caption → Threads) | doc | internal style guide |
| large-account reply target list | csv | manual curation |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/instagram-growth` | IG source for adapted content. |
| `solo/marketing/smm-manager/growth-twitter-x-growth` | X source for adapted content. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `adapt_x_to_threads` | haiku | Tone conversion — bounded transformation. |
| `draft_native_thread_posts` | sonnet | Conversation-shaped hooks. |
| `review_voice_drift` | opus | Cross-platform voice consistency. |

## Templates

| File | Purpose |
|---|---|
| `templates/threads-growth.json` | JSON Schema for the output contract. |
| `templates/threads-growth.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-threads-growth.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[instagram-growth]] — IG cross-source.
- [[growth-twitter-x-growth]] — X cross-source.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
