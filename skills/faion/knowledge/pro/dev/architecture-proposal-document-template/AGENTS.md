---
slug: architecture-proposal-document-template
tier: pro
group: dev
domain: architecture
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an architecture proposal: problem, constraints, options, decision, consequences, rollback.
content_id: "d59a8de2e1013c92"
complexity: medium
produces: spec
est_tokens: 5400
tags: [architecture, proposal, adr, spec, decision]
---

# Architecture Proposal Document Template

## Summary

**One-sentence:** Produces an architecture proposal: problem, constraints, options, decision, consequences, rollback.

**One-paragraph:** Produces an architecture proposal: problem, constraints, options, decision, consequences, rollback. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Cross-team, multi-system architecture decisions з high cost of reversal.
- Документований set of options з consequences, а не only the chosen path.
- Rollback strategy як first-class section, а не afterthought.

## Applies If (ALL must hold)

- Decision involves ≥3 systems or ≥2 teams.
- Decision is reversible only at high cost.
- Multiple options are credible.

## Skip If (ANY kills it)

- Single-team decision with low blast radius — use a lightweight ADR.
- Decision is forced by an external constraint (vendor mandate, regulation) — document, do not deliberate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem statement | markdown | sponsor |
| Constraint list | markdown | architecture |
| Option set with first-pass costs | markdown | architecture |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[architecture-review-meeting-facilitation]] | Proposal is consumed by the review meeting |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
| `content/05-examples.xml` | reference | One full worked example end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/arch-proposal.md` | Proposal skeleton with problem/constraints/options/decision/consequences/rollback |
| `templates/_smoke-test.md` | Filled-in proposal for a queue-vs-pubsub decision |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architecture-proposal-document-template.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[architecture-review-meeting-facilitation]]
- [[arch-health-weekly-report-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
