---
slug: agent-postmortem-template
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Blameless postmortem template for incidents where the AI agent itself is the defendant — hallucinated tool calls, context overflow, jailbreak success, retrieval misread — with layer attribution and replay fields.
content_id: 371973b0699b2ba3
---

# Agent Postmortem Template

## Summary

The generic incident postmortem treats the engineer as the actor and the agent as a drafting tool. When the agent is the defendant — a tool call was fabricated, a retrieved snippet was misread, a prompt-injection slipped through, or a context window overflowed and dropped the system rule — that template hides the actual root cause. This methodology defines first-class fields for trace ID, model version, prompt diff, eval delta, and a forced layer-attribution step (model / system prompt / tool schema / tool result / retrieved context / user input) so the team converges on which layer to fix instead of arguing about whose fault it is.

## Applies If

- An agent-mediated action caused user-visible harm, customer escalation, or a failed eval in production.
- You have a stored trace (request id, model id, prompt rendered, tool calls, tool results) you can replay or partially replay.
- A named owner exists for at least one of the six layers (model, system prompt, tool schema, tool result, retrieved context, user input).
- The eval suite for this agent has a baseline score the incident can be compared against.

## Skip If

- The agent was only a drafting assistant for a human-owned action — use the standard engineer-incident postmortem instead.
- No trace was captured and cannot be reconstructed within 24h — write a "trace-gap" note and fix instrumentation first; a postmortem without trace is fiction.

## Content
See `content/01-core-rules.xml`.

## Related
- [[hallucination-incident-runbook]]
- [[hallucination-attribution-checklist]]
- [[ai-post-mortem-template]]
