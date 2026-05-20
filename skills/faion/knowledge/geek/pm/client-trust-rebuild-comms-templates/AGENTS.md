---
slug: client-trust-rebuild-comms-templates
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Client Trust Rebuild Comms Templates: codified pm practice that turns the recurring 'role-project-manager/Distressed-project rescue (six-week turnaround)' decision into a repeatable, auditable artefact.
content_id: "220822555ab37e5b"
tags: [client-trust-rebuild-comms-templates, pm, geek]
---
# Client Trust Rebuild Comms Templates

## Summary

**One-sentence:** Client Trust Rebuild Comms Templates: codified pm practice that turns the recurring 'role-project-manager/Distressed-project rescue (six-week turnaround)' decision into a repeatable, auditable artefact.

**One-paragraph:** Client Trust Rebuild Comms Templates addresses the gap surfaced by 'role-project-manager/Distressed-project rescue (six-week turnaround)'. When a project goes red the comms register completely changes (more direct, shorter cycles, more written confirmations). No template set exists for the apology / reset / recovery cadence emails and decks. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-project-manager/Distressed-project rescue (six-week turnaround)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-project-manager/Distressed-project rescue (six-week turnaround)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill — provides the operating context for this methodology |

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
| `templates/client-trust-rebuild-comms-templates.json` | JSON schema for the Client Trust Rebuild Comms Templates output contract |
| `templates/client-trust-rebuild-comms-templates.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-trust-rebuild-comms-templates.py` | Enforce Client Trust Rebuild Comms Templates output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/project-manager/`
- upstream playbook: `role-project-manager/Distressed-project rescue (six-week turnaround)`
- methodology family: `geek/pm/` (gap-p2 batch, F-059-063)
