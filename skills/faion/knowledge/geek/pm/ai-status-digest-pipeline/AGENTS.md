---
slug: ai-status-digest-pipeline
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ai Status Digest Pipeline: codified delivery-management practice that turns the recurring 'role-project-manager/Async cross-timezone delivery cadence (P4 outsource)' decision into a repeatable, auditable artefact.
content_id: "d9998db7f490888e"
tags: [ai-status-digest-pipeline, pm, geek]
---
# Ai Status Digest Pipeline

## Summary

**One-sentence:** Ai Status Digest Pipeline: codified delivery-management practice that turns the recurring 'role-project-manager/Async cross-timezone delivery cadence (P4 outsource)' decision into a repeatable, auditable artefact.

**One-paragraph:** Ai Status Digest Pipeline addresses the gap identified by the role-project-manager/Async cross-timezone delivery cadence (P4 outsource) playbook: communications-management gives comms-plan.md template; nothing wires actual data sources (Jira + GitHub + Slack + budget sheet) into AI-drafted weekly digest with red-yellow-green auto-classification. This is the 80% of PM busywork that AI can absorb. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-project-manager/Async cross-timezone delivery cadence (P4 outsource) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-project-manager/Async cross-timezone delivery cadence (P4 outsource) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-llm-grounding | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-status-digest-pipeline.json` | JSON schema for the Ai Status Digest Pipeline output contract |
| `templates/ai-status-digest-pipeline.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-status-digest-pipeline.py` | Enforce Ai Status Digest Pipeline output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- upstream playbook: `role-project-manager/Async cross-timezone delivery cadence (P4 outsource)`
- external: [RAGAS](https://docs.ragas.io/) · [Anthropic agent design](https://docs.anthropic.com/en/docs/build-with-claude/agents)
