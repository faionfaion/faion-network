---
slug: tool-deprecation-lifecycle
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "0647285ab449d099"
summary: "Tool Deprecation Lifecycle: produces a versioned, owner-signed artefact that closes the gap 'p7-llm-agent-developer/New tool-call schema design session'."
tags: [tool-deprecation-lifecycle, ai, geek]
---
# Tool Deprecation Lifecycle

## Summary

**One-sentence:** Tool Deprecation Lifecycle: produces a versioned, owner-signed artefact that closes the gap 'p7-llm-agent-developer/New tool-call schema design session'.

**One-paragraph:** Addresses the gap surfaced by 'p7-llm-agent-developer/New tool-call schema design session': Tool schemas churn weekly in agent products; there is no opinionated deprecation/migration policy in the corpus. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tool deprecation lifecycle artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p7-llm-agent-developer/New tool-call schema design session' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tool deprecation lifecycle artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p7-llm-agent-developer/New tool-call schema design session' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai` | parent domain group — provides operating context for Tool Deprecation Lifecycle |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-deprecation-lifecycle.json` | JSON schema for the Tool Deprecation Lifecycle output contract |
| `templates/tool-deprecation-lifecycle.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-deprecation-lifecycle.py` | Enforce Tool Deprecation Lifecycle output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/`
- upstream playbook: `p7-llm-agent-developer/New tool-call schema design session`
- geek/ai/p7-llm-agent-developer
