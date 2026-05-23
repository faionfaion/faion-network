---
slug: architecture-decision-records
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Capture each architectural decision in a single Markdown file (Nygard format) with context, decision, alternatives considered, and consequences, co-located with the code under docs/adr/NNN-title.md.
content_id: "e04a1ee4ff81d8de"
complexity: medium
produces: decision-record
est_tokens: 3600
tags: ["architecture", "adr", "decision-records", "documentation", "nygard"]
---
# Architecture Decision Records

## Summary

**One-sentence:** Capture each architectural decision in a single Markdown file (Nygard format) with context, decision, alternatives considered, and consequences, co-located with the code under docs/adr/NNN-title.md.

**One-paragraph:** ADRs make architectural decisions visible to new team members and future agents. Each ADR sits beside the code in docs/adr/, numbered sequentially from 001, and transitions through Proposed → Accepted → Deprecated/Superseded. New ADRs amend, never edit, Accepted ones. The five-section Nygard format forces explicit alternatives with rejection reasons so the same debate does not recur in week 4.

**Ефективно для:**

- Solo founder or small team where new decisions surface every week and the next agent must understand why.
- Refactor or stack-migration projects where decisions need an audit trail.
- Compliance regimes (SOC 2, ISO 27001) that require documented architectural rationale.
- Distributed agent workflows where the executor agent needs to load decisions before generating code.

## Applies If (ALL must hold)

- A meaningful architectural choice is about to be committed (database, framework, auth, deployment topology).
- At least two viable alternatives were seriously considered.
- The decision is hard to reverse — costs more than a day to undo.
- Future agents or new team members will need the context.

## Skip If (ANY kills it)

- Trivial implementation detail (which utility function, naming convention).
- Decision will certainly be revisited within 1-2 weeks — too early.
- Only one realistic option existed — no choice to record.
- Configuration value that belongs in docs/runtime.md, not an ADR.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| docs/adr/ index | directory listing | Repo file system |
| Relevant feature spec.md | markdown | Spec methodology output |
| design.md context | markdown | design-doc-structure output |
| Alternatives shortlist | list | Research / brainstorm |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-structure` | Spec provides the problem statement that triggers the decision. |
| `solo/sdd/sdd-planning/design-doc-structure` | Design doc carries the higher-level architecture this ADR slots into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-adr` | sonnet | Per-decision judgement on alternatives and consequences. |
| `compliance-review` | haiku | Scan ADR index for Accepted vs codebase drift. |
| `supersede-existing` | opus | Multi-document analysis when superseding multiple Accepted ADRs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/architecture-decision-records.json` | JSON skeleton conforming to the output contract schema. |
| `templates/architecture-decision-records.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architecture-decision-records.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-doc-structure]]
- [[writing-implementation-plans]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
