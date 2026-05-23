---
slug: ai-call-site-inventory
tier: pro
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Report cataloguing every LLM call site in the codebase — file path, model, prompt version, schema version, fallback chain — required before any model migration or audit.
content_id: "cd9232a9ed610961"
complexity: medium
produces: report
est_tokens: 4900
tags: [call-site-inventory, ai-audit, migration, prompt-versioning, ml-engineering]
---

# AI Call Site Inventory

## Summary

**One-sentence:** Report cataloguing every LLM call site in the codebase — file path, model, prompt version, schema version, fallback chain — required before any model migration or audit.

**One-paragraph:** Report cataloguing every LLM call site in the codebase — file path, model, prompt version, schema version, fallback chain — required before any model migration or audit. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a report produced by an agent applying ai call site inventory. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible report for ai call site inventory across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- the codebase has multiple LLM call sites whose ownership is unclear
- an upcoming change (model deprecation, prompt overhaul, vendor migration) needs a full inventory first
- the team wants an audit trail of which features call which models with which prompts

## Skip If (ANY kills it)

- codebase has exactly one well-known LLM call — inventory is the call itself
- inventory was produced <30 days ago and the codebase has not changed materially — use the existing report
- the team uses a managed prompt registry that already lists call sites — refresh the registry instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-repo access (read) | git | engineering |
| Model registry or provider list | docs | ml-engineering |
| Prompt-storage convention | files or registry | ml-engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[AGENTS.md]] | Parent skill context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from real engagement | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `static_scan` | haiku | grep / AST scan for LLM SDK call sites. |
| `metadata_extraction` | sonnet | Lift model + prompt + schema metadata per call site. |
| `gap_audit` | sonnet | Identify untracked / version-less / schema-less calls. |

## Templates

| File | Purpose |
|------|---------|
| `templates/call-site-inventory.md` | Inventory report skeleton |
| `templates/output-schema.json` | Inventory JSON schema |
| `templates/_smoke-test.md` | Minimum viable filled-in inventory |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-call-site-inventory.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[agent-context-engineering-corpus-standard]]
- [[ai-feature-build-buy-finetune-decision]]
- [[eval-driven-development-tdd-for-ai]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
