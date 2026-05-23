---
slug: tweet-thread-launch-template
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a 7-tweet launch-thread spec (hook → demo gif → problem → solve → price → CTA → social proof) tuned for indie-hacker X audiences and Product Hunt launch day."
content_id: "4afdde69ef09d9fe"
complexity: light
produces: spec
est_tokens: 3200
tags: [twitter-x, launch, indie-hacker, copywriting, product-hunt]
---

# Tweet Thread Launch Template

## Summary

**One-sentence:** Produces a 7-tweet launch-thread spec (hook → demo gif → problem → solve → price → CTA → social proof) tuned for indie-hacker X audiences and Product Hunt launch day.

**Ефективно для:** Indie hackers shipping on Product Hunt or solo launches who keep writing the launch thread on launch morning under pressure with no template discipline.

**One-paragraph:** The same 7-tweet shape outperforms ad-hoc launch threads by 3-5x on indie-hacker X. This template fixes the structure (hook, demo gif, problem, solve, price, CTA, social proof), enforces a tested-hook-variant rule, requires a real demo gif (not a screenshot), and refuses launches without ≥1 pre-launch social-proof quote. Output is a 7-tweet draft consumed by the launch scheduler.

## Applies If (ALL must hold)

- A real product (paid or free with email capture) is ready to launch.
- A demo gif or short video (<30s) exists showing the core use.
- Pricing decision is final.
- At least one social-proof quote (early customer or testing user) is on file.

## Skip If (ANY kills it)

- No product to launch yet — write distribution-first idea-validation post instead.
- Demo gif absent — film one before threading; static screenshots underperform.
- Product is a hard-B2B sale where X is not the buyer channel.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| product URL + one-liner | URL + string | founder decision |
| demo gif (<30s, 1080p, captions baked in) | gif/mp4 | internal video |
| pricing decision (final) | string | founder decision |
| ≥1 social-proof quote (permission logged) | string + handle | social-proof-harvest output |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/swipe-file-tweet-hooks` | Hook variants source. |
| `solo/marketing/social-proof-harvest` | Quote source with consent. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_3_hook_variants` | sonnet | Per-launch creative variants. |
| `score_hook_against_swipe` | haiku | Bounded similarity scoring. |
| `review_launch_thread` | opus | Final pre-publish judgement. |

## Templates

| File | Purpose |
|---|---|
| `templates/tweet-thread-launch-template.json` | JSON Schema for the output contract. |
| `templates/tweet-thread-launch-template.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-tweet-thread-launch-template.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[swipe-file-tweet-hooks]] — hook bank.
- [[social-proof-harvest]] — quote source.
- [[twitter-x-monetization-thread-to-product]] — funnel after launch.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
