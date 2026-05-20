---
slug: adr-consequence-evidence-binding
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: End-to-end playbook for adr consequence evidence binding that walks an operator from trigger to closed outcome with named artefacts at each step.
content_id: "1c260ffb07b68782"
tags: [adr, playbook, sdd]
---
# ADR Consequence Evidence Binding

## Summary

**One-sentence:** End-to-end playbook for adr consequence evidence binding that walks an operator from trigger to closed outcome with named artefacts at each step.

**One-paragraph:** End-to-end playbook for adr consequence evidence binding that walks an operator from trigger to closed outcome with named artefacts at each step. ADR Consequences are usually hand-waved. This methodology binds each Consequence to a specific file path, dependency version, or fitness-function ID and fails CI when the binding goes stale. Directly counters ADR decay.

## Applies If (ALL must hold)

- You are executing the cross-cutting workflow addressed by adr consequence evidence binding end to end.
- All inputs the playbook calls for are reachable (people, data, artefacts).
- The output is consumed by a named downstream owner with a deadline.
- Deviations from the steps are logged with a one-line rationale.

## Skip If (ANY kills it)

- Highly contextual one-shot work where playbook constrains the wrong axes.
- Pre-discovery — playbook assumes the problem is named.
- Teams already running a well-tuned variant — re-tooling friction outweighs upside.

## Prerequisites

- Stakeholders, owners, and deadlines named in advance.
- Inputs (data, briefs, accounts) reachable at start.
- Storage location for each step's output decided.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdd/sdd/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `input_collection` | haiku | Structured gather from inputs |
| `decision_steps` | sonnet | Apply playbook branches against state |
| `synthesis_writeup` | opus | Final artefact authoring |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/sdd/sdd/`
- peer methodologies: see siblings under `geek/sdd/sdd/`
- external: industry references cited inline in `content/01-core-rules.xml`
