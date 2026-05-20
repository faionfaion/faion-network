---
slug: pair-with-ai-agent-protocol
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Pair With Ai Agent Protocol: codified dev practice that turns the recurring 'role-software-developer/Pair / mob session with junior on AI-assisted task' decision into a repeatable, auditable artefact.
content_id: "c041531f78c356bd"
tags: [pair-with-ai-agent-protocol, dev, solo]
---
# Pair With Ai Agent Protocol

## Summary

**One-sentence:** Pair With Ai Agent Protocol: codified dev practice that turns the recurring 'role-software-developer/Pair / mob session with junior on AI-assisted task' decision into a repeatable, auditable artefact.

**One-paragraph:** Pair With Ai Agent Protocol addresses the gap identified by the role-software-developer/Pair / mob session with junior on AI-assisted task playbook: Pair / mob programming methodologies predate AI agents. Specific protocol for three-way pairing (driver + navigator + agent) is needed because the agent shifts the failure modes. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-software-developer/Pair / mob session with junior on AI-assisted task OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-software-developer/Pair / mob session with junior on AI-assisted task task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/pair-with-ai-agent-protocol.json` | JSON schema for the Pair With Ai Agent Protocol output contract |
| `templates/pair-with-ai-agent-protocol.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pair-with-ai-agent-protocol.py` | Enforce Pair With Ai Agent Protocol output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/software-developer/`
- upstream playbook: `role-software-developer/Pair / mob session with junior on AI-assisted task`
