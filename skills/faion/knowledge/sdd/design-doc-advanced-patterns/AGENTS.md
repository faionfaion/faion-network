# Design Doc Advanced Patterns

## Summary

**One-sentence:** Apply advanced design-doc patterns (sequence diagrams, capacity sketches, failure-mode tables, migration playbooks) on top of the standard structure when the change is high-stakes or cross-system.

**One-paragraph:** A vanilla design doc covers most features. Advanced patterns kick in for cross-system changes, hot-path performance work, security boundaries, and irreversible migrations. This methodology layers four optional blocks — sequence diagram, capacity model, failure-mode table, migration playbook — onto the base design-doc-structure, with explicit triggers for when each block is mandatory rather than optional.

**Ефективно для:**

- Engineers writing a design doc for a multi-service change that touches a critical path.
- Security-relevant changes (auth, key handling) that need a documented threat model.
- Performance work where capacity must be modelled before implementation.
- Irreversible migrations (schema, data, deploy topology) that need a rollback playbook.

## Applies If (ALL must hold)

- Base design doc (design-doc-structure) already exists in draft.
- The change is cross-system, hot-path, security-relevant, or a migration.
- Reviewers will require evidence beyond prose (numbers, diagrams, tables).
- Stakes warrant the extra pages — rollback or outage cost is non-trivial.

## Skip If (ANY kills it)

- Single-service in-process change — base structure is enough.
- Cold-path internal tool — capacity model would be ceremony.
- Reversible config tweak — migration playbook is overkill.
- Prototype with no production deploy planned.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Base design doc draft | markdown | design-doc-structure output |
| Latency / throughput SLO | rubric | Ops runbook |
| Threat model template | markdown | Security baseline |
| Rollback budget | number (minutes) | Ops constraint |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/design-doc-structure` | Base layout this methodology extends. |
| `solo/sdd/sdd-planning/architecture-decision-records` | Cross-system decisions referenced by these patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sequence-diagram-block` | sonnet | Per-system reasoning about message flow. |
| `capacity-model` | opus | Multi-variable arithmetic + assumption gathering. |
| `failure-mode-table` | sonnet | Per-component judgement on failure surfaces. |
| `migration-playbook` | opus | End-to-end rollback design across services. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-doc-advanced-patterns.json` | JSON skeleton conforming to the output contract schema. |
| `templates/design-doc-advanced-patterns.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-doc-advanced-patterns.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-doc-structure]]
- [[architecture-decision-records]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
