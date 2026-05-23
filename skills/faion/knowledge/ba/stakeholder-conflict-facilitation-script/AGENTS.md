# Stakeholder Conflict Facilitation Script

## Summary

**One-sentence:** 60-minute structured five-phase meeting (frame → positions → rubric → decide → record dissent) that converts a requirement disagreement into a signed decision-log entry.

**One-paragraph:** 60-minute structured five-phase meeting (frame → positions → rubric → decide → record dissent) that converts a requirement disagreement into a signed decision-log entry. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned playbook-step artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- ≥2 стейкхолдери мають записану незгоду щодо requirement / scope / design.
- BA є фасилітатором (співфасилітатором), не пасивним учасником.
- стейкхолдерів можна звести в одну синхронну зустріч (in-person/video).
- рішення впливає на роботу, заплановану в найближчому sprint.
- потрібен підписаний decision-log, який пізніше не «розпарується».

## Applies If (ALL must hold)

- two or more named stakeholders disagree on a requirement, scope item, or design choice — disagreement is recorded.
- the BA owns or co-owns the resolution process (not pure escalation to a sponsor).
- stakeholders can be brought into one synchronous meeting (in-person or video).
- decision affects work that is committed within the next sprint cycle.

## Skip If (ANY kills it)

- pure escalation case where the sponsor will rule unilaterally.
- conflict is interpersonal, not requirements-based — needs HR/coaching.
- stakeholders refuse to commit to the rubric in advance — phase 3 collapses without it.
- decision can be safely deferred more than 2 sprints — run async clarification instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the playbook-step artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-conflict-facilitation-script.md` | Working playbook-step skeleton with 5-line header |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-conflict-facilitation-script.py` | Validate the playbook-step artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[stakeholder-conflict-mediation]]
- [[decision-rationale-capture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
