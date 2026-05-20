---
slug: ai-pm-tool-integration-recipes
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "321446301b273422"
summary: Runnable recipes that wire Jira → Claude → Slack digest, GitHub PR events → risk register update, and Loom transcripts → retro notes — with code, schemas, and the exact prompt scaffolds the PM ships.
tags: [pm, automation, claude, jira, github, loom, recipes, geek]
---
# AI PM Tool Integration Recipes

## Summary

**One-sentence:** Three runnable recipes that wire common PM tools to Claude — Jira → Claude → Slack digest, GitHub PR events → risk register update, Loom transcripts → retro notes — with checked-in code, JSON schemas, and the exact prompt scaffolds.

**One-paragraph:** `ai-powered-pm-tools` is a survey essay; this methodology ships executable. Each recipe is a small Python or TypeScript package the PM clones, configures with provider keys (`anthropic`, `github`, `jira`), and runs on a cron / webhook. Recipe 1: Jira → Claude → Slack — daily synthesis of in-progress tickets into a digest with risk callouts, posted to the team channel. Recipe 2: GitHub PR events → risk register — every PR that touches a flagged component re-evaluates the project's risk register entries. Recipe 3: Loom transcripts → retro notes — converts session transcripts into structured retro inputs (what worked / what didn't / actions). Output: three working integrations the PM can fork, configure, and run within one afternoon.

## Applies If (ALL must hold)

- PM has admin access (or API tokens) to Jira / Linear, GitHub, Slack, Loom.
- A provider key for Claude (or equivalent) is available.
- A cron / webhook runner is reachable (GitHub Actions, scheduled SDK agent, n8n, Pipedream).
- Team has a Slack channel or equivalent for the digest output.

## Skip If (ANY kills it)

- PM cannot get tool tokens (security policy) — use manual versions of the recipes.
- Team does not use Jira / GitHub / Loom — wire equivalents (Linear / GitLab / Granola) or skip the recipe.
- PM does not own a single team's project — broader integrations need the `dependency-graph-reasoning` methodology.
- Slack / Teams digest fatigue already an issue — start with one recipe instead of three.

## Prerequisites

- API tokens for Jira / Linear, GitHub, Slack, Loom (scoped read-only where possible).
- A repo to host the recipe configs (private; secrets in env / vault, never committed).
- A scheduling runtime (GitHub Actions, scheduled Anthropic SDK agent, n8n).
- An LLM provider with structured output support (Anthropic Claude with JSON mode, or equivalent).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager/ai-powered-pm-tools` | Survey-level methodology that introduces the concepts. |
| `geek/pm/project-manager/ai-in-project-management` | Background on AI-in-PM patterns. |
| `geek/sdlc-ai/tracker-jira-rovo-mcp-agents` | Sibling for Jira MCP integration. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: scoped tokens, structured output required, digest budget, retro-note template, PM signoff | ~1100 |
| `content/02-output-contract.xml` | essential | Digest schema, risk-register update schema, retro-note schema | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: token leak, runaway cost, hallucinated risk, retro fabrication | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `digest-summarise` | sonnet | Bounded synthesis across N tickets |
| `risk-classify-and-update` | sonnet | Per-PR judgement against risk register |
| `retro-extract` | sonnet | Structured extraction from transcript |
| `slack-format` | haiku | Mechanical: render to Slack markdown |

## Templates

| File | Purpose |
|------|---------|
| `templates/digest-schema.json` | JSON schema for the Jira digest |
| `templates/risk-register.json` | JSON schema for risk-register entries |
| `templates/retro-notes.json` | JSON schema for retro outputs |
| `templates/prompts/digest.xml` | XML prompt scaffold for digest recipe |
| `templates/prompts/risk.xml` | XML prompt scaffold for risk recipe |
| `templates/prompts/retro.xml` | XML prompt scaffold for retro recipe |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/recipe-1-jira-digest.py` | Pull Jira tickets, call Claude, post Slack digest | Daily cron |
| `scripts/recipe-2-pr-risk-update.py` | Triggered by GitHub webhook on PR events; updates risk register | On PR event |
| `scripts/recipe-3-loom-retro.py` | Process a Loom transcript URL into retro notes | After each retro Loom |

## Related

- parent skill: `geek/pm/project-manager/`
- peer methodologies: `ai-powered-pm-tools`, `ai-earned-value-management`, `ai-in-project-management`
- external: [Anthropic SDK](https://docs.claude.com/en/api/) · [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) · [GitHub Webhooks](https://docs.github.com/en/webhooks)
