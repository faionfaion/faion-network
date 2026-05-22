---
slug: tool-deprecation-lifecycle
tier: geek
group: ai
domain: ai-core
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a deprecation playbook step for an LLM-agent tool: announce-window, dual-run, sunset, post-sunset error mode, with caller-cohort migration tracking."
content_id: "87d0b5208b92ca9e"
complexity: medium
produces: playbook-step
est_tokens: 3900
tags: [tool-use, deprecation, lifecycle, agent, ai, geek]
---

# Tool Deprecation Lifecycle

## Summary

**One-sentence:** Produces a deprecation playbook step for an LLM-agent tool: announce-window, dual-run, sunset, post-sunset error mode, with caller-cohort migration tracking.

**Ефективно для:** platform owners sunsetting an LLM-agent tool with live callers; PMs negotiating migration timelines; SREs setting up dual-run + sunset telemetry.

**One-paragraph:** This methodology pins the recurring decision around "tool-deprecation-lifecycle" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- A live tool has 1 or more active LLM-agent callers.
- A replacement tool exists or is planned within the announce window.
- Caller cohorts can be enumerated (org / agent / surface).
- Owner exists for both old and new tool through the lifecycle.

## Skip If (ANY kills it)

- Tool has zero callers — just delete it.
- Replacement is identical re-name only — rename instead of deprecate.
- Vendor / external dependency forces immediate sunset — incident playbook applies.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool card being deprecated | Markdown | platform repo |
| Caller cohort enumeration | CSV / JSON | telemetry |
| Replacement tool card or RFC | Markdown | platform repo |
| Owner for migration | handle / email | team roster |
| Sunset target date | ISO date | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[tool-card-template]]` | card shape of both old and new tool |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_announce` | haiku | Template fill from card. |
| `synthesize_dual_run_plan` | sonnet | Per-cohort migration ordering. |
| `escalate_blocker` | opus | Cross-cohort risk when migration stalls. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-deprecation-lifecycle.json` | JSON Schema for the Tool Deprecation Lifecycle output contract |
| `templates/tool-deprecation-lifecycle.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-deprecation-lifecycle.py` | Enforce the Tool Deprecation Lifecycle output contract | After subagent returns, before downstream consumer reads |

## Related

- [[tool-card-template]] — upstream artefact being deprecated.
- [[vendor-feature-portability-matrix]] — adjacent vendor-migration view.
- [[tool-trust-boundary-model]] — trust-boundary refresh on swap.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
