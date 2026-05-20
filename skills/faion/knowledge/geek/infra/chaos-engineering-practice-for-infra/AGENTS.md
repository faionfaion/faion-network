---
slug: chaos-engineering-practice-for-infra
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Infra game-days: Litmus/Chaos Mesh experiment design, steady-state hypothesis, blast-radius containment, learning capture.
content_id: "854370fdb4d54b36"
tags: [chaos-engineering-practice-for-infra, infra, geek]
---

# Chaos Engineering Practice for Infra

## Summary

**One-sentence:** Infra game-days: Litmus/Chaos Mesh experiment design, steady-state hypothesis, blast-radius containment, learning capture.

**One-paragraph:** Only chaos-eval-fault-injection exists, scoped to AI agents. Missing: infra game-days for human-operated systems. Mechanism: steady-state hypothesis first, blast-radius caps, runbook-driven recovery, post-mortem with one action item. Output: experiment plan + steady-state metric + blast-radius cap + learning record.

## Applies If (ALL must hold)

- production infra with ≥1 SLO (latency, availability, error budget)
- on-call rotation exists
- team has authority to deliberately break things in a controlled blast radius

## Skip If (ANY kills it)

- no SLO defined — set SLOs first
- no observability — game-days produce blind chaos without metrics
- team in active P1/P2 backlog — defer game-days until backlog drains

## Prerequisites

- SLO definitions per service
- Chaos tool installed (Litmus, Chaos Mesh, Gremlin, AWS FIS, or custom)
- feature-flag or namespace-level blast-radius control

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent skill — provides operating context for this methodology |
| `geek/ai/chaos-eval-fault-injection` | peer methodology — produces inputs or consumes outputs |
| `geek/sdlc-ai/incident-response` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodology: `geek/ai/chaos-eval-fault-injection`
- peer methodology: `geek/sdlc-ai/incident-response`
- external: https://principlesofchaos.org/ (Principles of Chaos Engineering); https://litmuschaos.io/; https://chaos-mesh.org/
