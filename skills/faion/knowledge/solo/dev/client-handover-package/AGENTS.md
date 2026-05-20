---
slug: client-handover-package
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Client Handover Package: codified dev practice that turns the recurring 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)' decision into a repeatable, auditable artefact.
content_id: "96d5591f9144e081"
tags: [client-handover-package, dev, solo]
---
# Client Handover Package

## Summary

**One-sentence:** Client Handover Package: codified dev practice that turns the recurring 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)' decision into a repeatable, auditable artefact.

**One-paragraph:** Client Handover Package addresses the gap surfaced by 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)'. API docs methodology exists but there's no 'closeout package' SOP for solo devs: secrets, accounts, infra, runbook, Loom, future-roadmap doc. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)' task (last 30 days of activity)
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
| `templates/client-handover-package.json` | JSON schema for the Client Handover Package output contract |
| `templates/client-handover-package.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-handover-package.py` | Enforce Client Handover Package output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/software-developer/`
- upstream playbook: `p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)`
- methodology family: `solo/dev/` (gap-p2 batch, F-059-063)
