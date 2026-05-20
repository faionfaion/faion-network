---
slug: multi-region-failover-pattern-pack
tier: geek
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Multi Region Failover Pattern Pack: codified dev practice that turns the recurring 'role-software-architect/Disaster-recovery plan + live drill' decision into a repeatable, auditable artefact.
content_id: "9801ea9eaede6aca"
tags: [multi-region-failover-pattern-pack, dev, geek]
---
# Multi Region Failover Pattern Pack

## Summary

**One-sentence:** Multi Region Failover Pattern Pack: codified dev practice that turns the recurring 'role-software-architect/Disaster-recovery plan + live drill' decision into a repeatable, auditable artefact.

**One-paragraph:** Multi Region Failover Pattern Pack addresses the gap identified by the role-software-architect/Disaster-recovery plan + live drill playbook: Multi-region failover (active-active vs active-passive, data replication, DNS strategies) is a top architect topic absent at geek tier; reliability-architecture stays generic. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-software-architect/Disaster-recovery plan + live drill OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-software-architect/Disaster-recovery plan + live drill task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/multi-region-failover-pattern-pack.json` | JSON schema for the Multi Region Failover Pattern Pack output contract |
| `templates/multi-region-failover-pattern-pack.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-region-failover-pattern-pack.py` | Enforce Multi Region Failover Pattern Pack output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/dev/software-developer/`
- upstream playbook: `role-software-architect/Disaster-recovery plan + live drill`
