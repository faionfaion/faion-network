---
slug: puppeteer-agent-workflow
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers how AI agents should drive Puppeteer (stateless worker-process pattern, not inline in the LLM turn), known LLM-generated code gotchas, performance flags for resource blocking, CLI tools ecosystem, and managed browser services for production scraping.
content_id: "9db73cbd93fc6d7d"
tags: [puppeteer, agent-workflow, browser-automation, llm-integration, nodejs]
---
# Puppeteer: Agentic Workflow, LLM Gotchas & Performance

## Summary

**One-sentence:** Covers how AI agents should drive Puppeteer (stateless worker-process pattern, not inline in the LLM turn), known LLM-generated code gotchas, performance flags for resource blocking, CLI tools ecosystem, and managed browser services for production scraping.

**One-paragraph:** Covers how AI agents should drive Puppeteer (stateless worker-process pattern, not inline in the LLM turn), known LLM-generated code gotchas, performance flags for resource blocking, CLI tools ecosystem, and managed browser services for production scraping.

## Applies If (ALL must hold)

- Configuring an AI agent to generate and execute Puppeteer scripts as one-shot tool calls.
- Building a worker-process daemonised runner the agent talks to over a queue or HTTP.
- Selecting between self-hosted Puppeteer and managed browser services (Browserless, Apify, etc.).
- Auditing LLM-generated Puppeteer code for known anti-patterns before execution.

## Skip If (ANY kills it)

- Pure human-authored scripts where LLM gotchas are irrelevant — use puppeteer-launch-setup and puppeteer-page-interaction directly.
- Long-running sessions that require stateful browser state across multiple LLM turns — use a daemonised runner and expose an HTTP control API instead.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/automation-tooling/`
