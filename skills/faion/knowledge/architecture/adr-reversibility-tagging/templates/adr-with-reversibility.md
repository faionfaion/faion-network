# purpose: ADR template with reversibility frontmatter and pre-mortem section.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a adr-reversibility-tagging artefact validating against scripts/validate-adr-reversibility-tagging.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
adr_id: NNN
title: <decision_title>
reversibility: <two_way_door|partial_two_way|one_way_door_costly|one_way_door_irrevocable>
rollback_estimate:
  engineering_weeks: 0
  dollars_contract_exit: 0
  customers_affected: <none|internal_only|subset|all_active>
status: proposed
owner: <owner_full_name> <owner_email>
version: 1.0.0
last_reviewed: 2026-05-23
---

## Context

<one paragraph: why the decision was needed>

## Decision

<one paragraph: what was decided>

## Consequences

<bullets: trade-offs accepted>

## Alternatives

<bullets: options rejected with reasons>

## Pre-mortem (required if reversibility starts with one_way_door)

12 months from now this was wrong because:
1. <failure_scenario_1>
2. <failure_scenario_2>

Reversal triggers (if either fires within 6 months, reopen this ADR):
- <trigger_1>
- <trigger_2>
