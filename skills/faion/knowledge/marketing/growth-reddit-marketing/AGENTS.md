# Long-Game Reddit Marketing

## Summary

**One-sentence:** Produces a Reddit-marketing plan artefact (subreddit shortlist + lurk plan + posting plan) gated by a 10:1 value-to-promo ratio and a karma-history threshold.

**One-paragraph:** Solo operators drop launch posts in target subreddits from day-1 accounts and get banned. This methodology pins a long-game Reddit plan: ≥30 days of organic comments + ≥100 karma before any promo, 10:1 value-to-promo ratio per subreddit, per-subreddit rule sheets, no link-only posts, and a single named brand account. Output: a Reddit plan spec.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-reddit-marketing» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator has ≥30 days runway to lurk before promoting.
- Target subreddits exist with active moderation.
- Operator can commit to a single account (not a throwaway).

## Skip If (ANY kills it)

- Operator wants results within 7 days — Reddit is not a fast channel.
- Target subreddits explicitly ban any commercial mention.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Subreddit shortlist | list | operator research |
| Brand account profile | Reddit account URL | ops |
| Value-post backlog (≥10) | drafts | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/conversion-optimizer/growth-landing-page-design` | Destination LP for the eventual promo posts. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the reddit-plan artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-reddit-marketing.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-reddit-marketing.json` | reddit-plan JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-reddit-marketing.py` | Validate the reddit-plan artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[growth-landing-page-design]]
- [[dm-personalisation-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
