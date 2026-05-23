---
slug: cutover-rollback-runbook-template
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a multi-wave migration cutover runbook with go/no-go gates, comms tree, and proven rollback for each wave.
content_id: "b176099dbb995899"
complexity: deep
produces: playbook-step
est_tokens: 4500
tags: [migration, cutover, rollback, runbook]
---
# Cutover Rollback Runbook Template

## Summary

**One-sentence:** Produces a multi-wave migration cutover runbook with go/no-go gates, comms tree, and proven rollback for each wave.

**One-paragraph:** `deploy-blue-green-canary` is task-level; a multi-wave cutover runbook with go/no-go gates, comms tree, and proven rollback per wave is missing for legacy-to-modern migrations. This methodology pins a runbook structure where each wave declares: entry criteria, executed steps, gate checks, rollback path, comms cadence. Each wave's rollback is rehearsed once in staging before the corresponding production cutover; rollback evidence is attached.

**Ефективно для:**

- Legacy-to-modern migration з multi-wave cutover (3+ хвилі по тижню).
- коли deploy-blue-green-canary є task-level, а multi-wave runbook відсутній.
- потрібні go/no-go gates, comms tree, rollback proof перед production cutover.
- P4-outsource-specialist веде клієнтський проєкт ~3 місяці.

## Applies If (ALL must hold)

- Migration is multi-wave (>=3 waves) and crosses a production boundary.
- Each wave has identified blast radius and an explicit rollback strategy.
- Comms tree is named (who pages whom, in what order).
- Rollback can be rehearsed in staging before each production wave.

## Skip If (ANY kills it)

- Migration is single-wave or in-place upgrade — `deploy-blue-green-canary` is sufficient.
- No production users yet — cutover discipline does not apply.
- Team has a tested multi-wave runbook from a prior migration — re-use it.
- Rollback is structurally impossible (data-destructive cutover) — different methodology (data-migration-runbook).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source + target system inventory | Markdown / spreadsheet | migration lead |
| Wave plan | numbered list with blast radius | architect |
| Comms tree | list of names + channels | engagement lead |
| Rollback strategy per wave | Markdown | architect |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/deploy-blue-green-canary` | wave-level deploy mechanics |
| `pro/infra/devops-engineer` | parent role skill |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r1-bound-scope) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate-waves` | sonnet | Decompose migration into ordered waves with blast radius |
| `draft-rollback-per-wave` | sonnet | Per-wave rollback path with rehearsal evidence |
| `compose-comms-tree` | haiku | Mechanical list of names + channels |
| `final-gate-review` | opus | Cross-wave consistency + risk concentration check |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Multi-wave cutover runbook skeleton with gates |
| `templates/skeleton.json` | JSON schema for the cutover artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cutover-rollback-runbook-template.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[deploy-blue-green-canary]]
- [[incident-response-rotation]]
- [[data-migration-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Cutover Rollback Runbook Template methodology when in doubt about scope or fit.
