---
slug: sdd-promotion-gate-checklist
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Formal backlog→todo promotion checklist that replaces gut-feel reviewer approval with a binary-pass artefact for SDD task-expansion gating."
content_id: "930d2725fb26054b"
tags: [sdd-promotion-gate-checklist, sdd, geek]
---
# SDD Promotion Gate Checklist

## Summary

**One-sentence:** A binary-pass checklist that reviewers run before moving an SDD feature from `backlog/` to `todo/`, ensuring every task is materialised, sized, and dependency-resolved.

**One-paragraph:** SDD lifecycle says `backlog/ → todo/` is a promotion gate, but no methodology defines what the reviewer actually checks. Reviewers fall back on gut feel, which lets half-expanded features into the executor's claim queue and breaks parallel waves. This methodology defines the canonical 7-item gate (task files exist, AC mapped, deps DAG-clean, token budget set, test-plan referenced, owner named, blockers documented) plus a signed gate record that lives in the feature's `.aidocs/_progress/` folder. Output is a versioned `promotion-gate.md` decision record.

## Applies If (ALL must hold)

- feature currently sits in `.aidocs/backlog/F-NNN/` with `implementation-plan.md` present
- task expansion has produced `tasks/todo/TASK_NN.md` files (not only inline tree)
- a human reviewer (or escalated reviewer agent) is about to approve promotion
- tier == geek (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- feature is a single-task hotfix that bypasses the formal lifecycle (`emergency/` track)
- repo does not use the `backlog/ → todo/` workflow at all (CIA exception)
- the feature already lives in `todo/` or later — apply retroactive audit instead

## Prerequisites

- read `docs/directory-structure.md` lifecycle table
- access to the feature's `.aidocs/<state>/F-NNN/` tree
- token-budget calculator or convention (e.g. ~50k per TASK)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdd/sdd-planning` | parent — defines plan/spec/design contracts that gate inputs reference |
| `solo/sdd/sdd` | execution model the promoted tasks will run under |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 binary-pass checklist rules + 1 worked example | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate_tasks` | haiku | filesystem walk + presence check |
| `verify_dag` | sonnet | parse `depends_on:` fields, detect cycles |
| `approve_or_reject` | opus | judgement on token estimates + AC coverage |

## Related

- parent skill: `geek/sdd/`
- `geek/sdd/sdd-planning`
- `solo/sdd/sdd`
- upstream playbook: `p6-product-dev-team/Sprint planning with SDD task expansion (bi-weekly)`
