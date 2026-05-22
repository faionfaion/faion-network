---
slug: prompt-engineering-security
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production LLM systems face prompt injection, jailbreaking, and data exfiltration risks.
content_id: "7cb9496c36245a5d"
tags: [prompt-injection, security, guardrails, prompt-engineering, llm-security]
---
# Prompt Engineering — Security and Injection Defense

## Summary

**One-sentence:** Production LLM systems face prompt injection, jailbreaking, and data exfiltration risks.

**One-paragraph:** Production LLM systems face prompt injection, jailbreaking, and data exfiltration risks. This methodology covers input sanitization, delimiter-based isolation, system prompt hardening, jailbreak detection, content moderation patterns, output filtering, and monitoring — with Python implementations and checklist-driven verification.

## Applies If (ALL must hold)

- Any LLM system that processes user-supplied text (chatbots, document processors, agents).
- Systems where model outputs could trigger real-world actions (email sending, API calls, code execution).
- Applications handling sensitive data (PII, credentials, financial data).
- Multi-agent systems where one agent's output becomes another agent's prompt.
- Agentic pipelines that read untrusted external content (web pages, uploaded files).

## Skip If (ANY kills it)

- Internal tooling with no user-supplied text — security overhead is not justified.
- Closed test environments with controlled inputs only.
- Replacing proper authentication and authorization — prompt hardening is defense-in-depth, not a substitute for access control.

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

- parent skill: `geek/ai/ml-engineer/`
