---
slug: ai-pm-tool-integration-recipes
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Runnable PM integration recipes — Jira → Claude → Slack digest, GitHub PR → risk register, Loom transcripts → retro notes — with prompts, schemas, and code."
content_id: "f9b69d74b126b187"
complexity: medium
produces: code
est_tokens: 3900
tags: [pm, automation, claude, jira, github, loom, recipes]
---
# Ai Pm Tool Integration Recipes

## Summary

**One-sentence:** Runnable PM integration recipes — Jira → Claude → Slack digest, GitHub PR → risk register, Loom transcripts → retro notes — with prompts, schemas, and code.

**One-paragraph:** Runnable PM integration recipes — Jira → Claude → Slack digest, GitHub PR → risk register, Loom transcripts → retro notes — with prompts, schemas, and code. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM-у — щоб не писати інтеграції з нуля; брати готовий рецепт і адаптувати.

## Applies If (ALL must hold)

- Team uses one of {Jira, Linear, GitHub Projects} as tracker.
- Slack / Teams used for daily comms.
- Loom / Granola / Otter used for meeting capture.
- PM has scripting access (laptop or CI).

## Skip If (ANY kills it)

- Team uses a tracker outside the supported set — adapt manually.
- No comms platform for output — recipes need a destination.
- Regulated context requires custom audit handling — author from scratch instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tracker API token | secret | Jira / Linear / GitHub Projects |
| Comms webhook | URL | Slack / Teams |
| Transcript source API | token/URL | Loom / Granola / Otter |
| Claude API key | secret | Anthropic console |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/pm-agile/ai-in-project-management` | Framework the recipes live inside. |
| `geek/pm/exception-driven-standup-protocol` | One of the consumers of the digest output. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `recipe-scaffold-fill` | haiku | Template fill for the picked recipe. |
| `prompt-adapter` | sonnet | Bounded judgement: customise the prompt for team voice. |
| `multi-source-narrative` | opus | Cross-tool synthesis (e.g. Loom + Jira → retro). |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.py` | Python recipe skeleton: pull from Jira → call Claude with canonical prompt → post to Slack. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-pm-tool-integration-recipes.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[ai-in-project-management]]
- [[ai-powered-pm-tools]]
- [[exception-driven-standup-protocol]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to ship a recipe (all four feeds + scripting access), block (no API/key), or fall back to no-code AI PM tools. Run before any recipe code is touched.
