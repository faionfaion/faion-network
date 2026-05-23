---
slug: threads-basics
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Threads setup + content strategy for accounts leveraging an Instagram audience; 7-10 posts/day, reply velocity, ≤500 chars, banned engagement-bait, pillar tags, no auto-post.
content_id: "95915b81d9e74541"
complexity: medium
produces: spec
est_tokens: 4400
tags: [threads, meta, social-media, content-strategy, community]
---
# Threads Basics

## Summary

**One-sentence:** Setup + content strategy for Meta Threads — text-first, leveraging Instagram audience, growth driven by conversational content + 7-10 posts/day + reply velocity, not volume alone.

**One-paragraph:** Threads crossed 100M users rapidly; early adopters get reach upside before competition densifies. Accounts that cross-post X verbatim underperform — Threads rewards a warmer conversational register. No stable scheduling API exists at the start of 2026; the operator posts manually from a ranked draft pool the agent produces. This methodology pins the mechanics into testable rules: 3-10 posts/day, ≤500 chars, banned engagement-bait phrases, pillar tags, hook bigram rotation, and a 50% cap on agent-generated drafts. Output: a daily content pack of 5-12 ranked drafts validated against the contract.

**Ефективно для:**

- Брендів з вже існуючою Instagram-аудиторією.
- High-cadence 7-10 постів/день з reply-velocity у першу годину.
- Drafts ≤500 chars + pillar tag + bigram rotation.
- Operator picks 7-10 з 20 agent-ranked candidates manually.
- Conversational-register rewrites замість X-verbatim cross-post.

## Applies If (ALL must hold)

- Standing up a brand or founder presence on Threads while leveraging an existing Instagram audience.
- Drafting daily content packs (5-12 posts) for a SMM operator who has defined voice guidelines.
- Auditing an account that cross-posts from X/Twitter verbatim and is underperforming.
- Hot-take and conversation-starter ideation for accounts where engagement bait is acceptable.
- Bootstrapping a new niche account that needs cadence and format scaffolding.

## Skip If (ANY kills it)

- Target audience does not overlap with Instagram demographics (e.g., enterprise security buyers — use LinkedIn).
- Brand voice forbids hot takes, personal stories, or unmoderated conversation.
- Team has zero capacity for replies — Threads' algorithm rewards reply velocity; posting alone plateaus within weeks.
- Regulated industries (finance, healthcare) where every post needs compliance review incompatible with the required cadence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Content pillars (Opinion / Value / Question / Personal / Curated) | YAML | operator's strategy doc |
| Banned-bigram + banned-phrase list | YAML | brand book + Meta moderation guidelines |
| Instagram audience export | CSV | Instagram Business account |
| Recent Threads insights | screenshots / CSV | Threads Insights tab |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/smm-manager/instagram-basics` | Sibling — Threads piggy-backs on Instagram audience + visual brand. |
| `pro/marketing/growth-social-media-strategy` | Upstream strategy: which platforms to invest in. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules (cadence, no X-verbatim, no auto-post, char cap, banned bait, bigram rotation, pillar) + self-routing anchors | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for a daily content pack + valid / invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (verbatim X cross-post, auto-post, identical hooks, engagement-bait, link-heavy, ignored replies) | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-daily-pack` | sonnet | Per-draft judgment: pillar tag, hook score, register rewrite. |
| `score-hook` | haiku | Mechanical 1-5 rating against the rubric. |
| `weekly-trend-synthesis` | opus | Cross-pack synthesis across 7 days; bigram rotation and pillar-balance check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/threads-basics.md` | Markdown skeleton (5-line header) for the daily content pack artefact. |
| `templates/threads-basics.json` | JSON Schema (draft-07) for the output contract. |
| `templates/bio-templates.txt` | Founder, expert, and creator bio formulas. |
| `templates/daily-posts.txt` | Morning/afternoon/evening post templates and multi-post thread format. |
| `templates/prompt-ideation.txt` | Daily content pack ideation prompt with pillar tags and hook scoring. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-threads-basics.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/smm-manager/`
- sibling: [[instagram-basics]]
- sibling: [[growth-twitter-x-growth]]
- sibling: [[growth-linkedin-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (audience-overlap-Instagram, reply capacity, brand-voice compatibility, regulatory load) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the SMM operator opens a fresh daily brief and must decide whether to invest the Threads pack today or route to a text-first sibling channel.

