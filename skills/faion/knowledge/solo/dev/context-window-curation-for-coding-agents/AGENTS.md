---
slug: context-window-curation-for-coding-agents
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Context Window Curation For Coding Agents: codified dev practice that turns the recurring 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)' decision into a repeatable, auditable artefact.
content_id: "b761936789f1944b"
tags: [context-window-curation-for-coding-agents, dev, solo]
---
# Context Window Curation For Coding Agents

## Summary

**One-sentence:** Context Window Curation For Coding Agents: codified dev practice that turns the recurring 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)' decision into a repeatable, auditable artefact.

**One-paragraph:** Context Window Curation For Coding Agents addresses the gap surfaced by 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)'. Vibe-coded breakage usually starts when the agent has the wrong files in context. Need an explicit method: how to pick files, when to summarize history, when to wipe context. Nothing in faion teaches this. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

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
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/context-window-curation-for-coding-agents.json` | JSON schema for the Context Window Curation For Coding Agents output contract |
| `templates/context-window-curation-for-coding-agents.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-context-window-curation-for-coding-agents.py` | Enforce Context Window Curation For Coding Agents output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/software-developer/`
- upstream playbook: `p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)`
- methodology family: `solo/dev/` (gap-p2 batch, F-059-063)
