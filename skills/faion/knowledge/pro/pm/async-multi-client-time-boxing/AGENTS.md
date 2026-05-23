---
slug: async-multi-client-time-boxing
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Async Multi Client Time Boxing: codified delivery-management practice that turns the recurring 'p3-technical-freelancer/Freelancer-to-SaaS transition without losing the runway' decision into a repeatable, auditable artefact.
content_id: "a866d47be9a4d760"
complexity: medium
produces: spec
est_tokens: 4000
tags: [async-multi-client-time-boxing, pm, pro]
---
# Async Multi Client Time Boxing

## Summary

**One-sentence:** Async Multi Client Time Boxing: codified delivery-management practice that turns the recurring 'p3-technical-freelancer/Freelancer-to-SaaS transition without losing the runway' decision into a repeatable, auditable artefact.

**One-paragraph:** Async Multi Client Time Boxing addresses the gap identified by the p3-technical-freelancer/Freelancer-to-SaaS transition without losing the runway playbook: Context-switching across 3-5 active clients is the #4 pain. pro/pm methodology is full Jira/Azure-DevOps PMBOK. None of it addresses one operator running 3-5 micro-projects in parallel: time-block-per-client, weekly status batching, single-tool stack (one repo of notes, one tracker), notification gates. Borderline between pm and personal productivity. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

**Ефективно для:**

- Одного operator з 3-5 паралельних micro-projects.
- Time-block-per-client + weekly status batching.
- Single-tool stack: один repo нотаток, один tracker.
- Notification gates — не Slack-pinged-every-15-min.

## Applies If (ALL must hold)

- task is an instance of p3-technical-freelancer/Freelancer-to-SaaS transition without losing the runway OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p3-technical-freelancer/Freelancer-to-SaaS transition without losing the runway task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/async-multi-client-time-boxing.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/async-multi-client-time-boxing.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-async-multi-client-time-boxing.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p3-technical-freelancer/Freelancer-to-SaaS transition without losing the runway`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

